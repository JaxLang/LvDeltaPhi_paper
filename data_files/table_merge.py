import os
import numpy as np
import pandas as pd
from datetime import datetime as dt

def convert_dt(item, datum, timum): #string, bool, bool
    if datum and not timum:
        new_item = dt.strptime(item, "%Y %b. %d")
#         print(new_item)
        return new_item#.strftime("%Y-%m-%d")

    elif datum and timum:
        new_item = dt.strptime(item, "DD/MM/YY %H:%M")
        print(new_item)
        return new_item#.strftime("%Y-%m-%d %H:%M")

    elif timum and not datum:
        if len(item)>5:
            item = item[:5]
        new_item = dt.strptime(item, "%H:%M")
        print(new_item)
        return new_item#.strftime("%H:%M")




# read in all the files
tab2 = pd.read_csv(f"{os.getcwd()}/PaassEA18_tab2.csv",index_col=0, header=[0,1])
tab3 = pd.read_csv(f"{os.getcwd()}/PaassEA18_tab3.csv",index_col=0, header=[0,1])
tab4 = pd.read_csv(f"{os.getcwd()}/PaassEA18_tab4.csv",index_col=0, header=[0,1])
tab5 = pd.read_csv(f"{os.getcwd()}/PaassEA18_tab5.csv",index_col=0, header=[0,1])
tab6 = pd.read_csv(f"{os.getcwd()}/PaassEA18_tab6.csv",index_col=0, header=[0,1])

tables = [tab2, tab3, tab4, tab5, tab6]


# create a list of all the events
all_events = []
for x in tab2['Date']['Date']:
    all_events.append(convert_dt(x, True, False))
print(all_events)


# iterate through each table and make the fixes
for dft in tables:
    # remove all white space before/after alphanumeric chars
    dft = dft.apply(lambda x: x.str.strip() if x.dtype == 'object' else x)

    # convert initial date column to date object
    dft.loc[:,('Date','Date')] = dft.loc[:,('Date','Date')].apply(lambda x: convert_dt(x, True, False))

    # Check that all the dates in the tabs are in the list
    # print(dft.loc[:,('Date','Date')])
    for x in dft.loc[:,('Date','Date')]:
        if x.strftime("%Y-%m-%d") in all_events:
            print(x)
            jax = input("Fix this.")

# make a new df that contains all the tables
df = pd.DataFrame(columns=all_events)

full_df = pd.concat(tables, axis=1)
print(full_df)

#save to a usable csv for future use - note that it will make multiple Date/Date columns
full_df.to_csv('paassEA18_data.csv')

