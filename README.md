# Data-Downloader-Tool
Supports downloading files from given url. Supported download protocols are HTTP, HTTPS, FTP and SFTP.
Runs and tested on Python >=3.6.9. Input URLs given by .txt or .csv files. Makes use of external dependencies namely requests, ftplib and paramiko for handling downloads for HTTP/HTTPS, FTP and SFTP protocols respectively.


## Installation
Ensure Python 3 installed in system. 
 `cd DataSet-Downloader-Tool`
 `python setup.py install`

## Input
Add download URLs to txt or csv file as seen in either `sampleInputs/sampleInput.txt` or `sampleInputs/sampleInput.csv`

eg. 
```
http://raw.githubusercontent.com/okfn/dataportals.org/master/data/portals.csv
https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz
sftp://demo:password@test.rebex.net/pub/example/WinFormClientSmall.png
ftp://speedtest.tele2.net/1MB.zip
```

Note: hosts which require authentication has the username and password field formatted within the URL eg.
`ftp://<username>:<password>@hostname/file `

## Running the program

Usage: `downloadtool <input_path> -d <download_folder> -o -bs <block_size>` 
eg. : `downloadtool sampleInputs/sampleInput.txt -d tests/sampleDownloads -bs 2048`

Positional Arguments:
  path        Absolute/relative path to the URL list. Currently supports txt and csv file
              formats

Optional Arguments:
  -h, --help  show this help message and exit
  -d          Absolute/relative path to the download destination directory. Defaults to current directory
  -o          Add this flag to prevent overwrite existing files in directory
  -bs         Specify size for each block to be downloaded at one time (in bytes). Default set to 1024 bytes

## Running tests

In the root project folder,
`python -m unittest discover -s ./tests -t ../`


 

 
