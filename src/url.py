"""
Wrapper Object for URLs
"""
 
from urllib.parse import urlparse
import os
import sys 

# Raised when filename not present in url
class FileNotFoundException(Exception):
    def __init__(self, message):         
        super().__init__(message)


class URL:
    def __init__(self,url=None):
        """
        Parameters
            url - (string) string consisting of 1 URL
        """
        if(url is not None):
            self.url = url       
            self.protocol = self.getProtocolFromUrl(url)        
            self.filename = self.getFileNameFromUrl(url)
            self.host,self.username,self.password = self.hostUserNameFromUrl(url)  
            self.remotePath = self.remotePathFromUrl(url)
         
    def __str__(self):
        return self.url      
       
    def getProtocolFromUrl(self,url):
        """
        Parse protocol from URL
        """ 
        protocol = urlparse(url).scheme
        return protocol

    def hostUserNameFromUrl(self,url):
        """
        Parse hostname, username, password from URL
        """
        parsed = urlparse(url)
        host = parsed.hostname        
        user = parsed.username or ""
        pw = parsed.password or ""

        return host,user,pw


    def remotePathFromUrl(self,url):
        """
        Parse Remote Path from URL
        """
        return urlparse(url).path


    def getFileNameFromUrl(self,url):
        """
        Parse Filename from URL
        """
        a = urlparse(url)               
        filename = os.path.basename(a.path) 
             
        if(len(filename) == 0):
            raise FileNotFoundException("No File found for download")
        return filename

 

 
 

