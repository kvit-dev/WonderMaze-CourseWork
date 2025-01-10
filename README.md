# WonderMaze Game

## Requirements
Please ensure the following components are installed:

* Python 3.11.0 or higher (CPython)
* MSYS2 (for .dll libraries)
* Virtualenv

## Setting Up MSYS2
MSYS2 is a collection of tools and libraries providing you with an easy-to-use environment for building, installing and running native Windows software.

You can download the installer here: [https://www.msys2.org/]

***After installation, follow all the steps listed on the website***
- PATH to MSYS2: `C:\msys64\ucrt64`
  

To activate the `ucrt64` you need to run these commands in the MSYS2 Shell:
```bash
$ pacman -Syu
$ pacman -S base-devel python python-pip
```

## Generating a dll library
To generate a dll library use: 
```bash
g++ -shared -o maze_lib.dll generator.cpp
```
You should compile this lib everytime you change the .cpp code

## Run
To run the application you need to run _main.py_
