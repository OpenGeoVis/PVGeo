#!/usr/bin/env python2

# See blog for details: https://blog.kitware.com/easy-customization-of-the-paraview-python-programmable-filter-property-panel/
#
# This code has been heavily modified by Bane Sullivan (banesullivan@gmail.com) for making customized filters in the geoscience data visualization. Credit does not go to Bane for this script but to the author of the above blog post.


import os
import sys
import inspect
import textwrap


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
    if 'HIDE' in propertyName:
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
    return '\n\n'.join(xml)


def getNumberOfInputs(info):
    return info.get('NumberOfInputs', 1)


def getInputPropertyXml(info):

    numberOfInputs = getNumberOfInputs(info)
    if not numberOfInputs:
        return ''


    inputDataType = info.get('InputDataType', 'vtkDataObject')

    inputDataTypeDomain = ''
    if inputDataType:
        inputDataTypeDomain = '''
          <DataTypeDomain name="input_type">
            <DataType value="%s"/>
          </DataTypeDomain>''' % inputDataType

    inputPropertyAttributes = 'command="SetInputConnection"'
    if numberOfInputs > 1:
        inputPropertyAttributes = '''\
            clean_command="RemoveAllInputs"
            command="AddInputConnection"
            multiple_input="1"'''

    inputPropertyXml = '''
      <InputProperty
        name="Input"
        %s>
          <ProxyGroupDomain name="groups">
            <Group name="sources"/>
            <Group name="filters"/>
          </ProxyGroupDomain>
          %s
      </InputProperty>''' % (inputPropertyAttributes, inputDataTypeDomain)

    return inputPropertyXml


def getOutputDataSetTypeXml(info):


    outputDataType = info.get('OutputDataType', '')

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


def generatePythonFilter(info):
    e = escapeForXmlAttribute

    proxyName = info['Name']
    proxyLabel = info['Label']
    shortHelp = e(info['Help'])
    longHelp = e(info['Help'])
    extraXml = info.get('ExtraXml', '')

    proxyGroup = getProxyGroup(info)
    inputPropertyXml = getInputPropertyXml(info)
    outputDataSetType = getOutputDataSetTypeXml(info)
    scriptProperties = getScriptPropertiesXml(info)
    filterProperties = getFilterPropertiesXml(info)
    filterGroup = getFilterGroup(info)


    outputXml = '''\
<ServerManagerConfiguration>
  <ProxyGroup name="%s">
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
    </SourceProxy>
 </ProxyGroup>
</ServerManagerConfiguration>
      ''' % (proxyGroup, proxyName, proxyLabel, longHelp, shortHelp,
                filterGroup, extraXml, inputPropertyXml,
                filterProperties, outputDataSetType, scriptProperties)

    return textwrap.dedent(outputXml)

def getFilterGroup(info):
    if "FilterCategory" not in info:
        return ''
    else:
        return ('''\
        <Hints>
            <ShowInMenu category="%s" />
        </Hints>
        ''' % info["FilterCategory"])


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


def generatePythonFilterFromFiles(scriptFile, outputFile):

    namespace = {}
    execfile(scriptFile, namespace)

    replaceFunctionWithSourceString(namespace, 'RequestData')
    replaceFunctionWithSourceString(namespace, 'RequestInformation', allowEmpty=True)
    replaceFunctionWithSourceString(namespace, 'RequestUpdateExtent', allowEmpty=True)

    xmlOutput = generatePythonFilter(namespace)

    open(outputFile, 'w').write(xmlOutput)


def main():

    if len(sys.argv) != 3:
        print('Usage: %s <python input filename> <xml output filename>' % sys.argv[0])
        sys.exit(1)

    inputScript = sys.argv[1]
    outputFile = sys.argv[2]

    generatePythonFilterFromFiles(inputScript, outputFile)


if __name__ == '__main__':
    main()
