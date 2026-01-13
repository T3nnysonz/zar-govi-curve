import matplotlib.pyplot as plt
import numpy as np

def interpolate(datapoints, grain = 10):
    # datapoints: array of tuples, each tuple should be of form (float, float) and containts
    # in order the time of the datapoint and the difference factor at that time
    # grain: Integer, how fine the interpolation should be
    
    # These lines ensure grain is an integer greater than 1
    grain = np.floor(grain)
    if grain<1:
        grain = 1
    
    
    # Generates interpolated datapoints between inputted datapoints
    pillars_t, pillars_df = zip(*datapoints) # Seperating tuples
    new_pillars_t = []
    log_df = np.log(pillars_df) # preparing for linearly interpolating between log of datapoints
    new_pillars_df = []
    for t in range(len(pillars_t)-1): # For every time pillar
        interval_length = pillars_t[t+1]-pillars_t[t] # Find distance to next time pillar
        df_difference = log_df[t+1]-log_df[t] # Calculate difference in DF values at the time pillars
        for i in range(grain): # linearly adds datapoints between the pillars
            new_pillars_t.append(pillars_t[t]+(i/grain)*interval_length)
            new_pillars_df.append(log_df[t]+(i/grain)*df_difference)
    new_pillars_t.append(pillars_t[-1])
    new_pillars_df.append(np.log(pillars_df[-1]))
    
    new_pillars_df = np.exp(new_pillars_df) #reverts the logarithmic data into standard data
    new_data = zip(new_pillars_t, new_pillars_df) # recombines the time and DFs
    return new_data

def plot(datapoints):
    times, dfs = zip(*datapoints)
    plt.plot(times, dfs)
    plt.xlabel('Time (years)')
    plt.ylabel('Discount Factor')
    plt.title('Discount Factor Curve')
    plt.grid()
    plt.show()
    return 0

data = [(0,1), (1,0.9), (2,0.75),(3,0.4),(4,0.1)]
plot(interpolate(data))