# This file has a ton of convienance methods for generating extra XML for
# the pvpluginss
__all__ = [
    'get_python_path_property',
    'get_reader_time_step_values',
    'get_vtk_type_map',
    'get_property_xml',
    'get_file_reader_xml',
    'get_drop_down_xml',
    '_help_arrays_xml',
    'get_input_array_xml'
]

from . import errors as _helpers


def get_python_path_property():
    """Get the XML content for setting the Python path when making a ParaView
    plugin.
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


def get_reader_time_step_values(extensions, reader_description):
    """Get the XML content for reader time step values the Python path when
    making a ParaView plugin.
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
      ''' % (extensions, reader_description)



def get_vtk_type_map():
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



def get_property_xml(name, command, default_values, panel_visibility='default', help=''):
    """Get the XML content for a property of a parameter for a python data
    object when making a ParaView plugin.
    """
    # A helper to build XML for any data type/method
    value = default_values

    def _prop_xml(typ, panel_visibility, name, command, default_values, num, help, extra=''):
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
      </%sVectorProperty>''' % (typ, panel_visibility, command, name, command,
                                default_values, num, extra, help, typ)

    if isinstance(value, list):
        num = len(value)
        if not num > 0:
            raise AssertionError('length of values must be grater than 0')
        propertyType = type(value[0])
        default_values = ' '.join([str(v) for v in value])
    else:
        num = 1
        propertyType = type(value)
        default_values = str(value)

    typ = ''
    extra = ''
    if propertyType is bool:
        typ = 'Int'
        extra = '<BooleanDomain name="bool" />'
        default_values = default_values.replace('True', '1').replace('False', '0')
    elif propertyType is float:
        typ = 'Double'
    elif propertyType is str:
        typ = 'String'
    elif propertyType is int:
        typ = 'Int'
    else:
        raise RuntimeError('get_property_xml(): Unknown property type: %r' % propertyType)

    return _prop_xml(typ, panel_visibility, name, command, default_values, num, help, extra)



def get_file_reader_xml(extensions, reader_description='', command="AddFileName"):
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
        clean_command="clear_file_names"
        repeat_command="1"
        panel_visibility="never">
        <FileListDomain name="files"/>
            <Documentation>
            The list of files to be read by the reader.
            </Documentation>
      </StringVectorProperty>
      <Hints>
            <ReaderFactory extensions="%s"
                    file_description="%s" />
      </Hints>''' % (command, extensions, reader_description)


def get_drop_down_xml(name, command, labels, help='', values=None):
    """Get the XML content for a drop down menu when making a ParaView plugin.
    """

    def _enum(labels, values=None):
        if values is None:
            values = range(len(labels))
        els = []
        for i, lab in enumerate(labels):
            els.append('<Entry value="%d" text="%s"/>' % (values[i],lab))

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





def _help_arrays_xml(idx, input_name=None, label=None):
    """Internal helper
    """
    if input_name is None:
        input_name = 'Input'
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
      </StringVectorProperty>''' % (idx, label, idx, input_name, input_name)




def get_input_array_xml(labels=None, nInputPorts=1, n_arrays=1, input_names='Input'):
    """Get the XML content for an array selection drop down menu when making a
    ParaView plugin.
    """
    def get_labels(labels):
        if labels is None and nInputPorts > 1:
            labels = [None]*nInputPorts
            return labels
        if nInputPorts > 1:
            for l in labels:
                if not isinstance(l, list):
                    raise _helpers.PVGeoError('`InputArrayLabels` is improperly structured. Must be a list of lists.')
        return labels

    labels = get_labels(labels)

    def fix_array_labels(labels, n_arrays):
        if n_arrays is 0:
            return ''
        if labels is None:
            labels = ['Array %d' % (i+1) for i in range(n_arrays)]
            return labels
        if len(labels) < n_arrays:
            toadd = n_arrays - len(labels)
            for i in range(toadd):
                labels.append('Array %d' % (i + len(labels) + 1))
        return labels

    # Recursively call for each input
    if nInputPorts > 1:
        if not isinstance(n_arrays, list):
            raise _helpers.PVGeoError('When multiple inputs, the `NumberOfInputArrayChoices` must be a list of ints for the number of arrays from each input.')
        if len(n_arrays) != nInputPorts:
            raise _helpers.PVGeoError('You must spectify how many arrays come from each input. `len(NumberOfInputArrayChoices) != nInputPorts`.')

        # Now perfrom recursion
        out = []
        for i in range(nInputPorts):
            # Fix labels
            labs = fix_array_labels(labels[i], n_arrays[i])
            xml = ''
            for j in range(n_arrays[i]):
                xml += _help_arrays_xml(i+j, input_name=input_names[i], label=labs[j])
            out.append(xml)
        outstr = "\n".join(inp for inp in out)
        return outstr
    else:
        # Get parameters from info and call:
        labs = fix_array_labels(labels, n_arrays)
        xml = ''
        for j in range(n_arrays):
            xml += _help_arrays_xml(j, input_name=None, label=labs[j])
        return xml
