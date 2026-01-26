import numpy as np

class DiscountCurve:
    def __init__(self, datapoints, interpolation="log_linear", bounds = None):

        self.bounds = bounds
        if bounds is None:
            self.bounds = {
                'min_rate': 0.0,     # Rates shouldn't be negative (usually)
                'max_rate': 0.50,    # 50% maximum (adjust for hyperinflation markets)
                'min_df': 0.001,      # Discount factors shouldn't be near zero
                'max_df': 1.01,       # Discount factors may barely go above 1 for overnight market differences
            }
        
        datapoints = sorted(datapoints) # Sorts data by time since settlement date
        pillars_t, pillars_df = zip(*datapoints)
        self.times = np.array(pillars_t, dtype=float) # Convert to numpy arrays for easier maths
        self.dfs = np.array(pillars_df, dtype=float)
        self.interpolation = interpolation
        
        self.validate();
        
    def interpolate(self, grain = 10):
        # datapoints: array of tuples, each tuple should be of form (float, float) and containts
        # in order the time of the datapoint and the difference factor at that time
        # grain: Integer, how fine the interpolation should be
    
        # These lines ensure grain is an integer greater than 1
        grain = np.floor(grain)
        if grain<1:
            grain = 1
    
        # Generates interpolated datapoints between inputted datapoints
        if(self.interpolation == "log_linear"):
            new_pillars_t = []
            log_df = np.log(self.dfs) # preparing for linearly interpolating between log of datapoints
            new_pillars_df = []
            for t in range(len(self.times)-1): # For every time pillar
                interval_length = self.times[t+1]-self.times[t] # Find distance to next time pillar
                df_difference = log_df[t+1]-log_df[t] # Calculate difference in DF values at the time pillars
                for i in range(grain): # linearly adds datapoints between the pillars
                    new_pillars_t.append(self.times[t]+(i/grain)*interval_length)
                    new_pillars_df.append(log_df[t]+(i/grain)*df_difference)
            new_pillars_t.append(self.times[-1])
            new_pillars_df.append(np.log(self.dfs[-1]))
    
            new_pillars_df = np.exp(new_pillars_df) #reverts the logarithmic data into standard data
            new_data = zip(new_pillars_t, new_pillars_df) # recombines the time and DFs
            
            return new_data
        elif(self.interpolation == "linear"):
            return zip(self.times, self.dfs)
        else:
            print("Unknown interpolation method, used linear interpolation instead.")
            return zip(self.times, self.dfs)

    def calcDF(self, t):
        before = 0 # will be used to find the latest time pillar before t
        after = 0 # will be used to find the earliest time pillar after t
        i = np.searchsorted(self.times, t) # will be used to index the Discount Factor array later
        for time in self.times:
            if(before <= t and t <= after): # Checks if we have surrounded t, this method produces an edge case
                break
            else: # Iterates
                before = after
                after = time
        if(before > t): # This works correctly by accident. No need to fix it, however.
            return 1;
        elif(t>after): # If a t value outside the Discount Factors range is inputted use the
                       # last recorded discount factor
            return self.dfs[-1]
        elif(i==0): # Edge case, is only triggered in the event that t = 0
            return 1;
        
        before_df = self.dfs[i-1] # These lines index the corresponding discount factors
        after_df = self.dfs[i]
        
        prop_dist = (t-before)/(after-before) # Calculates how far we are between the time pillars
        log_before = np.log(before_df) # Converts discount factors to logarithms
        log_after = np.log(after_df)
        log_diff = log_after-log_before
        
        log_df = log_before + log_diff*prop_dist # log_diff*prop_dist is the distance between the
        # df pillars that corresponds to the distance between time pillars required.
        
        df = np.exp(log_df)
        return df

    def plot(self, interpolated = True): # Misleading name, function returns the data needed to plot the curve
        if(interpolated): # interpolation is set true when graphing for clean visuals and false for tables for easy reading
            datapoints = self.interpolate()
            times, dfs = zip(*datapoints)
            return times, dfs
        else:
            return self.times, self.dfs
    
    def plot_zero_rates(self, Interpolated = True): # Misleading name, function returns the data needed to plot the curve
        if(Interpolated): # interpolation is set true when graphing for clean visuals and false for tables for easy reading
            datapoints = self.interpolate() # rather than coding a new interpolation function, we simply interpolate dfs before converting to rates
        else:
            datapoints = zip(self.times, self.dfs)
        
        rates = []
        times = []
        for time, ___ in datapoints:
            if(time == 0):
                continue # Do not plot zero rates for t = 0, which normally leads to an undefined expression
            else:
                times.append(time) # appends time pillar data
                rates.append(self.rate_from_df(time)) # calculates zero rates and appends pillar data
                
        return times, rates
    
    def validate(self):
        # Personal note, these bounds are more likely to be triggered when working with made up toy data.
        if(min(self.dfs) < self.bounds["min_df"]):
            raise ValueError(f"Warning: Provided discount factors exceed tolerated bounds: {min(self.dfs)} < {self.bounds["min_df"]}")
        if(max(self.dfs) > self.bounds["max_df"]):
            raise ValueError(f"Warning: Provided discount factors exceed tolerated bounds: {max(self.dfs)} > {self.bounds["max_df"]}")
        if(min(self.times < 0)):
            raise ValueError(f"Warning: Pillar times may not be less than to zero.")
        if(self.times[0]!=0):
            raise ValueError(f"Warning: Expected initial time pillar to be t = 0, got: +{self.times[0]}")
        elif(self.dfs[0]!=1):
            raise ValueError(f"Warning: Illogical data used. Discount factor should always equal 1 at t = 0.")
        for i in range(len(self.times)-1):
            if self.dfs[i]<self.dfs[i+1]:
                raise ValueError(f"Warning, discounts provided are increasing.")
    
    def update_data(self, datapoints, interpolation = "log_linear"):
        datapoints = sorted(datapoints) # Sorts data by time since settlement date
        # Convert to numpy arrays for easier maths
        pillars_t, pillars_df = zip(*datapoints)
        self.times = np.array(pillars_t, dtype=float)
        self.dfs = np.array(pillars_df, dtype=float)
        #
        self.interpolation = interpolation
        
        self.validate(); # Checks that the updated curve is valid
        
    def rate_from_df(self, time):
        df = self.calcDF(time) # calucaltes df at time = time which will later be used to calculate zero rate
        #rate = freq*(1/np.power(df,1/(freq*time))-1) # Discrete formula for conversion from discount factor to zero rate
        rate = -np.log(df)/time # Continuous formula, less accurate against murex results
        if rate < self.bounds['min_rate']: # validating rates
            raise ValueError(f"Warning: Rate {rate:.2%} at t={time:.2f} below minimum")
        if rate > self.bounds['max_rate']: # validating rates
            raise ValueError(f"Warning: Rate {rate:.2%} at t={time:.2f} above maximum")
        return rate
    #