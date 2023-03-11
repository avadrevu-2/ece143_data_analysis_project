import pandas as pd
import numpy as np
from data_processing import DataProcessing


def merge_df_by_dates(df_dict: dict, date_columns: set) -> tuple:
    '''
    Merge dataframes that have columns containing string dates
    by a newly created datetime column.
    '''
    assert len(df_dict)>1, 'Need more than 1 dataframe to merge.'
    failed_df=set()
    for dfID, dframe in df_dict.items():
        try:
            dframe=add_month_yr(dframe,date_columns)
            try:
                df=df.merge(dframe,on='month-yr')
                print('merged')
            except UnboundLocalError:
                print('no df')
                df=dframe
            # print(dframe)
        except TypeError:
            print(f'Dataframe {dfID} has no dates or timestamps.')
            failed_df.add(dfID)
        
    return (failed_df,fix_categorical(df))

def add_month_yr(x:pd.DataFrame, date_columns: set):
    '''
    Adds a month_yr column to a dataframe that has a column
    containing date strings.
    '''
    for column in date_columns:
        if column in x:
            # print(pd.to_datetime(x[column]))
            # print(x[column])
            # x['datetime']=pd.to_datetime(x[column])
            x['month-yr']=pd.to_datetime(x[column]).dt.strftime('%b-%Y')
            return x
    raise TypeError

def fix_categorical(x):
    '''Changes 'month-yr' column to CategoricalDtype'''
    assert isinstance(x,pd.DataFrame)
    dates=pd.DataFrame(x['month-yr'])
    dates['Timestamp']=pd.to_datetime(x['month-yr'])
    dates=dates.sort_values(by=['Timestamp'])
    sorted=[]
    [sorted.append(x) for x in dates['month-yr'] if x not in sorted]
    t=pd.CategoricalDtype(categories=sorted,ordered=True)
    x['month-yr'] = pd.Series(x['month-yr'],dtype=t)
    return x


if __name__=='__main__':
    data_dir = 'data'
    processor = DataProcessing(data_dir)
    data_dict=processor.process()
    bad_dict={'dud_df':pd.DataFrame(np.zeros((5,5)))}
    data_dict.update(bad_dict)
    print([[i for i in j] for j in data_dict.values()])
    date_columns={'timestamp','date'}

    unmerged_set,merged_df= merge_df_by_dates(data_dict,date_columns)
    # print(unmerged_set)
    print([i for i in merged_df])
    print(merged_df)
    # temp_df=pd.DataFrame(np.zeros((5,5)))
    # temp_df2=pd.DataFrame(np.zeros((5,5)))
    # print(temp_df.merge(temp_df2))