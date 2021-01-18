import unittest
from unittest import mock 
from src import run
import shutil
import os
 
class TestRunArgs(unittest.TestCase):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs) 
        self.runPath = "src/run.py" 
        self.filePath = "/test/urls.txt"
        self.dir = "/tmp/"

    def test_ArgsParser(self):
        testArgs1 = [self.runPath,self.filePath,'-d', self.dir]
        testArgs2 = [self.runPath, self.filePath, '-d', self.dir, '-o', '-bs', "512"]
        testArgs3 = [self.runPath, self.filePath, '-d', self.dir, '-o', '-bs', "True"]
        
        # Valid params/args
        with mock.patch.object(run.sys, "argv", testArgs1):          
            args = run.parseArgs()
            self.assertEqual(vars(args),{'urlPath': self.filePath, 'd': self.dir, 'o': True, 'bs': 1024})

        # Valid params/args
        with mock.patch.object(run.sys, "argv", testArgs2):          
            args = run.parseArgs()
            self.assertEqual(vars(args),{'urlPath': self.filePath, 'd': self.dir, 'o': False, 'bs': 512})

        # Invalid params/args
        with mock.patch.object(run.sys, "argv", testArgs3):    
            with self.assertRaises(SystemExit) as cm:      
                args = run.parseArgs()
                 

            self.assertEqual(cm.exception.code, 2)

    def test_DirectoryValidator(self):

        # Valid directory
        code = run.validateDirectories("sampleInputs/sampleInput.txt","./")
        self.assertEqual(code, 0)

        # Invalid directories            
        with self.assertRaises(SystemExit) as cm:      
            run.validateDirectories(self.filePath,self.dir)
            self.assertEqual(cm.exception.code, 2)

class TestRunMain(unittest.TestCase):
    
    def __init__(self,*args, **kwargs):
        # Test object to recreate command line argument inputs
        class MockArgs:
            def __init__(self,urlPath,d,o,bs):
                self.urlPath = urlPath
                self.d = d
                self.o = o
                self.bs = bs

        super().__init__(*args, **kwargs)     

        # Recreate existing directory
        self.DIR = "tests/sampleDownloads"
        try:
            shutil.rmtree(self.DIR)
        except:
            pass
        os.mkdir(self.DIR)  

        self.args =  MockArgs("sampleInputs/sampleInput2.csv",self.DIR, True, 1024)

    # Main system test
    def test_main(self):
        filesToDownload, totalDownloaded, errorList = run.main(self.args,getReturn=True)
        self.assertEqual(len(os.listdir(self.DIR)), totalDownloaded)
        self.assertEqual(len(errorList), filesToDownload-totalDownloaded)


        




        
             

      