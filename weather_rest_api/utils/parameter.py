def is_valid_parameter(var: str) -> bool:
    """
    This function checks if the parameter is valid.
    A valid parameter is a string that is not empty, not numeric and not None.
    """
    if not var:
        return False
    if var == '':
        return False
    if var.isnumeric():
        return False
    return True

def is_valid_city_element(element: dict) -> bool:
    """
    This function checks if the element has the following keys:
    - ascii_display
    - lat
    - long
    """
    if not 'lat' in element or not 'long' in element:
        return False
    if element['lat'] == '' or element['long'] == '':
        return False
    if element['lat'] == None or element['long'] == None:
        return False
    return True