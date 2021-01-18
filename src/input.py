"""
Utility functions to handle inputs for downstream task of downloading from these URLs.
"""
import os
import csv
import requests

class InputException(Exception):
    pass

# Raised for wrongly formatted files
class FileFormatException(InputException):
    def __init__(self, message):         
        super().__init__(message)

# Raised for empty file
class EmptyFileException(InputException):
    def __init__(self, message):         
        super().__init__(message)

  
def readTxtFile(fname):
    """
    Helper method to read txt File
    Parameters:
        fname - (str) Path to input txt file

    """   
    res = set()  
    with open(fname, 'r') as f:
        data = f.readlines()
        for i in data:             
            for j in i.split(" "):
                j = j.strip()
                if(len(j) > 0):
                    res.add(j)
     
    return res
    

def readCsvFile(fname):
    """
    Helper method to read csv File
    Parameters:
        fname - (str) Path to input csv file

    """   
    res = set()
    with open(fname, "r") as f:
        reader = csv.reader(f, delimiter="\t")
         
        for line in reader:             
            if(len(line)>0):
                for j in line[0].split(","):
                    j = j.strip()
                    if(len(j) >0):
                        res.add(j)
    
    
    return res

# Map file format to its respective handling function
inputHandler = {
    '.txt':readTxtFile,
    '.csv':readCsvFile
}

 
def readFile(fname):
    """
    Main method for reading input path files
    Parameters:
        fname - (str) Path to input file (txt or csv)

    """   
    # Input Path Error
    if(not os.path.exists(fname)):
        raise FileNotFoundError("Input file: {} does not exist".format(fname))
    
    _, ext = os.path.splitext(fname)
    
    # Input format not supported
    if(ext not in inputHandler):
        raise FileFormatException("Input file format {} not supported".format(ext))
    
    # Set used to prevent unnecessary download of duplicate files
    urlSet = inputHandler[ext](fname)

    if(len(urlSet)==0):
        raise EmptyFileException("No URLs found or file is improperly formatted")

    # print("FINAL",urlSet)

    return urlSet
     




 

