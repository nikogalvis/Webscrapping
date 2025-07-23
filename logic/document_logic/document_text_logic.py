"""
Base class for creating documents
"""
class Documents:
    """
    Dcuments class
    """
    def __init__(self, name: "str", type: "str"):
        self.type = type

    def create_document(self):
        raise NotImplementedError("Child classes must implement the method")

    def add_information(self, new_information: "str"):
        raise NotImplementedError("Child classes must implement the method")