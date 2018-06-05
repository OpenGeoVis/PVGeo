Name = 'NormalizeArray'
Label = 'Normalize Array'
Help = 'This filter allows the user to select an array from the input data set to be normalized. The filter will append another array to that data set for the output. The user can specify how they want to rename the array, can choose a multiplier, and can choose from several types of common normalizations (more functionality added as requested).'

NumberOfInputs = 1
NumberOfInputArrayChoices = 1
InputArrayLabels = ['Array']
# Works on any data type so no need to specify input/ouptut
ExtraXml = '''\
      <IntVectorProperty
        name="Normalization"
        command="SetParameter"
        number_of_elements="1"
        initial_string="test_drop_down_menu"
        default_values="0">
        <EnumerationDomain name="enum">
          <Entry value="0" text="Feature Scaling"/>
          <Entry value="1" text="Standard Score"/>
          <Entry value="2" text="Natural Log"/>
          <Entry value="3" text="Log Base 10"/>
          <Entry value="4" text="Just Multiply"/>
        </EnumerationDomain>
        <Documentation>
          This is the type of normalization to apply to the input array.
        </Documentation>
      </IntVectorProperty>
'''


Properties = dict(
    Multiplier=1.0,
    New_Array_Name='Normalized',
    Normalization=0,
    Absolute_Value=False,
    Use_Range=False,
    Range=[0.0,0.0]
)

PropertiesHelp = dict(
    Multiplier="This is a static shifter/scale factor across the array after normalization.",
    New_Array_Name="Give the new normalized array a meaningful name.",
    Absolute_Value="This will take the absolute value of the array before normalization."
)


def RequestData():
    from PVGPpy.filt import normalizeArray
    import PVGPpy.helpers as inputhelp
    # Choose range to use:
    if Use_Range:
        rng = Range
    else:
        rng = None
    # Get input/output of Proxy
    pdi = self.GetInput()
    pdo = self.GetOutput()
    # Grab input arrays to process from drop down menus
    # Simply grab the name and field association
    name = inputhelp.getSelectedArrayName(self, 0)
    field = inputhelp.getSelectedArrayField(self, 0)
    # Perfrom normalization
    normalizeArray(pdi, (name,field), Normalization, multiplier=Multiplier, newName=New_Array_Name, pdo=pdo, abs=Absolute_Value, rng=rng)
