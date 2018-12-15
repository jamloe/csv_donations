# -*- coding: utf-8 -*-

import os

def file_rename():
    oldname=input("Old name: ") #Get the old file name, don't forget the extention
    newname=input("New name: ") #Get the new file name (excluding the extention)
    #os.rename(oldname,newname + ".txt") #Renames the file
    os.rename(oldname,newname)

file_rename() #Calls the function above