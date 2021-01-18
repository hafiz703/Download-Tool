import sys, os
path = os.path.dirname(__file__)
# print("path",path)
path = os.path.join(path, '../src')
if path not in sys.path:
    sys.path.append(path)