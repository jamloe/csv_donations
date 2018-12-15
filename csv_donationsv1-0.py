# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 16:39:28 2018

@author: Tim
"""
__version__ = '1.0'

import re

ba_len = 8

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
    return dool2

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
    is_csv = False
    #get a valid csv file
    while not is_csv:
        try:
            fname = input('Enter name of csv donor file: ')
            if fname.split('.')[1]=='csv':
                try:
                    #read the csv file
                    f = open(fname,'r').read()
                    is_csv=True
                except (PermissionError,TypeError,FileNotFoundError) as e:
                    print(fname+' is not a valid closed csv file')
                    print(e)
            else:
                is_csv=False    
        except IndexError:
            print('File needs to have an extension of csv')
    return (f,fname)

def dateformat(ba):
    import dateutil.parser as p
    
    ba_split = ba.split(',')
    transactiondate = p.parse(ba_split[1])
    datestring = str(transactiondate.month)+'/'+\
        str(transactiondate.day)+'/'+str(transactiondate.year)
    ba_split[1]=datestring
    return ','.join(ba_split)

def get_donorstrings(dool):
    #create the donorstring list and populate with headers
    donorstrings=[]
    headers = 'employeeID,Date,Num,Related Donor IDS,Name,Pay Meth,Amount,Name E-mail,Memo,Name Street1,Name Street2,Name Street3,Name City,Name State,Name Zip,Name Phone #'
    donorstrings.append(headers)
    #parse the donor rows
    for idx in range(1,len(dool)):
        #splits the donor row into 3 parts which are divided on ""
        #into beforeaddress, address and afteraddress
        infostring = getinfostring(dool[idx])
        beforeaddress = infostring.group(1)
        beforeaddress_with_formatted_date = dateformat(beforeaddress)
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
        donorstrings.append(beforeaddress_with_formatted_date+'{0},{1},{2},,,{3},{4},{5},{6}'.\
            format( email,
                    memo,
                    address[0],
                   address[1],
                   address[2],
                   address[3],
                   address[4]))
    return donorstrings
        
def write_new_csv(fname,donorstrings):
    #writes the donorstrings to a csv file row by row
    try:
        with open('parsed_'+fname,'w') as f:
            for d in donorstrings:
                f.write(d+'\n')
            print('Your new file will be called parsed_'+fname)
    except (PermissionError) as e:
        print('File is already open...')
        print(e)
        f = None
    return f

def main():  
    f,fname = get_valid_csv_file()
    # turn the file into donors_on_one_line
    dool = processfile(f)
    if dool:
        #get donor strings parsed correctly
        donorstrings = get_donorstrings(dool)
        print('Finished processing csv file...')
        return write_new_csv(fname,donorstrings)
        print('Writing new parsed csv file...')
    else:
        print('File and account number don\'t match')
        
if __name__=="__main__":
    main()