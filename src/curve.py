import matplotlib.pyplot as plt
import numpy as np

class DiscountCurve:
    def __init__(self, datapoints, interpolation="log_linear"):
        # Convert to numpy arrays for easier math
        pillars_t, pillars_df = zip(*datapoints)
        self.times = np.array(pillars_t, dtype=float)
        self.dfs = np.array(pillars_df, dtype=float)
        self.interpolation = interpolation
        
    def interpolate(this, grain = 10):
        # datapoints: array of tuples, each tuple should be of form (float, float) and containts
        # in order the time of the datapoint and the difference factor at that time
        # grain: Integer, how fine the interpolation should be
    
        # These lines ensure grain is an integer greater than 1
        grain = np.floor(grain)
        if grain<1:
            grain = 1
    
    
        # Generates interpolated datapoints between inputted datapoints
        new_pillars_t = []
        log_df = np.log(this.pillars_df) # preparing for linearly interpolating between log of datapoints
        new_pillars_df = []
        for t in range(len(this.pillars_t)-1): # For every time pillar
            interval_length = this.pillars_t[t+1]-this.pillars_t[t] # Find distance to next time pillar
            df_difference = log_df[t+1]-log_df[t] # Calculate difference in DF values at the time pillars
            for i in range(grain): # linearly adds datapoints between the pillars
                new_pillars_t.append(this.pillars_t[t]+(i/grain)*interval_length)
                new_pillars_df.append(log_df[t]+(i/grain)*df_difference)
        new_pillars_t.append(this.pillars_t[-1])
        new_pillars_df.append(np.log(this.pillars_df[-1]))
    
        new_pillars_df = np.exp(new_pillars_df) #reverts the logarithmic data into standard data
        new_data = zip(new_pillars_t, new_pillars_df) # recombines the time and DFs
        
        #this.pillars_df = new_pillars_df
        #this.pillars_t = new_pillars_t
        return new_data

    def caclDF(self, t):
        before = 0
        after = 0
        for time in self.times:
            if(before <= t and t <= after):
                break
            else:
                before = after
                after = time
        if(before > t):
            return 1
        elif(t>after):
            return self.dfs[-1]
        
        df = 0
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

df = DiscountCurve([(0,1),(1,0.75),(2,0.5),(3,0.25)])
print(df.caclDF(10))