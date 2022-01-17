# mass-batch

The goal is create a script to create a tree hierarchy of nested folders based on user defined variables (perhaps with a yaml file).  From there a template file will be copied to the bottom child directory and altered based on the names of the nested folders (perhaps with mako templates).  The script will optionally allow submission to a PBS job queue.

### Example

User defined variables

`variable1 = ['a', 'b', 'c']`

`variable2 = ['m', 'n', 'o']`

`tfile = input.tmpl`

`sfile = pbs.sh`

Three folders would be created named 'a', 'b', and 'c'.  Under each of these three more folders would be created named 'm', 'n', and 'o'.  The tfile.tmpl file would be copied 9 times into the bottom child directories.

### Things to check

- check if folder already exists, if so then continue. skip if on bottom child directory
- see if variable names having matching place holder in .tmpl file
- use argparse? for options including whether to not run submission command
- print summary at end: how many .tmpl files copied, how many skipped, etc. 
