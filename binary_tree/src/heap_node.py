"""
Class to implement heap node
It allows any generic object to be added to heap
"""
class HeapNode(object):
    """
    Parameters:
        properties: Dictionary which specifies the attributes of the heap node as key-value pair
        value_attribute: Name of attribute that will be used to maintain the heap
    """
    def __init__(self, properties, value_attribute):
        for k, v in properties.items():
            setattr(self, k, v)
        if value_attribute not in properties:
            raise Exception("Field to be used for heap doesn't appears as node's attributes")
        self.value_attribute = value_attribute

    def get_value_attribute(self):
        return getattr(self, self.value_attribute)

    def set_value_attribute(self, value):
        setattr(self, self.value_attribute, value)

    def __str__(self):
        return '[' +  ','.join([':'.join(map(lambda x: str(round(x, 2)) if isinstance(x, float) else str(x), (k, v))) for k,v in self.__dict__.items() if k != 'value_attribute']) + ']'
