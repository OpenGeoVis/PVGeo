Name = 'TestFilter'
Label = 'Test Filter'
Help = 'Help for the Test Filter'

NumberOfInputs = 1
InputDataType = 'vtkPolyData'
OutputDataType = 'vtkPolyData'
ExtraXml = ''


Properties = dict(
  test_bool = True,
  test_int = 123,
  test_int_vector = [1, 2, 3],
  test_double = 1.23,
  test_double_vector = [1.1, 2.2, 3.3],
  test_string = 'string value',
  )


def RequestData():

    assert test_bool == True
    assert test_int == 123
    assert test_int_vector == [1, 2, 3]
    assert test_double == 1.23
    assert test_double_vector == [1.1, 2.2, 3.3]
    assert test_string == "string value"
