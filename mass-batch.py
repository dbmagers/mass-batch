import os
from time import sleep
from re import sub
import yaml
import argparse
from mako.template import Template
import logging
import subprocess

# argparser
parser = argparse.ArgumentParser(description= "Submit all the jobs")
parser.add_argument('-y', '--yaml', help = "Location of yaml file that stores all directories to be created.\n(Default: data.yaml)", default='data.yaml')
parser.add_argument('-m', '--mako', help = "Location of mako template input file.\n(Default: input.yaml)", default='input.tmpl')
parser.add_argument('-p', '--pbs', help = "Location of pbs submission file", default='submit.sh')
parser.add_argument('-i', '--input', help = "Name of input file to create in each bottom directory.\n(Default: input.dat)", default='input.dat')
parser.add_argument('-t', '--time', help = "Time between subsequent submissions.\n(Default: 1 second)", default=1, type=float)
parser.add_argument('-d', '--debug', help = "Write all files but do not submit files to be run", action='store_true')
args = vars(parser.parse_args())

# logging file config
logging.basicConfig(filename="log.txt", level = logging.INFO,format="%(asctime)s %(message)s")

# load yaml data file
stream = open(args['yaml'],'r')
yamldata = yaml.safe_load(stream)
stream.close()
yamldata_rev = list(reversed(yamldata))

# set root folder for created file tree
root = 'calcs'
cwd = os.getcwd()
logging.info("mass-batch script began at "+cwd)

# recursive function to walk folder tree and create each file from template
def recurse(yamldata_rev, num_level, pwd):
    # create child pwd folder by walkinng through yamldata data
    if num_level >= 1:
        temp = num_level
        for i in yamldata_rev[num_level-1]: # i is a dict
            if temp != num_level:
                pwd = pwd.split('/')[:-1]
                pwd = '/'.join(pwd)
            pwd += "/"+i
            temp -= 1
            recurse(yamldata_rev, num_level - 1, pwd)
    # if at bottom child folder, make input file from template and submit to queue
    else:
        #LOGGING DATA ADDITION; instead of printing directories on screen, log them into "log.txt" file
        logging.info(pwd)
        # check if folder already exists, then make it
        if not os.path.exists(pwd): 
            os.makedirs(pwd)
        # check if input.dat already exists, else make it
        if not os.path.exists(pwd +"/"+args["input"]):
            mytemplate = Template(filename = args["mako"])
            # get names of parent folders in pwd and remove root folder name from array
            directories = pwd.split("/")[1:]

            # build dict of var#:values to render with mako into template file
            num_directories = len(directories)
            replace_dict = {}
            for j in range(0,num_directories):
                replace_dict['var'+str(j+1)] = yamldata[j][directories[j]]
            file_contents = mytemplate.render(**replace_dict).replace('\r','')

            # make file in bottom directory               
            file1 = open(pwd+"/"+args["input"], "w")
            file1.write(file_contents)
            file1.close()
            # change to bottom child directory in order to run submit script then change back
            if args['debug'] == False:
                os.chdir(pwd)
                os.system("qsub "+cwd+'/'+args["pbs"])
                os.chdir(cwd)
                logging.info("job submitted at "+pwd)
                sleep(args["time"])
            
        #"input data will go into log"
        else:
            logging.info("input.dat already exists at "+pwd+"/input.dat") 
            #print("input.dat already exists at "+pwd+"/input.dat")

def main():
    recurse(yamldata_rev, len(yamldata_rev), root)

if __name__ == "__main__":
    main()

