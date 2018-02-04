Name = 'AddCellConnectivityToPoints'
Label = 'Add Cell Connectivity To Points'
FilterCategory = 'CSM GP Filters'
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
    from PVGPpy.filt import connectCells
    # Get input/output of Proxy
    pdi = self.GetInput() # VTK PolyData Type
    pdo = self.GetOutput() # VTK PolyData Type
    # Perfrom task
    connectCells(pdi, cellType=Cell_Type, nrNbr=Use_nearest_nbr, pdo=pdo, logTime=False)
