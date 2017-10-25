Name = 'AddCellConnectivityToPoints'
Label = 'Add Cell Connectivity To Points'
FilterCategory = 'CSM Geophysics Filters'
Help = 'This filter will add linear cell connectivity between scattered points. You have the option to add VTK_Line or VTK_PolyLine connectivity. VTK_Line connectivity makes a straight line between the points in order (either in the order by index or using a nearest neighbor calculation). The VTK_PolyLine adds a poly line connectivity between all points as one spline (either in the order by index or using a nearest neighbor calculation).'

NumberOfInputs = 1
InputDataType = 'vtkPolyData'
OutputDataType = 'vtkPolyData'
ExtraXml = '''\
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
        Choose what type of cell connectivity to have.
    </Documentation>
</IntVectorProperty>
'''


Properties = dict(
    Cell_Type=4,
    Use_nearest_nbr=True,
)

PropertiesHelp = dict(
    Use_nearest_nbr="Check this to use SciPy's cKDTree nearest neighbor algorithms to sort the points to before adding linear connectivity",
)

def RequestData():
    from datetime import datetime
    import numpy as np
    from vtk.util import numpy_support as nps
    from vtk.numpy_interface import dataset_adapter as dsa
    # NOTE: Type map is specified in vtkCellType.h

    startTime = datetime.now()
    pdi = self.GetInput() # VTK PolyData Type
    pdo = self.GetOutput() # VTK PolyData Type

    # Get the Points over the NumPy interface
    wpdi = dsa.WrapDataObject(pdi) # NumPy wrapped input
    points = np.array(wpdi.Points) # New NumPy array of poins so we dont destroy input

    pdo.DeepCopy(pdi)
    numPoints = pdi.GetNumberOfPoints()

    if Use_nearest_nbr:
        from scipy.spatial import cKDTree
        # VTK_Line
        if Cell_Type == 3:
            sft = 0
            while(len(points) > 1):
                tree = cKDTree(points)
                # Get indices of k nearest points
                dist, ind = tree.query(points[0], k=2)
                ptsi = [ind[0]+sft, ind[1]+sft]
                pdo.InsertNextCell(Cell_Type, 2, ptsi)
                points = np.delete(points, 0, 0) # Deletes first row
                del(tree)
                sft += 1
        # VTK_PolyLine
        elif Cell_Type == 4:
            tree = cKDTree(points)
            dist, ptsi = tree.query(points[0], k=numPoints)
            pdo.InsertNextCell(Cell_Type, numPoints, ptsi)
    else:
        # VTK_PolyLine
        if Cell_Type == 4:
            ptsi = [i for i in range(numPoints)]
            pdo.InsertNextCell(Cell_Type, numPoints, ptsi)
        # VTK_Line
        elif Cell_Type == 3:
            for i in range(0, numPoints-1):
                ptsi = [i, i+1]
                pdo.InsertNextCell(Cell_Type, 2, ptsi)
    #print((datetime.now() - startTime))
