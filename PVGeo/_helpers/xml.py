# This file has a ton of convienance methods for generating extra XML for
# the pvpluginss
from . import errors as _helpers

def getPythonPathProperty():
    """Get the XML content for setting the Python path when making a ParaView plugin.
    """
    return '''
      <StringVectorProperty
        command="SetPythonPath"
        name="PythonPath"
        number_of_elements="1"
        panel_visibility="advanced">
        <Documentation>A semi-colon (;) separated list of directories to add to
        the python library search path.</Documentation>
      </StringVectorProperty>'''


def getReaderTimeStepValues(extensions, readerDescription):
    """Get the XML content for reader time step values the Python path when making a ParaView plugin.
    """
    return '''<DoubleVectorProperty
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



def getVTKTypeMap():
    """Get the the VTK Type Map as specified in ``vtkType.h``
    """
    return {
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



def getPropertyXml(name, command, default_values, visibility='default', help=''):
    """Get the XML content for a property of a parameter for a python data object when making a ParaView plugin.
    """
    # A helper to build XML for any data type/method
    value = default_values

    def _propXML(typ, visibility, name, command, defaultValues, num, help, extra=''):
        return '''
      <%sVectorProperty
        panel_visibility="%s"
        name="%s"
        label="%s"
        command="%s"
        default_values="%s"
        number_of_elements="%s">
        %s
        <Documentation>%s</Documentation>
      </%sVectorProperty>''' % (typ, visibility, command, name, command, defaultValues, num, extra, help, typ)

    if isinstance(value, list):
        num = len(value)
        assert num > 0
        propertyType = type(value[0])
        defaultValues = ' '.join([str(v) for v in value])
    else:
        num = 1
        propertyType = type(value)
        defaultValues = str(value)

    typ = ''
    extra = ''
    if propertyType is bool:
        typ = 'Int'
        extra = '<BooleanDomain name="bool" />'
        defaultValues = defaultValues.replace('True', '1').replace('False', '0')
    elif propertyType is float:
        typ = 'Double'
    elif propertyType is str:
        typ = 'String'
    elif propertyType is int:
        typ = 'Int'
    else:
        raise RuntimeError('getPropertyXml(): Unknown property type: %r' % propertyType)

    return _propXML(typ, visibility, name, command, defaultValues, num, help, extra)



def getFileReaderXml(extensions, readerDescription='', command="AddFileName"):
    """Get the XML for a selectectable file for a reader when building a ParaView plugin

    Note:
        * Thanks: `Daan van Vugt`_ and for `his work here`_
        * Modified by `Bane Sullivan`_

    .. _Daan van Vugt: daanvanvugt@gmail.com
    .. _his work here: https://github.com/Exteris/paraview-python-file-reader
    .. _Bane Sullivan: info@pvgeo.org
    """
    return '''
      <StringVectorProperty
        name="FileNames"
        label="File Names"
        animateable="0"
        number_of_elements="0"
        command="%s"
        clean_command="ClearFileNames"
        repeat_command="1"
        panel_visibility="advanced">
        <FileListDomain name="files"/>
            <Documentation>
            The list of files to be read by the reader.
            </Documentation>
      </StringVectorProperty>
      <Hints>
            <ReaderFactory extensions="%s"
                    file_description="%s" />
      </Hints>''' % (command, extensions, readerDescription)


def getDropDownXml(name, command, labels, help='', values=None):
    """Get the XML content for a drop down menu when making a ParaView plugin.
    """

    def _enum(labels, values=None):
        if values is None:
            values = range(len(labels))
        els = []
        for i in range(len(labels)):
            els.append('<Entry value="%d" text="%s"/>' % (values[i],labels[i]))

        formatter = r'%s\n'*len(els)
        dom = '''\
        <EnumerationDomain name="enum">'''
        for el in els:
            dom += ('''
          %s''' % el)
        dom += ('''
        </EnumerationDomain>''')
        return dom, values

    domain, values = _enum(labels, values)
    return '''\
      <IntVectorProperty
        name="%s"
        command="%s"
        number_of_elements="1"
        default_values="%d">
%s
        <Documentation>
          %s
        </Documentation>
      </IntVectorProperty>''' % (name, command, values[0], domain, help)





def _helpArraysXml(idx, inputName=None, label=None):
    """Internal helper
    """
    if inputName is None:
        inputName = 'Input'
    if label is None:
        label = 'Array%d' % idx
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
      </StringVectorProperty>''' % (idx, label, idx, inputName, inputName)




def getInputArrayXml(labels=None, nInputPorts=1, numArrays=1, inputNames='Input'):
    """Get the XML content for an array selection drop down menu when making a ParaView plugin.
    """
    def getLabels(labels):
        if labels is None and nInputPorts > 1:
            labels = [None]*nInputPorts
            return labels
        if nInputPorts > 1:
            for l in labels:
                if type(l) is not list:
                    raise _helpers.PVGeoError('`InputArrayLabels` is improperly structured. Must be a list of lists.')
        return labels

    labels = getLabels(labels)

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
    if nInputPorts > 1:
        if type(numArrays) is not list:
            raise _helpers.PVGeoError('When multiple inputs, the `NumberOfInputArrayChoices` must be a list of ints for the number of arrays from each input.')
        if len(numArrays) != nInputPorts:
            raise _helpers.PVGeoError('You must spectify how many arrays come from each input. `len(NumberOfInputArrayChoices) != nInputPorts`.')

        # Now perfrom recursion
        out = []
        for i in range(nInputPorts):
            # Fix labels
            labs = fixArrayLabels(labels[i], numArrays[i])
            xml = ''
            for j in range(numArrays[i]):
                xml += _helpArraysXml(i+j, inputName=inputNames[i], label=labs[j])
            out.append(xml)
        outstr = "\n".join(inp for inp in out)
        return outstr
    else:
        # Get parameters from info and call:
        labs = fixArrayLabels(labels, numArrays)
        xml = ''
        for j in range(numArrays):
            xml += _helpArraysXml(j, inputName=None, label=labs[j])
        return xml





# import inspect
# import textwrap
#
# def escapeForXmlAttribute(s):
#
#     # http://www.w3.org/TR/2000/WD-xml-c14n-20000119.html#charescaping
#     # In character data and attribute values, the character information items "<" and "&" are represented by "&lt;" and "&amp;" respectively.
#     # In attribute values, the double-quote character information item (") is represented by "&quot;".
#     # In attribute values, the character information items TAB (#x9), newline (#xA), and carriage-return (#xD) are represented by "&#x9;", "&#xA;", and "&#xD;" respectively.
#
#     s = s.replace('&', '&amp;') # Must be done first!
#     s = s.replace('<', '&lt;')
#     s = s.replace('>', '&gt;')
#     s = s.replace('"', '&quot;')
#     s = s.replace('\r', '&#xD;')
#     s = s.replace('\n', '&#xA;')
#     s = s.replace('\t', '&#x9;')
#     return s
#
#
# def _replaceFunctionWithSourceString(func, allowEmpty=True):
#
#     if not func:
#         if allowEmpty:
#             namespace[functionName] = ''
#             return
#         else:
#             raise _helpers.PVGeoError('Function not found.')
#
#     # if not inspect.isfunction(func):
#     #     raise _helpers.PVGeoError('Object is not a function object.')
#
#     lines = inspect.getsourcelines(func)[0]
#
#     if len(lines) <= 1:
#         raise _helpers.PVGeoError('Function %s must not be a single line of code.' % functionName)
#
#     # skip first line (the declaration) and then dedent the source code
#     sourceCode = textwrap.dedent(''.join(lines[1:]))
#
#     return sourceCode
#
#
#
# def getRequestInfoScriptXml(func):
#     """For testing only"""
#     e = escapeForXmlAttribute
#     rinfo = e(_replaceFunctionWithSourceString(func))
#     return '''
#       <StringVectorProperty
#         name="InformationScript"
#         label="RequestInformation Script"
#         command="SetInformationScript"
#         number_of_elements="1"
#         default_values="%s"
#         panel_visibility="advanced">
#         <Hints>
#           <Widget type="multi_line" syntax="python"/>
#         </Hints>
#         <Documentation>This property is a python script that is executed during
#         the RequestInformation pipeline pass. Use this to provide information
#         such as WHOLE_EXTENT to the pipeline downstream.</Documentation>
#       </StringVectorProperty>''' % rinfo
