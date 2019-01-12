# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 16:39:28 2018

@author: Tim
"""
__version__ = '1.21'

import re
import dateutil.parser as p
import pandas as pd

ba_len = 8

def get_datestring(donor_line):
    first_of_month = donor_line.split('from')[-1].split('to')[0].strip()
    dtobject = p.parse(first_of_month)
    year = dtobject.year
    month = dtobject.month
    return '_{}_{}'.format(year, month)

def processfile(f):
    """
    Turns the csv file into a single line and removes the 
    extra commas, the Deduction and Premium columns
    """
    #do these constants change?  Will have to see
    up_to_Deduction =6
    from_Premium = 8
    #get the account number
    account_num = input('PI Account Number: ')
    print('\n')
    if account_num in f:
        donor = f.splitlines()
        datestring = get_datestring(donor[1])
        donors_on_one_line = []
        tempdonor=''
        for idx,d in enumerate(donor):
            if account_num in d:
                donors_on_one_line.append(tempdonor)
                tempdonor=d
            else:
                tempdonor += d
        dool = [re.sub(r',+',',',d) for d in donors_on_one_line][1:]
        dool1 = [x.split(',') for x in dool]
        dool2 = [','.join(x[:up_to_Deduction]+x[from_Premium:]) for x in dool1]
    else:
        #file does not contain account_num
        dool2 = None
        datestring = None
        account_num = None
    return (dool2, datestring, account_num)

def parseinfo(infostring):
    """
    Pulls out the address1 as a single entity as well as the city,
    state,zip or postalcode and phonenumber using a regex
    """
    infosplit = infostring.split(',')
    rest = infosplit[-1].strip()
    city = infosplit[-2].strip()
    address1 = ' '.join(infosplit[:-2]).strip()
    match = re.search(r'(\w+)\s+(\w\d\w\s\d\w\d)\s+(.*)',rest)
    try:
        state = match.group(1).strip()
        zipcode = match.group(2).strip()
        phonenumber = match.group(3).strip()
        return (address1,city,state,zipcode,phonenumber)
    except:
        print('Issues parsing donor info for '+infostring.split(',')[4])
        return (infostring)
    
def getinfostring(dool):
    return re.search(r'(.*)"(.*)"(.*)',dool)

def get_valid_csv_file():
    #get a valid csv file
    while True:
        try:
            #TODO: remove delimiter
            fname = input('Enter name of Excel donor file: ')
            if fname:
                if fname.split('.')[1] in ['xls','xlsx']:
                    try:
                        #read the csv file
                        csv_file = pd.read_excel(fname).to_csv(index=False)
                        break
                    except (PermissionError,TypeError,FileNotFoundError) as e:
                        print(fname+' is not a valid closed csv file')
                        print(e)
            else:
                break
        except IndexError:
            print('File needs to have an extension of xls or xlsx')
    return (csv_file,fname)

def check_comma_in_amount(ba_split):
    if len(ba_split) == ba_len:
        new_ba_split = ba_split
    else:
        #fixes a number like 1,000 split on a comma and reassembles
        new_amount = ba_split[-3] + ba_split[-2]
        new_ba_split = ba_split[:-3] + [new_amount] + [ba_split[-1]]
    return new_ba_split

def dateformat(ba):
    
    ba_split = ba.split(',')
    new_ba_split = check_comma_in_amount(ba_split)
    transactiondate = p.parse(new_ba_split[1])
    datestring = str(transactiondate.month)+'/'+\
        str(transactiondate.day)+'/'+str(transactiondate.year)
    new_ba_split[1]=datestring
    return ','.join(new_ba_split)

def get_donorstrings(dool):
    #create the donorstring list and populate with headers
    donorstrings=[]
    headers = ',employeeID,Date,Num,Related Donor IDS,Name,Pay Meth,Amount,Name E-mail,Memo,Name Street1,Name Street2,Name Street3,Name City,Name State,Name Zip,Name Phone #'
    donorstrings.append(headers)
    #parse the donor rows
    for idx in range(1,len(dool)):
        #splits the donor row into 3 parts which are divided on ""
        #into beforeaddress, address and afteraddress
        infostring = getinfostring(dool[idx])
        beforeaddress = infostring.group(1)
        beforeaddress_with_formatted_date = dateformat(beforeaddress)
        prepended_extra_comma = ','
        address = parseinfo(infostring.group(2))
        afteraddress = infostring.group(3)
        #splits the afteraddress into email and memo
        aa = afteraddress.split(',')
        email = aa[1]
        if len(aa) > 2:
            memo =aa[2]
        else:
            memo =''
        #appends all the itemized info into the donor row
        donorstrings.append(prepended_extra_comma + beforeaddress_with_formatted_date+'{0},{1},{2},,,{3},{4},{5},{6}'.\
            format( email,
                    memo,
                    address[0],
                   address[1],
                   address[2],
                   address[3],
                   address[4]))
    return donorstrings
        
def write_new_csv(fname,donorstrings, datestring, account_num):
    #writes the donorstrings to a csv file row by row
    try:
        output_filename_string = 'parsed_{}{}.csv'.format(account_num, datestring)
        with open(output_filename_string, 'w') as f:
            for d in donorstrings:
                f.write(d+'\n')
            print('Your new file will be called {}'.format(output_filename_string))
    except (PermissionError) as e:
        print('File is already open...')
        print(e)
        f = None
    return f

def main():  
    f,fname = get_valid_csv_file()
    # turn the file into donors_on_one_line
    dool, datestring, account_num = processfile(f)
    if dool:
        #get donor strings parsed correctly
        donorstrings = get_donorstrings(dool)
        print('Finished processing csv file...')
        f = write_new_csv(fname,donorstrings, datestring, account_num)
        print('Finished writing new parsed csv file...')
        return f
    else:
        print('File and account number don\'t match')
        return None

if __name__=="__main__":
    f = main()
