#!/usr/bin/env python

"""
new.py: A simple utility to create files and folders based on templates.

With this program you can define template files, for instance a Python script
with some documentation or functions already defined, or a directory for a
LaTeX document. See the example directory for an example of a Python script.

Usage is quite simple, type::

    ./new.py

on the command line to get an overview of the current templates, and their
names. If you have for instance a Python script with the name ``python.py`` as
template name, you will get::

    ./new.py
    Available targets:
	Name	  	File / Dir
	----	  	----------
	python	->	python.py

The target name is automatically generated by stripping the extension of the
template file. So with the target name ``python``, you can use the following
command to copy the template to the current directory::

    ./new.py python

This will create a new file in the current directory named ``python.py``.
Finally, there is the option of naming the file in the current directory
differently::

    ./new.py python myscript.py

This will create the file ``myscript.py``, as a copy of the ``python.py``
template.

Author: G.J.J. van den Burg
Date: 2016-10-24
Copyright 2016, G.J.J. van den Burg.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>

"""

import os
import sys
import shutil

TEMPLATE_DIR = os.path.join(os.getenv('HOME'), ".newpy_templates/")

def list_targets():
    """Generate a list of templates and their names

    This function generates a dict of matches between target names and template
    files/directories. If the template target is a file, the name of the target
    is generated by stripping off the extension. If the target is a directory,
    a `/` is added to the name.

    Returns
    -------
    dict
        A mapping between target names and template files/dirs.

    """
    if not os.path.exists(TEMPLATE_DIR):
        os.mkdir(TEMPLATE_DIR)
    files = os.listdir(TEMPLATE_DIR)
    templates = {}
    for f in files:
        basefile = os.path.basename(f)
        target = os.path.splitext(basefile)[0]
        if os.path.isdir(os.path.join(TEMPLATE_DIR, f)):
            basefile += '/'
        templates[target] = basefile
    return templates


def show_targets():
    """Print a table of existing templates and their names
    """
    templates = list_targets()
    print("Name\t  \tFile / Dir")
    print("----\t  \t----------")
    for target in sorted(templates.keys()):
        basefile = templates[target]
        print("%s\t->\t%s" % (target, basefile))
    print("")


def create_template(target, name=None):
    """Create the actual output file from the template

    This function does the actual copying of the template file or directory. If
    the target is a directory, the entire directory will be copied recursively.
    If it is a file, the file will be copied. The name of the file or folder in
    the current directory is defined by the `name` input parameter. If the
    `name` parameter is `None`, the template name will be used.

    Parameters
    ----------
    target : str
        Name of the target to create

    name : str
        Name of the output file or directory, can be None.

    """
    templates = list_targets()
    targetpath = os.path.join(TEMPLATE_DIR, templates[target])
    here = os.getcwd()
    if name is None:
        if os.path.isdir(targetpath):
            shutil.copytree(targetpath, here)
        else:
            shutil.copy(targetpath, here)
    else:
        if os.path.isdir(targetpath):
            dest = os.path.join(here, name)
            shutil.copytree(targetpath, dest)
        else:
            dest = os.path.join(here, name)
            shutil.copy(targetpath, dest)


def fail(target=None):
    """Exit with an error message

    This command is used when incorrect arguments are supplied to the command
    line. Depending on what went wrong, a message is displayed to the user. A
    list of available targets is always printed.

    Parameters
    ----------
    target : str
        Name of the chosen target, used to print an error message when the
        target doesn't exist.

    Raises
    ------
    SystemExit
        Always raised in order to exit the program.

    """
    if target is None:
        print("Usage: ./new.py target [output_name]")
    else:
        print("Chosen target '%s' doesn't exist." % target)
    print("Available targets:")
    show_targets()
    raise SystemExit


def parse_args():
    """Parse the command line arguments

    Checks if the correct number of command line arguments is given to the
    command.

    Returns
    -------
        tuple : (str, str)
            Name of the target, outcome filename. If no output filename is
            desired, the second return argument is None.

    """
    if len(sys.argv) == 1 or len(sys.argv) > 3:
        fail()
    if len(sys.argv) == 2:
        target = sys.argv[1].strip().lower()
        filename = None
    else:
        target = sys.argv[1].strip().lower()
        filename = sys.argv[2].strip()
    if not target in list_targets():
        fail(target=target)
    return target, filename


if __name__ == '__main__':
    target, filename = parse_args()
    create_template(target, filename)
