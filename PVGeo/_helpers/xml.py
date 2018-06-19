# This file has a ton of convienance methods for generating extra XML for
# the pvpluginss

def getPythonPathProperty():
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



def getPropertyXml(name, label, command, value, visibility='default', help=''):
    # A helper to build XML for any data type/method

    def _propXML(typ, visibility, name, label, command, defaultValues, num, help, extra=''):
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
      </%sVectorProperty>''' % (typ, visibility, name, label, command, defaultValues, num, extra, help, typ)

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
    else:
        raise RuntimeError('getPropertyXml(): Unknown property type: %r' % propertyType)

    return _propXML(typ, visibility, name, label, command, defaultValues, num, help, extra)



def getFileReaderXml(extensions, readerDescription='', command="AddFileName"):
    """Author: Daan van Vugt <daanvanvugt@gmail.com>
    https://github.com/Exteris/paraview-python-file-reader
    Modified by Bane Sullivan: <info@pvgeo.org>
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
        </Hints>''' % (command, extensions, readerDescription)


def getDropDownXml(name,command,labels, help=''):

    def _enum(labels):
        els = []
        for i in range(len(labels)):
            els.append('<Entry value="%d" text="%s"/>' % (i,labels[i]))

        formatter = r'%s\n'*len(els)
        dom = '''\
        <EnumerationDomain name="enum">'''
        for el in els:
            dom += ('''
          %s''' % el)
        dom += ('''
        </EnumerationDomain>''')
        return dom

    domain = _enum(labels)
    return '''\
      <IntVectorProperty
        name="%s"
        command="%s"
        number_of_elements="1"
        default_values="0">
%s
        <Documentation>
          %s
        </Documentation>
      </IntVectorProperty>''' % (name,command,domain,help)
