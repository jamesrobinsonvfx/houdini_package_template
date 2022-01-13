#!/usr/bin/env python
"""Rename Package

Since this repo was likely created using GitHub's Template Repository
feature, it's assumed that the name of the repo is to be the name of
the package. If you wanted to call it something else, you can provide
a second argument when running the script (see below).

Replace all references to {% package_name %} and {% Package Title %}
with the user-specified name of this package.

Written in Python to be more cross-platform compatible.

Run with
```
./initialize.py "My Cool Package" [mycoolpackage]
```
or
```
python initialize.py "My Cool Package" [mycoolpackage]
```

Author: James Robinson
Date: 25 September 2021
"""
import fnmatch
import os
import re
import sys

# Python 2/3 compatibility
try:
    input = raw_input
except NameError:
    pass

TEMPLATE_NAME = "houdini_package_template"


class TokenSwapper():
    """Sanitizes inputs and helps search & replace."""

    def __init__(self, name, title):
        """Setup this instance of :class:`.TokenSwapper`.

        :param name: Short name of the package, no spaces
        :type name: str
        :param title: Title for the package
        :type title: str
        """
        self.name = name
        self.title = title

    @property
    def name(self):
        """Short name for the package. Preferable lowercase, no spaces.

        :param new_name: Shortname for the package, like `mypackage`
        :type new_name: str
        """
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name.rstrip().replace(" ", "_")

    @property
    def title(self):
        """Nice title for the package. The one most people will see.

        :param new_title: Title string. Should be pretty.
        :type new_title: str
        """
        return self._title

    @title.setter
    def title(self, new_title):
        self._title = " ".join(new_title.rstrip().split())

    def token_map(self):
        """Pair up search strings with replacement strings.

        :return: Search/Replace dictionary
        :rtype: dict
        """
        return {
            "Package Title": self.title,
            "package_name": self.name,
            "PACKAGE_NAME_UPPER": self.name.upper()
        }

    def replace_in_line(self, line):
        """Replace tokens found a line with the user-specified strings.

        :param line: Line to search
        :type line: str
        :return: Replaced line
        :rtype: str
        """
        for token, repl in self.token_map().items():
            line = re.sub(r"{{%\s?{0}\s?%}}".format(token), repl, line)
        return line


def rename(abspath, package_name):
    """Rename a file or directory if it matches a pattern.

    :param root: Parent directory. Likely from `os.walk`
    :type root: str
    :param nodename: File or Directory name
    :type nodename: str
    :param package_name: User-specified shortname for the package
    :type package_name: str
    """
    root = os.path.dirname(abspath)
    nodename = os.path.basename(abspath)
    if fnmatch.fnmatch(nodename, "*{0}*".format(TEMPLATE_NAME)):
        new_nodename = nodename.replace(TEMPLATE_NAME, package_name)
        print("Renaming {0} to {1}".format(abspath, new_nodename))
        os.rename(abspath, os.path.join(root, new_nodename))


def skip_files(root):
    """Get a list of filenames to skip.

    :param root: Root directory of the package template
    :type root: str
    """
    # We can use .gitattributes as a quick starting point
    gitattributes = os.path.join(root, ".gitattributes")
    fnames = []
    with open(gitattributes, "r") as file_:
        for line in file_.readlines():
            fnames.append(line.split()[0])
    fnames.extend([dir_ for dir_ in os.listdir(root) if dir_[0] == "."])
    return fnames


def main():
    """Entry point for cli."""
    package_name = ""
    package_title = ""
    name_guess = os.path.basename(os.getcwd())
    title_guess = re.sub(r"[-_]", " ", name_guess).title()

    # Use commandline args if supplied
    if len(sys.argv) > 1:
        package_title = sys.argv[1]
        try:
            package_name = sys.argv[2]
        except IndexError:
            pass
    # Otherwise, start a wizard
    else:
        print(
            "Setting up a new package from template\n"
            "Leave input blank and press enter to use what's in the [brackets]"
        )
        package_name = input("Package name [{0}]: ".format(name_guess))
        package_title = input("Package Title [{0}]: ".format(title_guess))

    # Use suggestion if no input supplied
    if not package_name:
        package_name = name_guess
    if not package_title:
        package_title = title_guess

    # Run it
    skip = skip_files(os.getcwd())
    swapper = TokenSwapper(package_name, package_title)

    # Get a list of all files and dirs
    all_files = []
    all_dirs = []
    for root, dirs, files in os.walk(os.getcwd(), topdown=True):
        # Skip dotfiles
        dirs[:] = [dir_ for dir_ in dirs if not dir_ in skip]
        files = [file_ for file_ in files if not file_ in skip]

        for fname in files:
            all_files.append(os.path.join(root, fname))

        for dname in dirs:
            all_dirs.append(os.path.join(root, dname))

    for fname in set(all_files):
        # Copy current contents
        with open(fname, "r") as file_:
            content = file_.readlines()

        # Update the template line-by-line
        for i, line in enumerate(content):
            content[i] = swapper.replace_in_line(line)

        # Re-write the file
        with open(fname, "w") as file_:
            file_.writelines(content)

        # Rename the file if necessary
        rename(fname, package_name)

    # Rename any dirs and cleanup boilerplate READMEs
    for dname in set(all_dirs):
        if fnmatch.fnmatch(dname, "*houdini*/otls"):
            try:
                print("Removing placeholder at {0}/README.md".format(dname))
                os.remove(os.path.join(dname, "README.md"))
            except OSError:
                print("Unable to remove {0}/README.md".format(dname))
                pass
        rename(dname, package_name)
    print("\033[0;37;42m" + "Done." + "\033[0m")


if __name__ == "__main__":
    main()
