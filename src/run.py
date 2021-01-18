#!/usr/bin/env python
"""
Driver code for dataset-downloader-tool
"""
from src.downloadHandler import DownloadHandler, DownloadException
from src.url import URL
from src.input import readFile,InputException
import threading
import glob
import os
import concurrent.futures 
import shutil 
import sys
import argparse
from time import time
 
# Get parsed arguments from user
def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('urlPath',
                       metavar='path',
                       type=str,
                       help='Path to the URL list. Currently supports txt and csv file formats')

    parser.add_argument('-d',                      
                       default="./",                        
                       help='Path to the download destination directory. Defaults to current directory')

    parser.add_argument('-o',                      
                    action='store_false',                     
                    help='Add this flag to prevent overwrite existing files in directory')

    parser.add_argument('-bs',                      
                default=1024,
                type=int,                 
                help='Specify block size in bytes) for download. Default set to 1024 bytes')

    return parser.parse_args()


def timer(f):
    """
    Util function to calculate total elapsed time taken for download
    Parameters:
        f - function to time
    """     
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print ("func:{} took: {:2.4f} sec".format(f.__name__, te-ts))
        return result
    return wrap
 
@timer 
def runAsync(urlSet,outputDirectory,ow,bs):
    """
    Handles downloads in an asynchronous manner
    Parameters:
        urlSet  - (set) set of URLs.
        outputDirectory - (string) local target directory where downloaded files are saved.
        ow - (bool) overwrite flag to allow/prevent files in outputDirectory to be overwritten. 
        bs - (int) size for each block to be downloaded at one time.
    """  
    filesToDownload = len(urlSet)
    totalDownloaded = 0
    errorList = []

    with concurrent.futures.ThreadPoolExecutor() as exec: 
        futures = []
        for urlString in urlSet:             
            dh = DownloadHandler(URL(urlString),outputDirectory,overwrite=ow,block_size=bs)
            futures.append(exec.submit(dh.startDownload))
           
            
        for future in concurrent.futures.as_completed(futures):
            try:
                if (future.result() == 0):
                    totalDownloaded +=1
                 
            except DownloadException as e:
                print("Error in download : {}".format(e))
                errorList.append(str(e))


    return filesToDownload,totalDownloaded,errorList

@timer
def runSync(urlSet,outputDirectory,ow,bs):
    """
    Handles downloads in a synchronous manner
    Parameters:
        urlSet  - (set) set of URLs.
        outputDirectory - (string) local target directory where downloaded files are saved.
        ow - (bool) overwrite flag to allow/prevent files in outputDirectory to be overwritten. 
        bs - (int) size for each block to be downloaded at one time.
    """ 
    filesToDownload = len(urlSet)
    totalDownloaded = 0
    errorList = []          
            
    for urlString in urlSet:         
        try:
            dh = DownloadHandler(URL(urlString),outputDirectory,overwrite=ow,block_size=bs)
            resultCode = dh.startDownload()
            if (resultCode == 0):
                totalDownloaded +=1
                
        except DownloadException as e:
            print("Error in download : {}".format(e))
            errorList.append(str(e))


    return filesToDownload,totalDownloaded,errorList
    
# Prints summary of download after 
def printSummary(inputPath,filesToDownload,totalDownloaded,errorList):    
    print("\nDOWNLOAD COMPLETED\n-- Total Unique URLs in {}: {}\n-- Total Downloaded: {} ".format(os.path.basename(inputPath),filesToDownload,totalDownloaded))
    if(len(errorList)>0):
        print("\nERROR SUMMARY")
        for err in errorList:
            print("\n--",err)

def validateDirectories(inpFile,saveDestDir):
    if(not(os.path.isfile(inpFile))):
        print('The file {} specified does not exist'.format(inpFile))
        sys.exit()

    if(not(os.path.isdir(saveDestDir))):
        print('The directory {} specified does not exist'.format(saveDestDir))
        sys.exit()
    return 0

def main(args=None,getReturn=None):
    if(args is None):
        args = parseArgs()
         
    # Positional arguments
    inputFilePath = args.urlPath    

    # Default arguments
    dir = args.d
    overWrite = args.o
    blockSize = args.bs    
    
    # Check if supplied directories are valid, else exit
    validateDirectories(inputFilePath,dir)

    # Read file into HashSet containing URLs
    try:
        urlSet = readFile(inputFilePath)
    except InputException as e:
        print(e)
        sys.exit()

    # Start Download
    filesToDownload,totalDownloaded, errorList = runAsync(urlSet,dir,overWrite,blockSize)
     
    # Print summary after all download completes
    printSummary(inputFilePath,filesToDownload,totalDownloaded,errorList)

    if(getReturn):
        return filesToDownload, totalDownloaded, errorList

if __name__ == "__main__":     
    main()