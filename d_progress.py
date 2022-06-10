import os
import yaml
import argparse
from mako.template import Template

# 1. understand mako libray, find examples
# put txt files with same format but different values in the bottom folder of Magers

#use yaml to sort our folders
#implement arg parse

yaml_string = """
- {'a':'e','b':'f'}
- {'m':'r','n':'s'}
"""

#stream = open('data.yaml','r')
#yamldata = yaml.safe_load(stream)
#stream.close()
yamldata = yaml.safe_load(yaml_string)
#print(yamldata)

#new part added 6/1/2022 for argparser
parser = argparse.ArgumentParser(description= "Show yaml file locations")

subparsers = parser.add_argument('-y', '--yaml', help = " location of yaml file that stores all directories to be created",
                                action=" ")
subparsers = parser.add_argument('-m', '--mako', help = " location of mako template file",
                                action=" ")
#subparsers = parser.add_argument('-p', '--pbs', help = " location of pbs submission file",
                                action=" ")
#subparsers = parser.add_argument('-d', '--debug', help = "write all files but do not submit files to be run",
                                action=" ")                                                                                                
#end of argparse part, don't know what the action should be but i assume all other
#argparse command line functions will follow the format above this comment

root = 'Magers'
yamldata_rev = list(reversed(yamldata))

def recurse(yamldata_rev, num_level, pwd):
    if num_level >= 1:
        temp = num_level
        for i in yamldata_rev[num_level-1]: # i is a dict
            if temp != num_level:
                pwd = pwd[:-2]
            pwd += "/"+i
            temp -= 1
            recurse(yamldata_rev, num_level - 1, pwd)
    else:
        print(pwd)
        # check if folder already exists, then make it
        if not os.path.exists(pwd): os.makedirs(pwd)
        # check if input.dat already exists, else make it
        if not os.path.exists(pwd+"/input.dat"):
            mytemplate = Template(filename = 'input.tmpl')
            # get names of parent folders in pwd and remove root folder name from array
            directories = pwd.split("/")[1:]

            # build dict of var#:values to render with mako into template file
            num_directories = len(directories)
            replace_dict = {}
            for j in range(0,num_directories):
                replace_dict['var'+str(j+1)] = yamldata[j][directories[j]]
            file_contents = mytemplate.render(**replace_dict)

            # make file in bottom directory               
            file1 = open(pwd+"/input.dat", "w")
            file1.write(file_contents)
            file1.close()
        else: print("input.dat already exists at "+pwd+"/input.dat")

recurse(yamldata_rev, len(yamldata_rev), root)
