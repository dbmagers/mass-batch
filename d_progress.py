import os
import yaml
import argparse
from mako.template import Template

# 1. understand mako libray, find examples
# put txt files with same format but different values in the bottom folder of Magers

#use yaml to sort our folders
#implement arc parse

yaml_string = """
- [{'a':'e','b':'f'}]
- [{'m':'r','n':'s'}]
"""

#stream = open('data.yaml','r')
#yamldata = yaml.safe_load(stream)
#stream.close()
yamldata = yaml.safe_load(yaml_string)
#print(yamldata)

root = 'Magers'
yamldata.reverse()

def recurse(yamldata, num_level, pwd):
    if num_level >= 1:
        temp = num_level
        for i in yamldata[num_level-1][0]: # i is a dict
            if temp != num_level:
                pwd = pwd[:-2]
            #pwd += "/"+list(i.keys())[0]
            pwd += "/"+i
            temp -= 1
            recurse(yamldata, num_level - 1, pwd)
    else:
        print(pwd)
        # check if folder already exists, then make it
        if not os.path.exists(pwd): os.makedirs(pwd)
        # check if input.dat already exists, else make it
        if not os.path.exists(pwd+"/input.dat"):
            mytemplate = Template(filename = 'input.tmpl')
            folders = pwd.split("/")
            print(folders)
            # use of enumerated for loops to try and index and get the key

#            for j in folders[1:]:
#                return None 

# how do we index over the variable number of mako variables ${blah}?
            stuff = mytemplate.render(var1='blah')
               
            file1 = open(pwd+"/input.dat", "w")
            file1.write(stuff)
            file1.close()
        else: print("input.dat already exists at "+pwd+"/input.dat")

recurse(yamldata, len(yamldata), root)

