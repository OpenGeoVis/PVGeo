#!/usr/bin/env python2

"""See blog for details: https://blog.kitware.com/easy-customization-of-the-paraview-python-programmable-filter-property-panel/

This code has been heavily modified by Bane Sullivan <banesullivan@gmail.com> for making customized filters in the geoscience data visualization. Credit does not go to Bane for this script but to the author of the above blog post.

Acknowledgements:
    Daan van Vugt <daanvanvugt@gmail.com> for file series implementation
        https://github.com/Exteris/paraview-python-file-reader
    Pat Marion (see blog post url above) for the foundation of this script
"""

__version__ = '0.6.2'

import os
import sys
import inspect
import textwrap
import xml.etree.ElementTree as ET


def escapeForXmlAttribute(s):

    # http://www.w3.org/TR/2000/WD-xml-c14n-20000119.html#charescaping
    # In character data and attribute values, the character information items "<" and "&" are represented by "&lt;" and "&amp;" respectively.
    # In attribute values, the double-quote character information item (") is represented by "&quot;".
    # In attribute values, the character information items TAB (#x9), newline (#xA), and carriage-return (#xD) are represented by "&#x9;", "&#xA;", and "&#xD;" respectively.

    s = s.replace('&', '&amp;') # Must be done first!
    s = s.replace('<', '&lt;')
    s = s.replace('>', '&gt;')
    s = s.replace('"', '&quot;')
    s = s.replace('\r', '&#xD;')
    s = s.replace('\n', '&#xA;')
    s = s.replace('\t', '&#x9;')
    return s



def getScriptPropertiesXml(info):

    e = escapeForXmlAttribute

    requestData = e(info['RequestData'])
    requestInformation = e(info['RequestInformation'])
    requestUpdateExtent = e(info['RequestUpdateExtent'])

    if requestData:
        requestData = '''
      <StringVectorProperty
        name="Script"
        command="SetScript"
        number_of_elements="1"
        default_values="%s"
        panel_visibility="advanced">
        <Hints>
          <Widget type="multi_line" syntax="python"/>
        </Hints>
        <Documentation>This property contains the text of a python program that
        the programmable source runs.</Documentation>
        </StringVectorProperty>''' % requestData

    if requestInformation:
        requestInformation = '''
      <StringVectorProperty
        name="InformationScript"
        label="RequestInformation Script"
        command="SetInformationScript"
        number_of_elements="1"
        default_values="%s"
        panel_visibility="advanced">
        <Hints>
          <Widget type="multi_line" syntax="python"/>
        </Hints>
        <Documentation>This property is a python script that is executed during
        the RequestInformation pipeline pass. Use this to provide information
        such as WHOLE_EXTENT to the pipeline downstream.</Documentation>
      </StringVectorProperty>''' % requestInformation

    if requestUpdateExtent:
        requestUpdateExtent = '''
      <StringVectorProperty
        name="UpdateExtentScript"
        label="RequestUpdateExtent Script"
        command="SetUpdateExtentScript"
        number_of_elements="1"
        default_values="%s"
        panel_visibility="advanced">
        <Hints>
          <Widget type="multi_line" syntax="python"/>
        </Hints>
        <Documentation>This property is a python script that is executed during
        the RequestUpdateExtent pipeline pass. Use this to modify the update
        extent that your filter ask up stream for.</Documentation>
      </StringVectorProperty>''' % requestUpdateExtent

    return '\n'.join([requestData, requestInformation, requestUpdateExtent])



def getPythonPathProperty():
    return '''
      <StringVectorProperty command="SetPythonPath"
                            name="PythonPath"
                            number_of_elements="1"
                            panel_visibility="advanced">
        <Documentation>A semi-colon (;) separated list of directories to add to
        the python library search path.</Documentation>
      </StringVectorProperty>'''



def getFilterPropertyXml(propertyInfo, propertyName, propertyHelpInfo):

    vis = 'default'
    if 'HIDE' in propertyName or 'Time_Step' in propertyName:
        vis = 'advanced'

    propertyHelp = propertyHelpInfo.get(propertyName, '')

    e = escapeForXmlAttribute

    propertyValue = propertyInfo[propertyName]
    propertyName = propertyName.replace('_HIDE_', '')
    propertyName = propertyName.replace('_HIDE', '')
    propertyName = propertyName.replace('HIDE_', '')
    propertyName = propertyName.replace('HIDE', '')
    propertyLabel = propertyName.replace('_', ' ')

    if isinstance(propertyValue, list):
        numberOfElements = len(propertyValue)
        assert numberOfElements > 0
        propertyType = type(propertyValue[0])
        defaultValues = ' '.join([str(v) for v in propertyValue])
    else:
        numberOfElements = 1
        propertyType = type(propertyValue)
        defaultValues = str(propertyValue)

    if propertyType is bool:

        defaultValues = defaultValues.replace('True', '1').replace('False', '0')

        return '''
      <IntVectorProperty
        panel_visibility="%s"
        name="%s"
        label="%s"
        initial_string="%s"
        command="SetParameter"
        animateable="1"
        default_values="%s"
        number_of_elements="%s">
        <BooleanDomain name="bool" />
        <Documentation>%s</Documentation>
      </IntVectorProperty>''' % (vis, propertyName, propertyLabel, propertyName, defaultValues, numberOfElements, propertyHelp)


    if propertyType is int:
        return '''
      <IntVectorProperty
        panel_visibility="%s"
        name="%s"
        label="%s"
        initial_string="%s"
        command="SetParameter"
        animateable="1"
        default_values="%s"
        number_of_elements="%s">
        <Documentation>%s</Documentation>
      </IntVectorProperty>''' % (vis, propertyName, propertyLabel, propertyName, defaultValues, numberOfElements, propertyHelp)

    if propertyType is float:
        if propertyName is 'Time_Step':
            return '''
      <DoubleVectorProperty
        panel_visibility="%s"
        name="%s"
        label="%s"
        initial_string="%s"
        command="SetParameter"
        animateable="1"
        default_values="%s"
        number_of_elements="%s">
        <Documentation>%s</Documentation>
      </DoubleVectorProperty>''' % (vis, propertyName, propertyLabel, propertyName, defaultValues, numberOfElements, propertyHelp)
        return '''
      <DoubleVectorProperty
        panel_visibility="%s"
        name="%s"
        label="%s"
        initial_string="%s"
        command="SetParameter"
        animateable="1"
        default_values="%s"
        number_of_elements="%s">
        <Documentation>%s</Documentation>
      </DoubleVectorProperty>''' % (vis, propertyName, propertyLabel, propertyName, defaultValues, numberOfElements, propertyHelp)

    if propertyType is str:
        if 'FileName' in propertyName:
            return '''
      <StringVectorProperty
        panel_visibility="%s"
        name="%s"
        label="%s"
        initial_string="%s"
        command="SetParameter"
        animateable="1"
        default_values="%s"
        number_of_elements="%s">
        <FileListDomain name="files"/>
        <Documentation>%s</Documentation>
      </StringVectorProperty>''' % (vis, propertyName, propertyLabel, propertyName, defaultValues, numberOfElements, propertyHelp)
        else:
            return '''
      <StringVectorProperty
        panel_visibility="%s"
        name="%s"
        label="%s"
        initial_string="%s"
        command="SetParameter"
        animateable="1"
        default_values="%s"
        number_of_elements="%s">
        <Documentation>%s</Documentation>
      </StringVectorProperty>''' % (vis, propertyName, propertyLabel, propertyName, defaultValues, numberOfElements, propertyHelp)

    raise Exception('Unknown property type: %r' % propertyType)


def getFilterPropertiesXml(info):

    propertyInfo = info['Properties']
    propertyHelpInfo = info.get('PropertiesHelp', {})
    xml = [getFilterPropertyXml(propertyInfo, name, propertyHelpInfo) for name in sorted(propertyInfo.keys())]
    return '\n'.join(xml)


def getNumberOfInputs(info):
    return info.get('NumberOfInputs', 1)


def getInputPropertyXml(info, inputDataType=None, name="Input", port=0):

    numberOfInputs = getNumberOfInputs(info)
    if not numberOfInputs:
        return ''

    # Recursively call if multiple inputs
    if numberOfInputs > 1 and inputDataType is None:
        inputDataType = info.get('InputDataType', 'vtkDataObject')
        if type(inputDataType) is not list:
            inputDataType = [inputDataType] * numberOfInputs
        if len(inputDataType) != numberOfInputs:
            raise Exception('You must specify `InputDataType` as list with `NumberOfInputs` elements.')
        # Now handle input names: InputNames
        inputNames = info.get('InputNames', [])
        if type(inputNames) is not list:
            raise Exception('`InputNames` must be a list of names.')
        if type(inputNames) is not list or len(inputNames) != numberOfInputs:
            num = len(inputNames)
            if num > numberOfInputs:
                raise Exception('Too many `InputNames` given.')
            # Autogenerate input names
            print('WARNING: length of `InputNames` does not match `numberOfInputs`.')
            # Fill in missing input names
            fill = numberOfInputs - num
            for i in range(fill):
                inputNames.append('Input %d' % (num + i + 1))
            # Reset InputNames in info so other functions can access them
            info['InputNames'] = inputNames
        # Now perfrom recursion
        inputs = []
        for i in range(len(inputDataType)):
            inputs.append(getInputPropertyXml(info,inputDataType=inputDataType[i], name=inputNames[i], port=i))
        outstr = "\n".join(inp for inp in inputs)
        return outstr

    ############
    # TODO: this doesn't work because: vtkPythonProgrammableFilter (0x6080007a7ee0): Attempt to connect input port index 1 for an algorithm with 1 input ports.
    # Now build each input's XML
    if inputDataType is None:
        inputDataType = info.get('InputDataType', 'vtkDataObject')

    inputDataTypeDomain = ''
    inputDataTypeDomain = '''
          <DataTypeDomain name="input_type">
            <DataType value="%s"/>
          </DataTypeDomain>''' % inputDataType

    inputPropertyAttributes = 'command="SetInputConnection"'
    if numberOfInputs > 1:
        inputPropertyAttributes = '''command="AddInputConnection"
        port_index="%d"''' % 0 #(port) # clean_command="RemoveAllInputs" multiple_input="1"
        # TODO: Find a way for python filters to take multiple input ports

    inputPropertyXml = '''
      <InputProperty
        name="%s"
        %s>
          <ProxyGroupDomain name="groups">
            <Group name="sources"/>
            <Group name="filters"/>
          </ProxyGroupDomain>
%s
      </InputProperty>''' % (name, inputPropertyAttributes, inputDataTypeDomain)

    return inputPropertyXml



def _helpArraysXML(info, inputName=None, numArrays=None, labels=None):
    # Gets input arrays XML for each input
    ###################################################
    # Perfrom XML generation for single input at a time
    def _getInputArrayXML(idx, label, name=None):
        if name is None: name = 'Input'
        return'''
      <StringVectorProperty
        name="SelectInputScalars%d"
        label="%s"
        command="SetInputArrayToProcess"
        default_values="%d NULL"
        number_of_elements="5"
        element_types="0 0 0 0 2"
        animateable="0">
        <ArrayListDomain
          name="array_list"
          attribute_type="Scalars"
          input_domain_name="inputs_array">
          <RequiredProperties>
            <Property
              name="%s"
              function="Input" />
          </RequiredProperties>
        </ArrayListDomain>
        <FieldDataDomain
          name="field_list">
          <RequiredProperties>
            <Property
              name="%s"
              function="Input" />
          </RequiredProperties>
        </FieldDataDomain>
      </StringVectorProperty>''' % (idx, label, idx, name, name)


    xml = ''
    for i in range(numArrays):
        xml += _getInputArrayXML(i, labels[i], name=inputName)
        xml += '\n\n'
    return xml




def getInputArraysXML(info):
    # TODO: make sure this is called AFTER input XML is built
    # TODO: handle multiple inputs case
    # Get details
    if "NumberOfInputArrayChoices" not in info:
        return ''
    numberOfInputs = getNumberOfInputs(info)
    numArrays = info.get("NumberOfInputArrayChoices")

    def getLabels():
        labels = info.get('InputArrayLabels', None)
        if labels is None and numberOfInputs > 1:
            labels = [None]*numberOfInputs
            return labels
        if numberOfInputs > 1:
            for l in labels:
                if type(l) is not list:
                    raise Exception('`InputArrayLabels` is improperly structured. Must be a list of lists.')
        return labels

    labels = getLabels()

    def fixArrayLabels(labels, numArrays):
        if numArrays is 0:
            return ''
        if labels is None:
            labels = ['Array %d' % (i+1) for i in range(numArrays)]
            return labels
        if len(labels) < numArrays:
            toadd = numArrays - len(labels)
            for i in range(toadd):
                labels.append('Array %d' % (i + len(labels) + 1))
        return labels

    # Recursively call for each input
    if numberOfInputs > 1:
        if type(numArrays) is not list:
            raise Exception('When multiple inputs, the `NumberOfInputArrayChoices` must be a list of ints for the number of arrays from each input.')
        if len(numArrays) != numberOfInputs:
            raise Exception('You must spectify how many arrays come from each input. `len(NumberOfInputArrayChoices) != NumberOfInputs`.')
        inputNames = info.get('InputNames')
        print(inputNames)

        # Now perfrom recursion
        out = []
        for i in range(numberOfInputs):
            # Fix labels
            print(i)
            labs = fixArrayLabels(labels[i], numArrays[i])
            out.append(_helpArraysXML(info, inputName=inputNames[i], numArrays=numArrays[i], labels=labs))
        outstr = "\n".join(inp for inp in out)
        return outstr
    else:
        # Get parameters from info and call:
        labels = fixArrayLabels(labels, numArrays)
        return _helpArraysXML(info, inputName=None, numArrays=numArrays, labels=labels)


def getVersionAttribute():
    return '''
      <!-- Built on version: %s -->
      <StringVectorProperty
        panel_visibility="never"
        name="BUILDVERSION"
        label="BUILDVERSION"
        initial_string="BUILDVERSION"
        command="SetParameter"
        animateable="1"
        default_values="%s"
        number_of_elements="1">
        <Documentation>This is an attribute to the filter to know what version it was built on. This is necessary for plugins that have major changes across versions and might need to alert a user that their state file is out of date.</Documentation>
      </StringVectorProperty>''' % (__version__, __version__)


def getOutputDataSetTypeXml(info):


    outputDataType = info.get('OutputDataType', '')

    if type(outputDataType) is list:
        raise Exception('Cannot have multiple OutputDataType as there can only be one output.')

    # these values come from vtkType.h in VTK Code Base
    typeMap = {
        '': 8, # same as input
        'vtkPolyData': 0,
        'vtkStructuredPoints': 1,
        'vtkStructuredGrid': 2,
        'vtkRectilinearGrid': 3,
        'vtkUnstructuredGrid': 4,
        'vtkPiecewiseFunction': 5,
        'vtkImageData': 6,
        'vtkDataObject': 7,
        'vtkPointSet': 9,
        'vtkUniformGrid': 10,
        'vtkCompositeDataSet': 11,
        #'vtkMultiGroupDataSet': 12, # obsolete
        'vtkMultiBlockDataSet': 13,
        #'vtkHierarchicalDataSet': 14, # obsolete
        #'vtkHierarchicalBoxDataSet': 15, # obsolete
        # 'vtkGenericDataSet': 16, # obsolete
        'vtkHyperOctree': 17,
        #'vtkTemporalDataSet': 18, # obsolete
        'vtkTable': 19,
        'vtkGraph': 20,
        'vtkTree': 21
    }

    typeValue = typeMap[outputDataType]

    # Make sure output type is specified if more than one input
    # TODO: we could check to see if all input types are same and use that...
    if typeValue is 8 and getNumberOfInputs(info) > 1:
        raise Exception('OutputDataType must be specified when there are multiple inputs.')

    return '''
      <!-- Output data type: "%s" -->
      <IntVectorProperty command="SetOutputDataSetType"
                         default_values="%s"
                         name="OutputDataSetType"
                         number_of_elements="1"
                         panel_visibility="never">
        <Documentation>The value of this property determines the dataset type
        for the output of the programmable filter.</Documentation>
      </IntVectorProperty>''' % (outputDataType or 'Same as input', typeValue)


def getProxyGroup(info):
    if "Group" not in info:
        return 'sources' if getNumberOfInputs(info) == 0 else 'filters'
    else:
        return info["Group"]

def getFileReaderXml(info):
    """Author: Daan van Vugt <daanvanvugt@gmail.com>
    https://github.com/Exteris/paraview-python-file-reader
    """
    if getNumberOfInputs(info) > 0 or not info.get('FileSeries', True):
        return ''
    else:
        if "Extensions" not in info and "ReaderDescription" not in info: #info["FilterCategory"]
            #raise Exception('Reader needs `Extensions` and `ReaderDescription` attributes.')
            return ''
        extensions = info.get('Extensions', '')
        readerDescription = info.get('ReaderDescription', '')
        return '''
      <StringVectorProperty
        name="FileNames"
        initial_string="FileNames"
        animateable="0"
        number_of_elements="0"
        command="AddParameter"
        clean_command="ClearParameter"
        repeat_command="1"
        panel_visibility="advanced">
        <FileListDomain name="files"/>
            <Documentation>
            The list of files to be read by the reader.
            </Documentation>
      </StringVectorProperty>

      <DoubleVectorProperty
        name="TimestepValues"
        repeatable="1"
        information_only="1">
        <TimeStepsInformationHelper/>
            <Documentation>
            Available timestep values.
            </Documentation>
        </DoubleVectorProperty>
        <Hints>
            <ReaderFactory extensions="%s"
                    file_description="%s" />
        </Hints>
        ''' % (extensions, readerDescription)

def _genFileContainor(allXml):
    outputXml = '''\
<ServerManagerConfiguration>
%s
</ServerManagerConfiguration>''' % (allXml)
    return outputXml

def _genGroupContainor(proxyGroup, pluginXml):
    if len(pluginXml) < 1:
        return pluginXml
    outputXml = '''\
  <!-- CATEGORY %s -->
  <ProxyGroup name="%s">
%s
  </ProxyGroup>''' % (proxyGroup.upper(), proxyGroup, pluginXml)
    return outputXml

def generatePythonFilter(info, embed=False, category=None):
    e = escapeForXmlAttribute

    proxyName = info['Name']
    proxyLabel = info['Label']
    shortHelp = e(info['Help'])
    longHelp = e(info['Help'])
    extraXml = info.get('ExtraXml', '')

    proxyGroup = getProxyGroup(info)
    versionXml = getVersionAttribute()
    inputPropertyXml = getInputPropertyXml(info)
    outputDataSetType = getOutputDataSetTypeXml(info)
    scriptProperties = getScriptPropertiesXml(info)
    filterProperties = getFilterPropertiesXml(info)
    filterGroup = getFilterGroup(info, category=category)
    fileReaderProperties = getFileReaderXml(info)
    inputArrayDropDowns = getInputArraysXML(info)
    pythonPath = getPythonPathProperty()

    pluginXml = '''
    <SourceProxy name="%s" class="vtkPythonProgrammableFilter" label="%s">
      <Documentation
        long_help="%s"
        short_help="%s">
      </Documentation>
%s
%s
%s
%s
%s
%s
%s
%s
%s
%s
    </SourceProxy>''' % (proxyName, proxyLabel, longHelp, shortHelp,
                filterGroup, versionXml, outputDataSetType, extraXml, inputPropertyXml,
                inputArrayDropDowns, fileReaderProperties, filterProperties,
                scriptProperties, pythonPath)


    if embed:
        return pluginXml, proxyGroup
    return _genFileContainor(_genGroupContainor(proxyGroup, pluginXml))

def getFilterGroup(info, category=None):
    if category is None and "FilterCategory" in info:
        category = info["FilterCategory"]
    # If reader
    if "Extensions" in info and "ReaderDescription" in info:
        # Just reader attributes, no category
        if category is None:
            return ('''\
      <Hints>
        <ReaderFactory extensions="%s"
          file_description="%s" />
      </Hints>''' % (info["Extensions"], info["ReaderDescription"]))
        # Has category and reader attributes
        if info.get('FileSeries', True):
            return ('''\
      <Hints>
        <ShowInMenu category="%s" />
        <ReaderFactory extensions="%s"
          file_description="%s" />
      </Hints>''' % (category, info["Extensions"], info["ReaderDescription"]))
        else:
            return ('''\
      <Hints>
        <ShowInMenu category="%s" />
      </Hints>
      <Hints>
        <ReaderFactory extensions="%s"
          file_description="%s" />
      </Hints>''' % (category, info["Extensions"], info["ReaderDescription"]))
    # not reader and no category
    elif category is None:
            return ''
    # Otherwise its has a category and is not a reader
    return ('''\
      <Hints>
        <ShowInMenu category="%s" />
      </Hints>''' % (category))


def replaceFunctionWithSourceString(namespace, functionName, allowEmpty=False):

    func = namespace.get(functionName)
    if not func:
        if allowEmpty:
            namespace[functionName] = ''
            return
        else:
            raise Exception('Function %s not found in input source code.' % functionName)

    if not inspect.isfunction(func):
        raise Exception('Object %s is not a function object.' % functionName)

    lines = inspect.getsourcelines(func)[0]

    if len(lines) <= 1:
        raise Exception('Function %s must not be a single line of code.' % functionName)

    # skip first line (the declaration) and then dedent the source code
    sourceCode = textwrap.dedent(''.join(lines[1:]))

    namespace[functionName] = sourceCode


def generatePythonFilterFromFiles(scriptFile, outputFile=None, category=None):
    embed = False
    if outputFile is None:
        embed = True
    namespace = {}
    execfile(scriptFile, namespace)

    replaceFunctionWithSourceString(namespace, 'RequestData')
    replaceFunctionWithSourceString(namespace, 'RequestInformation', allowEmpty=True)
    replaceFunctionWithSourceString(namespace, 'RequestUpdateExtent', allowEmpty=True)

    xmlOutput = generatePythonFilter(namespace, embed=embed, category=category)

    if embed:
        return xmlOutput

    open(outputFile, 'w').write(xmlOutput)
    return None

def getConfig(dir):
    tree = ET.parse(dir)
    root = tree.getroot()
    return root.attrib

def generatePluginSuite(indir, outdir, category=None):
    # find config file
    try:
        config = getConfig(indir + '/build.config')
    except FileNotFoundError:
        raise Exception("No config file for directory: %s" % indir)
    category = config.get("category", None)
    # get all plugin files in that directory
    # iterate over all plugins in that dir and make one plugin XML file
    readersGroup = ''
    filtersGroup = ''
    for o in os.listdir(indir):
        if o.endswith(('.py')):
            script = indir + '/' + o
            xml, group = generatePythonFilterFromFiles(script, category=category)
            comment = '\n\n%s<!-- %s -->' % (' '*4, script)
            if group is 'sources':
                readersGroup += comment + xml
            elif group is 'filters':
                filtersGroup += comment + xml
            else: raise Exception('Group %s unknown.' % group)
    # Now put groups into XML Proxy Groups
    readersGroup = _genGroupContainor('sources', readersGroup)
    filtersGroup = _genGroupContainor('filters', filtersGroup)
    xmlOutput = readersGroup + filtersGroup
    xmlOutput = _genFileContainor(xmlOutput)
    # Assumes output is a directory
    filename = '%s/%s.xml' % (outdir, config['name'].replace(' ', '-'))
    open(filename, 'w').write(xmlOutput)
    return None

def main():

    if len(sys.argv) != 3:
        print('Usage: %s <python input filename> <xml output filename>' % sys.argv[0])
        sys.exit(1)

    inputScript = sys.argv[1]
    outputFile = sys.argv[2]

    # if outputFile is a directory then:
    if os.path.isdir(inputScript):
        if not os.path.isdir(outputFile):
            raise Exception('Two paths must be given for plugin suite.')
        generatePluginSuite(inputScript, outputFile)
    # else it is a file:
    else:
        generatePythonFilterFromFiles(inputScript, outputFile)
    return None


if __name__ == '__main__':
    main()
