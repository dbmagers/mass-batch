import os
import yaml
import argparse


#use yaml to sort our folders
#implement arc parse

var1_yaml = """
- 'a'
' 'b'
- 'c'
- 'd'
"""

var = yaml.safe_load(var1_yaml)

var_1 = ['a','b','c','d']

var1_yam2 = """
- 'm'
' 'n'
- 'o'
"""

var_2 = ['m','n','o']

root = '/Magers'


try:

    for folders in var_1:
        for nestedfolder in var_2:
            pwd =(os.path.join(root,folders,nestedfolder))
            os.makedirs(pwd)
            file_name = "test.txt"
            file1 = open(pwd+"/input.dat", "w")
            file1.write("Chemistry and star stuffs?")
            file1.close()
    
except FileExistsError:
    print("file already exists")