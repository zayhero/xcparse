from __future__ import absolute_import
import os
import sys

from .xcspec import *

class XCSpecBuildSystem(xcspec):
    
    def __init__(self, spec_data):
        super(XCSpecBuildSystem, self).__init__(spec_data);