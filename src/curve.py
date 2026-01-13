import matplotlib.pyplot as plt
import numpy as np

def interpolate(datapoints, grain = 10):
    # grain: Integer, how fine the interpolation should be
    
    # These lines ensure grain is an integer greater than 1
    grain = np.floor(grain)
    if grain<1:
        grain = 1
    
    
    # Generates 10 interpolated datapoints between inputted datapoints
    pillars_t, pillars_df = zip(*datapoints)
    new_pillars_t = []
    log_df = np.log(pillars_df)
    new_pillars_df = []
    for t in range(len(pillars_t)-1):
        interval_length = pillars_t[t+1]-pillars_t[t]
        df_difference = log_df[t+1]-log_df[t]
        for i in range(grain):
            new_pillars_t.append(pillars_t[t]+(i/grain)*interval_length)
            new_pillars_df.append(log_df[t]+(i/grain)*df_difference)
    
    new_pillars_df = np.exp(new_pillars_df)
    new_data = zip(new_pillars_t, new_pillars_df)
    #print(new_data)
    return new_data

def plot(datapoints):
    times, dfs = zip(*datapoints)
    plt.plot(times, dfs)
    plt.xlabel('Time (years)')
    plt.ylabel('Discount Factor')
    plt.title('Discount Factor Curve')
    plt.show()
    return 0

data = [(0,1), (1,0.5)]
plot(interpolate(data))