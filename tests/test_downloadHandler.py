import unittest
from unittest import mock
from src import downloadHandler as dh
from src import url
import os
 
from requests.exceptions import ConnectTimeout, ReadTimeout, Timeout
import ftplib
import paramiko
#python -m unittest discover -s ./tests -t ../

def removeFileBeforeTest(path):
    if(os.path.exists(path)):
        os.remove(path)


"""
Unit / Integration Test of Download Handler with URL object
"""

class TestDownloadHandler(unittest.TestCase):
    def __init__(self,*args, **kwargs):

        # Set-up
        super().__init__(*args, **kwargs) 
 
        self.http = dh.DownloadHandler(url.URL("http://raw.githubusercontent.com/okfn/dataportals.org/master/data/portals.csv"))
        self.https = dh.DownloadHandler(url.URL("https://banner2.cleanpng.com/20180901/qoa/kisspng-computer-icons-hyperlink-favicon-url-shortening-po-ms-lianjie-svg-png-icon-free-download-331745-5b8ad9b3d25566.5256320315358263558615.jpg"))
        self.ftp = dh.DownloadHandler(url.URL("ftp://anonymous:password@speedtest.tele2.net/1KB.zip"))
        self.sftp = dh.DownloadHandler(url.URL("sftp://demo:password@test.rebex.net/pub/example/WinFormClientSmall.png"))     
        self.scp = dh.DownloadHandler(url.URL("scp://root@host:/root/ids/rules.tar.gz"))
   
    
    """
    Mock Download Trigger Fail Case  
    """  
    def test_HTTPSFailure(self):     
        with mock.patch('src.downloadHandler.DownloadHandler', autospec=True) as mockHttpDownload:             
            mockHttpDownload.side_effect = Exception("test")      
            result = mockHttpDownload.downloadHTTPS()            
            self.assertTrue(result,-1)          

    def test_FTPFailure(self):     
        with mock.patch('src.downloadHandler.DownloadHandler') as mockFtpDownload:
            mockFtpDownload.side_effect = Exception("test")             
            result = mockFtpDownload.downloadFTP()       
            self.assertTrue(result,-1)

    def test_SFTPFailure(self):     
        with mock.patch('src.downloadHandler.DownloadHandler') as mockSftpDownload:
            mockSftpDownload.side_effect = Exception("test")             
            result = mockSftpDownload.downloadSFTP()       
            self.assertTrue(result,-1)   

    # Test file removal
    def test_removePath(self):
        self.http.removePath()
        self.assertFalse(os.path.exists(self.http.downloadPath))

     
    # Authentication error test   
    def test_FTP_AuthFailure(self): 
        ftpFail = dh.DownloadHandler(url.URL("ftp://anonymousA:password@speedtest.tele2.net/1KB.zip"))
        self.assertRaises(dh.AuthException, ftpFail.startDownload)

    def test_SFTP_AuthFailure(self): 
        sftpFail = dh.DownloadHandler(url.URL("sftp://demoTest:passwords@test.rebex.net/pub/example/WinFormClientSmall.png"))
        self.assertRaises(dh.AuthException, sftpFail.startDownload)
         
"""
Integrated Tests to test file download functions
"""
             
class TestDownloadHandler2(TestDownloadHandler):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs) 
        
    def test_unsuppotedProtocol(self):
        self.assertRaises(dh.ProtocolNotSupportedException, self.scp.startDownload)
    
    # HTTP download test
    def test_httpDownloadSuccess(self):
        # Remove file if present before testing      
        removeFileBeforeTest(self.http.downloadPath)

        code = self.http.startDownload()
        self.assertEqual(code,0)
        self.assertTrue(os.path.exists(self.http.downloadPath))
                 

    # HTTPS download test
    def test_httpsDownloadSuccess(self):
        # Remove file if present before testing       
        removeFileBeforeTest(self.https.downloadPath)

        code = self.https.startDownload()
        self.assertEqual(code,0)        
        self.assertTrue(os.path.exists(self.https.downloadPath))
 

    # FTP download test
    def test_ftpDownloadSuccess(self):
        # Remove file if present before testing 
        removeFileBeforeTest(self.ftp.downloadPath)     
               
        code = self.ftp.startDownload()
        self.assertEqual(code,0)
        
        self.assertTrue(os.path.exists(self.ftp.downloadPath))
 
         
    # SFTP download test
    def test_sftpDownloadSuccess(self):
        # Remove file if present before testing     
        removeFileBeforeTest(self.sftp.downloadPath)

        code = self.sftp.startDownload()
        self.assertEqual(code,0)
        self.assertTrue(os.path.exists(self.sftp.downloadPath))
        
  
            

 