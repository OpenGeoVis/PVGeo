Name = 'TestFilter'
Label = 'Test Filter'
Help = 'Help for the Test Filter'

NumberOfInputs = 1
InputDataType = 'vtkPolyData'
OutputDataType = 'vtkPolyData'
ExtraXml = '''\
<Hints>
    <ShowInMenu category="CSM Geophysics Filters" />
</Hints>
'''


Properties = dict(
    test_bool=True,
    test_int=123,
    test_int_vector=[1, 2, 3],
    test_double=1.23,
    test_double_vector=[1.1, 2.2, 3.3],
    test_string='string value',
)


def RequestData():
    from vtk.util import numpy_support as nps
    pdi = self.GetInput() # VTK Data Type
    pdo = self.GetOutput() # VTK Data Type


def RequestInformation():
    #from paraview import util
    # ABSOLUTELY NECESSARY FOR THE IMAGEDATA FILTERS TO WORK:
    #util.SetOutputWholeExtent(self, [0,nx-1, 0,ny-1, 0,nz-1])
