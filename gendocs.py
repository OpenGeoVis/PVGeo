# This script generates mkdocs friendly Markdown documentation from a python package.
# It is based on the the following blog post by Christian Medina
# https://medium.com/python-pandemonium/python-introspection-with-the-inspect-module-2c85d5aa5a48#.twcmlyack

import pydoc
import os
import sys

module_header = "# Package {} Documentation\n"
class_header = "## Class {}"
function_header = "### {}"


def getmarkdown(module):
    output = [module_header.format(module.__name__)]

    if module.__doc__:
        output.append(module.__doc__)

    output.extend(getclasses(module))
    return "\n".join((str(x) for x in output))

def getclasses(item):
    output = list()
    for cl in pydoc.inspect.getmembers(item, pydoc.inspect.isclass):

        if cl[0] != "__class__" and not cl[0].startswith("_"):
            # Consider anything that starts with _ private
            # and don't document it
            output.append(class_header.format(cl[0]))
            # Get the docstring
            output.append(pydoc.inspect.getdoc(cl[1]))
            # Get the functions
            output.extend(getfunctions(cl[1]))
            # Recurse into any subclasses
            output.extend(getclasses(cl[1]))
            output.append('\n')
    return output


def getfunctions(item):
    output = list()
    #print item
    for func in pydoc.inspect.getmembers(item, pydoc.inspect.ismethod):

        if func[0].startswith('_') and func[0] != '__init__':
            continue

        output.append(function_header.format(func[0].replace('_', '\\_')))

        # Get the signature
        output.append('```py\n')
        output.append('def %s%s\n' % (func[0], pydoc.inspect.formatargspec(*pydoc.inspect.getargspec(func[1]))))
        output.append('```\n')

        # get the docstring
        if pydoc.inspect.getdoc(func[1]):
            output.append('\n')
            output.append(pydoc.inspect.getdoc(func[1]))

        output.append('\n')
    return output

def generatedocs(module):
    try:
        sys.path.append(os.getcwd())
        # Attempt import
        mod = pydoc.safeimport(module)
        if mod is None:
            print("Module not found")

        # Module imported correctly, let's create the docs
        return getmarkdown(mod)
    except pydoc.ErrorDuringImport as e:
        print("Error while trying to import " + module)

if __name__ == '__main__':

    print(generatedocs(sys.argv[1]))
