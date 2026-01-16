import matplotlib.pyplot as plt
import numpy as np

class DiscountCurve:
    def __init__(self, datapoints, interpolation="log_linear"):
        datapoints = sorted(datapoints) # Sorts data by time since settlement date
        # Convert to numpy arrays for easier maths
        pillars_t, pillars_df = zip(*datapoints)
        self.times = np.array(pillars_t, dtype=float)
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

    def calcDF(self, t):
        # The idea behind this function is to find which 2 time pillars surround the t we are
        # interested in. Then we use log-linear interpolation to find the correct df value.
        
        before = 0 # will be used to find the latest time pillar before t
        after = 0 # will be used to find the earliest time pillar after t
        i = -1 # will be used to index the Discount Factor array later
        for time in self.times:
            if(before <= t and t <= after): # Checks if we have surrounded t, this method produces an edge case
                break
            else: # Iterates
                before = after
                after = time
                i+=1
        if(before > t): # This works correctly by accident. No need to fix it, however.
            return 1;
        elif(t>after): # If a t value outside the Discount Factors range is inputted use the
                       # last recorded discount factor
            return self.dfs[-1]
        elif(i==-1): # Edge case, is only triggered in the event that t = 0
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

    def plot(self, interpolated = False):
        if(interpolated):
            datapoints = self.interpolate()
        else:
            datapoints = zip(self.times, self.dfs)
        
        times, dfs = zip(*datapoints)
        plt.plot(times, dfs)
        plt.xlabel('Time (years)')
        plt.ylabel('Discount Factor')
        plt.title('Discount Factor Curve')
        plt.grid()
        plt.show()
        return 0
    
    def validate(self):
        valid = True
        if(min(self.dfs <= 0)):
            print("Warning: Discount Factors may not be less than or equal to zero.")
            valid = False
        if(min(self.times < 0)):
            print("Warning: Pillar times may not be less than to zero.")
            valid = False
        if(self.times[0]!=0):
            print("Warning: Expected initial time pillar to be t = 0, got: " +str(self.times[0]))
            valid = False
        elif(self.dfs[0]!=1):
            print("Warning: Illogical data used. Discount factor should always equal 1 at t = 0.")
            valid = False
        for i in range(len(self.times)-1):
            if self.dfs[i]<self.dfs[i+1]:
                print("Warning, discount provided are not decreasing.")
                valid = False
                break;
        
        if(valid):
            print("Valid curve, continue.")
        else:
            print("invalid curve")
    
    def update_data(self, datapoints, interpolation = "log_linear"):
        datapoints = sorted(datapoints) # Sorts data by time since settlement date
        # Convert to numpy arrays for easier maths
        pillars_t, pillars_df = zip(*datapoints)
        self.times = np.array(pillars_t, dtype=float)
        self.dfs = np.array(pillars_df, dtype=float)
        self.interpolation = interpolation
        
        self.validate();