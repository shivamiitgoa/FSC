# FSC : Function Specific Compiler

## About
FSC generates the assembly code for each functions present in the source code. It uses gcc to compile source code to object files and radare2 to extract the assembly codes for each function. 

### Dependencies
* Radare2
* Ctags
* r2pipe in python

### Usage
* `python3 main.py input_source_file source_folder`
* Here, input_source_file is the input file whose functions are to be decompiled.
* Here, source folder is the folder in which we can find all the headers used in the input source file.