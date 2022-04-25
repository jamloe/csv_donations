#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 17:11:50 2022

@author: jamloe

"""

__version__ = '2022.04'

import re
import pandas as pd

def read_valid_excel_file():
    #get a valid csv file
    while True:
        try:
            #TODO: remove delimiter
            fname = input('Enter name of Excel donor file: ')
            if fname:
                if fname.split('.')[1] in ['xls','xlsx']:
                    try:
                        #read the excel file and remove total
                        df = pd.read_excel(fname)[:-1]
                        break
                    except (PermissionError,TypeError,FileNotFoundError) as e:
                        print(fname+' is not a valid closed csv file')
                        print(e)
            else:
                break
        except IndexError:
            print('File needs to have an extension of xls or xlsx')
    return (df[:-1],fname)

def get_account_number(df):
    account_num = df.iloc[0]['Account']
    df = df.drop('Account',axis=1)
    return df, account_num

def format_df(df):
    #fill empty Donor with previous Donor
    df['Donor'] = df['Donor'].fillna(method='ffill')
    
    #rename column labels
    df = df.rename(
        columns={
            "Row Labels": "employeeID","Donor":"Name", "Payment Type":"Pay Meth",
            "Sum of Amount":"Amount"
            })
        
    #date to correct format
    # find the the month and year of the report for file naming
    dt_string = df['Date'].min() # Earliest date
    report_period = str(dt_string.year)+'_'+str(dt_string.month)
    
    df['Date'] = df['Date'].apply(lambda row:row.strftime("%m/%d/%Y"))
       
    #replace text "(blank)" in address column with whitespace
    df = df.replace({'(blank)':''})
    
    df = df.replace({'Bank (Ach)':'Bank'})
    
    # change Pay Meth entries to acceptable 18 character length
    df = df.replace('Credit / Debit Card','Credit Card')
    df = df.replace('External Credit / Debit','External Card')
    
    
    # insert blank column at start of table
    df.insert(loc=0, column='', value=['' for i in range(df.shape[0])])
    
    df['Name E-mail'] = df['Account Email'] + df['Contact Email']
    
    df['address'] =df['Account Address'] + df['Contact Address']
    
    #Make all addresses 3 lines long
    df['address'] = df['address'].apply(lambda row:re.sub(r'\n',' ',row,1) if row.count('\n')==3 else row)
    return df, report_period    

def parse_address(df):
    #parses df['address'] into the lines below:
    #df['Name Street1'] = '#58 - 26970 32 Ave' or 'C/O Fulaan #58 - 26970 32 Ave'
    #df['Name City'] = 'Aldergrove'
    #df['Name State'] = 'BC'
    #df['Name Zip'] = 'V4W 3T4'
    #df['Country'] = 'Canada'
    regex_string = '^(.*)\\n(.*)\\s([A-Z]{2})\\s([A-Z]\\d[A-Z]\\s\\d[A-Z]\\d)\\n(.*)'
    regex = re.compile(regex_string)
    address_df = pd.DataFrame([match.groups() if match else ('','','','','') for match in df['address'].apply(lambda row: regex.search(row))],
                              columns=['Name Street1', 'Name City','Name State','Name Zip','Country'])
    #Changes CAN to Canada
    address_df['Country'] = address_df['Country'].apply(lambda row:('Canada' if row=='CAN' else row))
    return address_df

df, fname = read_valid_excel_file()

#get the account number
df, account_num = get_account_number(df)

#format the dataframe
formatted_df,report_period = format_df(df)
#parse the address
address_df = parse_address(formatted_df)
#merge the databases together
df = pd.concat([df,address_df], axis=1)
#name and save the new dataframe as a csv file
output_filename_string = 'parsed_{}_{}.csv'.format(account_num, report_period)
df.to_csv("parsed_{}_{}.csv".format(account_num,report_period), index=False, encoding='utf-8', )
print('Your new file will be called {}:'.format(output_filename_string))
