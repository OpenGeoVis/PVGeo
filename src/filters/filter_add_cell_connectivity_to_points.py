Name = 'AddCellConnectivityToPoints'
Label = 'Add Cell Connectivity To Points'
Help = ''

NumberOfInputs = 1
InputDataType = 'vtkPolyData'
OutputDataType = 'vtkPolyData'
ExtraXml = '''\
<Hints>
    <ShowInMenu category="CSM Geophysics Filters" />
</Hints>

<IntVectorProperty
    name="Cell_Type"
    command="SetParameter"
    number_of_elements="1"
    initial_string="test_drop_down_menu"
    default_values="0">
    <EnumerationDomain name="enum">
          <Entry value="4" text="Poly Line"/>
          <Entry value="3" text="Line"/>
    </EnumerationDomain>
    <Documentation>
        This property indicates which two axii will be swapped.
    </Documentation>
</IntVectorProperty>
'''


Properties = dict(
    Cell_Type=4,
    #Use_nearest_nbr=True,
    #max_distance=100.0
)

# TODO: Use nearest neighbor approximations or provide option to if ShallowCopy
# this will assign connectivity from the first point to the second point and from the second point to the third, etc. and varying for different cell types.
# TODO: nearest neighbor approxs for hexahedral
def RequestData():
    from datetime import datetime
    import numpy as np
    from scipy.spatial import cKDTree
    from vtk.util import numpy_support as nps
    from vtk.numpy_interface import dataset_adapter as dsa
    #from vtk.numpy_interface import algorithms as algs
    startTime = datetime.now()
    pdi = self.GetInput() # VTK PolyData Type
    pdo = self.GetOutput() # VTK PolyData Type

    # Get the Points over the NumPy interface
    wpdi = dsa.WrapDataObject(pdi) # NumPy wrapped input
    points = np.array(wpdi.Points) # New NumPy array of poins so we dont destroy input

    #pdo.SetPoints(pdi.GetPoints())
    pdo.DeepCopy(pdi)
    numPoints = pdi.GetNumberOfPoints()

    sft = 0
    # Type map is specified in vtkCellType.h
    #for i in range(0, numPoints - 2):
    while(len(points) > 1):
        tree = cKDTree(points)
        if Cell_Type == 3 or Cell_Type == 4:
            # Get indices of k nearest points
            dist, ind = tree.query(points[0], k=2)
            ptsi = [ind[0]+sft, ind[1]+sft]
            pdo.InsertNextCell(Cell_Type, 2, ptsi)
            points = np.delete(points, 0, 0) # Deletes first row
        '''
        if Cell_Type == 9:
            # Get indices of k nearest points
            dist, ind = tree.query(points[0], k=4)
            if len(points) < 4:
                break
            ptsi = [ind[0]+sft, ind[1]+sft, ind[2]+sft, ind[3]+sft]
            pdo.InsertNextCell(Cell_Type, 4, ptsi)
            # TODO: which ones do I delete here?
            points = np.delete(points, 0, 0) # Deletes first row
        '''
        del(tree)
        sft += 1
    print((datetime.now() - startTime))
