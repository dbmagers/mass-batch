import os
from re import sub
import yaml
import argparse
from mako.template import Template
import logging
import subprocess

# 1. understand mako libray, find examples
# put txt files with same format but different values in the bottom folder of Magers

#use yaml to sort our folders
#implement arg parse

# part added 6/1/2022 for yaml argparser
parser = argparse.ArgumentParser(description= "Submit all the jobs")

parser.add_argument('-y', '--yaml', help = "Location of yaml file that stores all directories to be created.\n(Default: data.yaml)", default='data.yaml')
parser.add_argument('-m', '--mako', help = "Location of mako template input file.\n(Default: input.yaml)", default='input.tmpl')
parser.add_argument('-p', '--pbs', help = "Location of pbs submission file", default='submit.sh')
# parser.add_argument('-d', '--debug', help = "write all files but do not submit files to be run", action=" ")

args = vars(parser.parse_args())

##end of mako argarser

##part added for logging files created 7/2/2022
logging.basicConfig(filename="log.txt", level = logging.INFO,format="%(asctime)s %(message)s")
## use of this logg import comes in LINE 66

# load needed files
#yaml_string = """
#- {'a':'e','b':'f'}
#- {'m':'r','n':'s'}
#"""
#yamldata = yaml.safe_load(yaml_string)
stream = open(args['yaml'],'r')
yamldata = yaml.safe_load(stream)
stream.close()

root = 'calcs'
yamldata_rev = list(reversed(yamldata))

def recurse(yamldata_rev, num_level, pwd):
    if num_level >= 1:
        temp = num_level
        for i in yamldata_rev[num_level-1]: # i is a dict
            if temp != num_level:
                pwd = pwd.split('/')[:-1]
                pwd = '/'.join(pwd)
            pwd += "/"+i
            temp -= 1
            recurse(yamldata_rev, num_level - 1, pwd)
    else:
        #LOGGING DATA ADDITION; instead of printing directories on screen, log them into "log.txt" file
        logging.info(pwd)
        # check if folder already exists, then make it
        if not os.path.exists(pwd): 
            os.makedirs(pwd)
        # check if input.dat already exists, else make it
        if not os.path.exists(pwd +"/input.dat"):
            mytemplate = Template(filename = args["mako"])
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
            
        #"input data will go into log"
        else:
            logging.info("input.dat already exists at "+pwd+"/input.dat") 
            #print("input.dat already exists at "+pwd+"/input.dat")

recurse(yamldata_rev, len(yamldata_rev), root)
