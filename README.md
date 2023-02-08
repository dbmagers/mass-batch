# mass-batch

This script is intended to streamline high throughput job submission to a queue such as PBS (portable batch system) common on many clusters.  The script was written with computational chemists in mind, but is general enough to have wider application.

The mass-batch.py script creates a tree hierarcy of nested folders based on user define variables (data.yaml).  Within each bottom, child directory a template file (input.tmpl using Mako library) will be copied and altered based on the names of the nested folders.  The script will optionally allow submission to a PBS job queue.

### Generalized Example
#### See below for detailed example

User defined variables

`variable1 = ['a', 'b', 'c']`

`variable2 = ['m', 'n', 'o']`

`tfile = input.tmpl`

`sfile = pbs.sh`

Three folders would be created named 'a', 'b', and 'c'.  Under each of these three more folders would be created named 'm', 'n', and 'o' for a total of 9 unique terminal paths.  The input.tmpl file would be copied 9 times into the bottom child directories with unique substitutions.

### For the computational chemist

An application would be if you would like to test different basis sets and dft functionals for a given calculation.  This script could automate submitting every possible combination between 5 different functionals and 5 different basis sets within seconds (25 total jobs).  Expanding this to other user-define variables in an input file, could be the molecular geometry, solvent, solvation model, bond distance, bond angle, etc.  Thousands of jobs could be submitted, all in unique folder paths, with one command line execution.

### User defined files to edit

- `data.yaml`
- `input.tmpl`
- `submit.sh`

`data.yaml` contains all the information for the names of the folders to create and the exact strings to insert into the input template file.  Each line of the file with the general format of `- {'key1':'value2', 'key2':'value2'}` defines another level of nested folders.  The dictionary of key-value pairs defines what the folders created will be named (keys) and the string to insert into the Mako template file (values).  For example, a `data.yaml` file could contain the following
```
---
- {'a':'A', 'b':'B'}
- {'m':'M', 'n':'N'}
```
Note that the `---` is required as the first line of `data.yaml`.  In this example the script will create two folders, `a` and `b`, under the top hierachy folder.  In each of these, two folders will be created named `m` and `n`.  In total there will be 2x2 = 4 total unique paths (`top/a/m`, `top/a/n`, `top/b/m`, and `top/b/n`).

In each of these bottom unique paths, the Mako template library is utilized with the `input.tmpl` file.  This file can contain almost (some special characters reserved in Mako that haven't been tested yet) text desired.  The user should define where in the file to insert the variables define in `data.yaml` with snippets with the format of `${var1}`.  See this example input.tmpl file
```
This is some text.
This will show the first variable: ${var1}
And here is the second : {$var2}
```
In this example, under the unique path of `top/a/m`, a input.dat file will be created with the following contents
```
This is some text.
This will show the first variable: A
And here is the second : M
```
Note that the template rendered the values from the dictionaries defined in the `data.yaml` file.  In this way 2x2 = 4 total unique input.dat files will be created in unique folder paths.

The submit.sh file can be whatever submit script file is required for the queue system of your desire.  The script will execute `qsub submit.sh` under each child directory.  The submission execution can be turned off with the `-d` flag on the command line which will only create the folders and create the templated input.dat files.

### mass-bath.py --help
```
usage: mass-batch.py [-h] [-y YAML] [-m MAKO] [-p PBS] [-i INPUT] [-t TIME] [-d]

Submit all the jobs

optional arguments:
  -h, --help                show this help message and exit
  -y YAML, --yaml YAML      Location of yaml file that stores all directories to be created. (Default: data.yaml)
  -m MAKO, --mako MAKO      Location of mako template input file. (Default: input.yaml)
  -p PBS, --pbs PBS         Location of pbs submission file
  -i INPUT, --input INPUT   Name of input file to create in each bottom directory. (Default: input.dat)
  -t TIME, --time TIME      Time between subsequent submissions. (Default: 1 second)
  -d, --debug               Write all files but do not submit files to be run
```
