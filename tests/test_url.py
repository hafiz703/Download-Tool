import unittest
from src import url
import os
 
class TestURL(unittest.TestCase):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs) 

        self.httpExample = "http://raw.githubusercontent.com/okfn/dataportals.org/master/data/portals.csv"
        self.cifarLarge = "https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz"
        self.longHttps = "https://banner2.cleanpng.com/20180901/qoa/kisspng-computer-icons-hyperlink-favicon-url-shortening-po-ms-lianjie-svg-png-icon-free-download-331745-5b8ad9b3d25566.5256320315358263558615.jpg"
        self.file = "http://my.file.com/file"
        self.ftp1 = "ftp://speedtest.tele2.net/1MB.zip" 
        self.ftp2 = "ftp://demo:password@speedtest.tele2.net/1MB.zip"  
        self.sftp1 = "sftp://and.also.this/ending"
        self.sftp2 = "sftp://test.rebex.net/pub/example/WinFormClientSmall.png"
        

        # Empty Test Object
        self.testObj = url.URL()
        
    # Protocol test
    def test_getProtocolFromUrl(self):
        # Proper Input
        self.assertEqual(self.testObj.getProtocolFromUrl(self.longHttps) , "https")  
    
    # Filename test
    def test_getFileNameFromUrl(self):
        # No file name / Not downloadable
        self.assertRaises(url.FileNotFoundException, self.testObj.getFileNameFromUrl  ,"https://www.google.com") 
         

        # Proper URLs with filename
        self.assertEqual(self.testObj.getFileNameFromUrl(self.httpExample) , "portals.csv")
        self.assertEqual(self.testObj.getFileNameFromUrl(self.cifarLarge) , "cifar-10-python.tar.gz") 
        self.assertEqual(self.testObj.getFileNameFromUrl(self.longHttps) , "kisspng-computer-icons-hyperlink-favicon-url-shortening-po-ms-lianjie-svg-png-icon-free-download-331745-5b8ad9b3d25566.5256320315358263558615.jpg")               
        self.assertEqual(self.testObj.getFileNameFromUrl(self.file) , "file") 
        self.assertEqual(self.testObj.getFileNameFromUrl(self.ftp1) , "1MB.zip") 
        self.assertEqual(self.testObj.getFileNameFromUrl(self.sftp1), "ending")
        self.assertEqual(self.testObj.getFileNameFromUrl(self.sftp2), "WinFormClientSmall.png")


    # Hostname test
    def test_hostName(self):
        # Test host names

        self.assertEqual(self.testObj.hostUserNameFromUrl(self.httpExample)[0] , "raw.githubusercontent.com")
        self.assertEqual(self.testObj.hostUserNameFromUrl(self.cifarLarge)[0] , "www.cs.toronto.edu") 
        self.assertEqual(self.testObj.hostUserNameFromUrl(self.longHttps)[0] , "banner2.cleanpng.com")               
        self.assertEqual(self.testObj.hostUserNameFromUrl(self.file)[0] , "my.file.com") 
        self.assertEqual(self.testObj.hostUserNameFromUrl(self.ftp1)[0] , "speedtest.tele2.net") 
        self.assertEqual(self.testObj.hostUserNameFromUrl(self.sftp1)[0], "and.also.this")
        self.assertEqual(self.testObj.hostUserNameFromUrl(self.sftp2)[0], "test.rebex.net")
        
        
    # Remote Path Name test
    def test_remotePathName(self):
        # Test remote path name

        self.assertEqual(self.testObj.remotePathFromUrl(self.httpExample), "/okfn/dataportals.org/master/data/portals.csv")
        self.assertEqual(self.testObj.remotePathFromUrl(self.cifarLarge), "/~kriz/cifar-10-python.tar.gz") 
        self.assertEqual(self.testObj.remotePathFromUrl(self.longHttps), "/20180901/qoa/kisspng-computer-icons-hyperlink-favicon-url-shortening-po-ms-lianjie-svg-png-icon-free-download-331745-5b8ad9b3d25566.5256320315358263558615.jpg")               
        self.assertEqual(self.testObj.remotePathFromUrl(self.file), "/file") 
        self.assertEqual(self.testObj.remotePathFromUrl(self.ftp1), "/1MB.zip") 
        self.assertEqual(self.testObj.remotePathFromUrl(self.sftp1), "/ending")
        self.assertEqual(self.testObj.remotePathFromUrl(self.sftp2), "/pub/example/WinFormClientSmall.png")

    # Username test
    def test_username(self):
        self.assertEqual(self.testObj.hostUserNameFromUrl(self.ftp1)[1], "") 
        self.assertEqual(self.testObj.hostUserNameFromUrl(self.ftp2)[1], "demo")

    # Password test
    def test_password(self):
        self.assertEqual(self.testObj.hostUserNameFromUrl(self.ftp1)[2], "") 
        self.assertEqual(self.testObj.hostUserNameFromUrl(self.ftp2)[2], "password")

         

 


 
 