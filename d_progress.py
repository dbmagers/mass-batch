import os
import yaml
import argparse

#use yaml to sort our folders
#implement arc parse

yaml_string = """
- [{'a':'e'},{'b':'f'}]
- [{'m':'r'},{'n':'s'}]
"""

#stream = open('data.yaml','r')
#yamldata = yaml.safe_load(stream)
#stream.close()
yamldata = yaml.safe_load(yaml_string)

#print(yamldata)

var_1 = ['a','b','c','d']
var_2 = ['m','n','o']

root = 'Magers'

dict = {'a':'e'}

#last check, for a given dict key, give us the value associated
print(dict.items())
#print(yamldata[0][0].keys()[0])

try:
    for level1 in yamldata:
        for level2 in yamldata[level1]:
            pwd =(os.path.join(root,level1,level2.keys()))
            os.makedirs(pwd)
            file_name = "test.txt"
            file1 = open(pwd+"/input.dat", "w")
            file1.write("Chemistry and star stuffs?")
            file1.close()
    
except FileExistsError:
    print("file already exists")
