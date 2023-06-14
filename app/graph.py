import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

def make_data_frame(data:object):
    """
    Function used for making a dictionary out of Data class.
    Then the dictionary is used to make a pandas DataFrame
    """
    new_dict={"TEMP":[],"HYDRATION":[], "PH":[], "TIME":[]}
    
    for d in data:
        # print(d)
        # print(d.sen_temp)
        new_dict["TEMP"].append(d.sen_temp)
        new_dict["HYDRATION"].append(d.sen_hydration)
        new_dict["PH"].append(d.sen_pH)
        new_dict["TIME"].append(d.sen_date)
        
    df= pd.DataFrame(new_dict)
        
    df["TIME"] = df["TIME"].dt.strftime('%d.%m.%Y. %H:%M:%S')
    return df
    
def plot_graph(df, plot_type:str):
    """
    Function used for ploting graphs out of the pandas dataframe that was made from
    the Data class.
    @params
    df - pandas dataframe
    @params
    plot_type - string for determining plot type (bar, pie, line)
    """
    
    fig, axes = plt.subplots(nrows=2, ncols=2)

    if plot_type == "pie":
        # iloc slices the dataframe
        df.iloc[-10:].plot(kind=plot_type,
                    y='TEMP',
                    ax=axes[0,0])
        df.iloc[-10:].plot(kind=plot_type,
                    y='HYDRATION',
                    ax=axes[0,1])
        df.iloc[-10:].plot(kind=plot_type,
                    y='PH',
                    ax=axes[1,0])
    else:
    
        df.iloc[-10:].plot(kind=plot_type,
                    x='TIME',
                    y='TEMP',
                    color='green',ax=axes[0,0])
        df.iloc[-10:].plot(kind=plot_type,
                    x='TIME',
                    y='HYDRATION',
                    color='blue',ax=axes[0,1])
        df.iloc[-10:].plot(kind=plot_type,
                    x='TIME',
                    y='PH',
                    color='red', ax=axes[1,0])
    
    plt.show()
    

    