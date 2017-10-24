Name = 'MergeTables'
Label = 'Merge Tables'
FilterCategory = 'CSM Geophysics Filters DEV'
Help = 'Merges two tables with the same number of rows'

NumberOfInputs = 2
InputDataType = 'vtkTable'
OutputDataType = 'vtkTable' #vtkPolyData
ExtraXml = '''\

'''


Properties = dict(
    Field_Type=0
)


def RequestData():
    from vtk.util import numpy_support as nps
    import numpy as np
    from vtk.numpy_interface import dataset_adapter as dsa
    from vtk.numpy_interface import algorithms as algs

    pdi = self.GetInput()
    pdo = self.GetOutput()

    # Get input array name
    info = self.GetInputArrayInformation(0)
    name = info.Get(vtk.vtkDataObject.FIELD_NAME())
    field = info.Get(vtk.vtkDataObject.FIELD_ASSOCIATION())

    wpdi = dsa.WrapDataObject(pdi)

    # Point Data
    if field == 0:
        arr = wpdi.PointData[name]
    # Cell Data:
    elif field == 1:
        arr = wpdi.CellData[name]
    # Field Data:
    elif field == 2:
        arr = wpdi.FieldData[name]
    # Row Data:
    elif field == 6:
        raise Exception('Row Data not supported.')
        #arr = wpdi.RowData[name]
    else:
        raise Exception('Field association not defined. Try inputing Point, Cell, Field, or Row data.')

    c = nps.numpy_to_vtk(num_array=arr,deep=True)
    c.SetName(name)

    # Point Data
    if Field_Type == 0:
        pdo.GetPointData().AddArray(c)
    # Cell Data:
    elif Field_Type == 1:
        pdo.GetCellData().AddArray(c)
