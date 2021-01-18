import unittest
from src import input
class TestInput(unittest.TestCase):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sampleRows = 4

    def test_readFile(self):        
        readFile = input.readFile
        # File not exist
        self.assertRaises(FileNotFoundError, readFile, "sampleInputs/nothing.txt")

        # File exists, but format unsupported
        self.assertRaises(input.FileFormatException, readFile, "sampleInputs/sample.json")

        # Empty File
        self.assertRaises(Exception, readFile, "sampleInputs/sampleNone.txt")

    # Test if number of rows retrieved in txt file is correct 
    def test_readTxtFile(self):
        self.assertEqual(len(input.readTxtFile("sampleInputs/sampleInput.txt")),self.sampleRows)

    # Test if number of rows retrieved in csv file is correct
    def test_readCsvFile(self):
        self.assertEqual(len(input.readCsvFile("sampleInputs/sampleInput1.csv")),self.sampleRows)
        self.assertEqual(len(input.readCsvFile("sampleInputs/sampleInput2.csv")),self.sampleRows)
        self.assertSetEqual(input.readCsvFile("sampleInputs/sampleInput2.csv"), input.readCsvFile("sampleInputs/sampleInput1.csv"))

        


if __name__ == '__main__':
    unittest.main()
    #python -m unittest tests.input_test