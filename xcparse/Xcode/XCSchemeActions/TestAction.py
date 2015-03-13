from ...Helpers import xcrun_helper
from .Base_Action import *

class TestAction(Base_Action):
    # contents = {};
    # children = [];
    # selectedDebuggerIdentifier = '';
    # selectedLauncherIdentifier = '';
    # shouldUseLaunchSchemeArgsEnv = '';
    # buildConfiguration = '';
    
    
    def __init__(self, action_xml):
        self.root = {};
        self.contents = action_xml;
        if 'selectedDebuggerIdentifier' in self.contents.keys():
            self.selectedDebuggerIdentifier = self.contents.get('selectedDebuggerIdentifier');
        if 'selectedLauncherIdentifier' in self.contents.keys():
            self.selectedLauncherIdentifier = self.contents.get('selectedLauncherIdentifier');
        if 'shouldUseLaunchSchemeArgsEnv' in self.contents.keys():
            self.shouldUseLaunchSchemeArgsEnv = self.contents.get('shouldUseLaunchSchemeArgsEnv');
        if 'buildConfiguration' in self.contents.keys():
            self.buildConfiguration = self.contents.get('buildConfiguration');
    
    def performAction(self, build_system, container, project_constructor, scheme_config_settings):
        if self.root != {}:
            for child in self.root.children:
                project_path = xcrun_helper.resolvePathFromLocation(child.target.ReferencedContainer, container[2].path.base_path, container[2].path.base_path);
                project = project_constructor(project_path);
                
                xcrun_helper.perform_xcodebuild(project, container[1].name, 'test', scheme_config_settings);