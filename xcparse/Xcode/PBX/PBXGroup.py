from .PBX_Base_Reference import *
from .PBX_Constants import *
from ...Helpers import path_helper

class PBXGroup(PBX_Base_Reference):
    
    def __init__(self, lookup_func, dictionary, project, identifier):
        super(PBXGroup, self).__init__(lookup_func, dictionary, project, identifier);
        if kPBX_REFERENCE_children in dictionary.keys():
            self.children = self.parseProperty(kPBX_REFERENCE_children, lookup_func, dictionary, project, True);
        