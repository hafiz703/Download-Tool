import requests 
from urllib.parse import urlparse
import os
import sys 
from time import time
from ftplib import FTP,error_perm,error_proto,error_reply,error_temp,socket
import paramiko
from tqdm import tqdm
import shutil 
from src.url import URL

# Base Class for Download Exceptions
class DownloadException(Exception):
    pass

# Raised when protocol not currently supported
class ProtocolNotSupportedException(DownloadException):
    def __init__(self, message):         
        super().__init__(message)

# Raised when connection to host unable to be established
class ConnectionException(DownloadException):
    def __init__(self, message):         
        super().__init__(message)

# Raised when credentials passed is incorrect
class AuthException(DownloadException):
    def __init__(self, message):         
        super().__init__(message)

# Raised when file not present in host
class FileNotFoundException(DownloadException):
    def __init__(self, message):         
        super().__init__(message)

# Raised during failure while downloading
class DownloadErrorException(DownloadException):
     def __init__(self, message):         
        super().__init__(message)
 
     

class DownloadHandler:
    def __init__(self,URLObject, destination="./", block_size = 1024, overwrite=True):

        self.__supportedProtocols = {
            "http":self.downloadHTTPS,
            "https":self.downloadHTTPS,
            "ftp":self.downloadFTP,
            "sftp":self.downloadSFTP
        }
        
        self.url = URLObject  
        self.destination = destination    
        self.overwrite = overwrite
        self.downloadPath = os.path.join(self.destination,self.url.filename)
        self.block_size = block_size   
           
    # Remove file if present
    def removePath(self):                 
        if(os.path.exists(self.downloadPath)):
            print("Removing partial file {}".format(self.downloadPath))
            os.remove(self.downloadPath)
 

    # Abstract method to start download 
    def startDownload(self): 
        # Skip downloading of overwrite set to False
        if(os.path.exists(self.downloadPath) and not self.overwrite):
            print("File present in {}, skipping download".format(self.downloadPath))
            return -1

        # Skip downloading if protocol not in supported 
        if(self.url.protocol not in self.__supportedProtocols):
            raise ProtocolNotSupportedException("{} Protocol not supported for {}".format(self.url.protocol,self.url))

        download = self.__supportedProtocols[self.url.protocol]
        
        # Start Download
        resultCode = download()

        
        if(resultCode == 0):
            print("\nFile {} downloaded in {}".format(self.url.filename,self.downloadPath))
        else:
            print("\nError in downloading {}".format(self.url.filename))
        return resultCode
    

    def downloadHTTPS(self):
        """
        HTTP/HTTPS Download handler
        """       
         
        try:
            r = requests.get(self.url,stream = True)     
            if(r.status_code != 200):
                raise ConnectionException("Connection error for {}".format(self.url))

            # Get file size
            file_size = r.headers.get('content-length')   
            if file_size is None: file_size = 0     
            file_size = int(file_size)  
             
            pbar = tqdm(total=file_size)           

            # Start downloading 
            with open(self.downloadPath, 'wb') as f:                 
                for block in r.iter_content(chunk_size=self.block_size):
                    if block:                        
                        f.write(block) 
                        pbar.update(len(block))

        except Exception as e:
            print(e)
            # ERROR - delete file   
            self.removePath()
            raise DownloadErrorException("Error while downloading {}".format(self.url))
             

        return 0
  
    def downloadFTP(self):
        """
        FTP Download handler
        """   
        ftp = None
        # Connect to FTP host
        try:
            ftp = FTP(self.url.host,timeout=10)      

        except (socket.timeout,error_perm,error_temp) as e :                   
            raise ConnectionException("{}\nConnection error for {}".format(e,self.url))  
             
        # Login via credentials 
        try: 
            ftp.login(user=self.url.username, passwd=self.url.password)

        except error_perm as e:     
            ftp.quit()       
            raise AuthException("{}\nAuthentication error for {}".format(e,self.url))
        
        # Get File Size
        try:
            file_size = ftp.size(self.url.remotePath)
            local_file = open(self.downloadPath, 'wb')         
            pbar = tqdm(total=file_size)        
         
        except error_perm as e:
            ftp.quit()       
            raise FileNotFoundException("{}\nUnable to retrieve file information for {}".format(e,self.url))

        # Callback function for progress bar update            
        def file_write(data):
            local_file.write(data)             
            nonlocal pbar
            pbar.update(len(data))         

        # Start download
        try:
            ftp.retrbinary('RETR '+self.url.filename, file_write, self.block_size)
             
        except (error_perm,error_proto,error_reply,error_temp) as e:            
            ftp.quit()
            local_file.close()
            #ERROR - Remove File
            self.removePath()
            raise DownloadErrorException("{}\nError while downloading {}".format(e,self.url))

        if(ftp is not None): 
            ftp.quit()
            local_file.close()
        return 0
         

    def downloadSFTP(self):  
        """
        SFTP Download handler 
        """          
        port = 22  
        transport = None

        # Connect to SFTP host
        try:
            transport = paramiko.Transport((self.url.host, port))

        except (socket.timeout,error_perm,error_temp) as e :                   
            raise ConnectionException("{}\nConnection error for {}".format(e,self.url))   
        

        # Authenticate via credentials        
        try:
            transport.connect(None, self.url.username, self.url.password)   

        except paramiko.ssh_exception.AuthenticationException as e:             
            raise AuthException("{}\nAuthentication error for {}".format(e,self.url.url))
  
        sftp = paramiko.SFTPClient.from_transport(transport) 

        # Get File Size     
        try:
            file_size = sftp.stat(self.url.remotePath).st_size
        except:
            raise FileNotFoundException("{}\nUnable to retrieve file information for {}".format(e,self.url))
        
        # Start Download
        try:
            pbar = tqdm(total=file_size)
            chunks = [(offset, self.block_size) for offset in range(0, file_size, self.block_size)]
            with sftp.open(self.url.remotePath, "rb") as infile:
                with open(self.downloadPath, "wb") as outfile:
                    for chunk in infile.readv(chunks):
                        outfile.write(chunk)
                        pbar.update(len(chunk))
                        
        except Exception as e:             
            self.removePath()
            raise DownloadErrorException("{}\nError while downloading {}".format(e,self.url))
        return 0
         
   

 


