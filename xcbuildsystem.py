from __future__ import absolute_import
import os
import sys
import importlib
import plistlib

from .xcrun import *
from .xcspec import *

class xcbuildsystem(object):
    
    def __init__(self):
        self.specs = set();
        # loading default specs
        defaults = [
            '../OtherFrameworks/DevToolsCore.framework/Resources/Built-in build phase types.xcspec',
            '../OtherFrameworks/DevToolsCore.framework/Resources/Built-in compilers.pbcompspec',
            '../OtherFrameworks/DevToolsCore.framework/Resources/Built-in file types.pbfilespec',
            '../OtherFrameworks/DevToolsCore.framework/Resources/Built-in languages.pblangspec',
            '../OtherFrameworks/DevToolsCore.framework/Resources/Built-in property condition flavors.xcspec',
            '../OtherFrameworks/DevToolsCore.framework/Resources/Built-in Runtime Systems.pbRTSspec',
            '../OtherFrameworks/DevToolsCore.framework/Resources/Code Sign.xcspec',
            '../OtherFrameworks/DevToolsCore.framework/Resources/Core Build System.xcspec',
            '../OtherFrameworks/DevToolsCore.framework/Resources/External Build System.xcspec',
            '../OtherFrameworks/DevToolsCore.framework/Resources/Jam Build System.xcspec',
            '../OtherFrameworks/DevToolsCore.framework/Resources/Native Build System.xcspec',
            '../OtherFrameworks/DevToolsCore.framework/Resources/Standard file types.pbfilespec',
            '../PlugIns/Xcode3Core.ideplugin/Contents/SharedSupport/Developer/Library/Xcode/Plug-ins/Clang LLVM 1.0.xcplugin/Contents/Resources/Clang LLVM 1.0.xcspec',
            '../PlugIns/Xcode3Core.ideplugin/Contents/SharedSupport/Developer/Library/Xcode/Plug-ins/Clang LLVM 1.0.xcplugin/Contents/Resources/Default Compiler.xcspec',
            '../PlugIns/Xcode3Core.ideplugin/Contents/SharedSupport/Developer/Library/Xcode/Plug-ins/Core Data.xcplugin/Contents/Resources/Core Data.xcspec',
            '../PlugIns/Xcode3Core.ideplugin/Contents/SharedSupport/Developer/Library/Xcode/Plug-ins/CoreBuildTasks.xcplugin/Contents/Resources/CopyPlistFile.xcspec',
            '../PlugIns/Xcode3Core.ideplugin/Contents/SharedSupport/Developer/Library/Xcode/Plug-ins/CoreBuildTasks.xcplugin/Contents/Resources/CopyStringsFile.xcspec',
            '../PlugIns/Xcode3Core.ideplugin/Contents/SharedSupport/Developer/Library/Xcode/Plug-ins/CoreBuildTasks.xcplugin/Contents/Resources/CopyTiffFile.xcspec',
            '../PlugIns/Xcode3Core.ideplugin/Contents/SharedSupport/Developer/Library/Xcode/Plug-ins/CoreBuildTasks.xcplugin/Contents/Resources/Cpp.xcspec',
            '../PlugIns/Xcode3Core.ideplugin/Contents/SharedSupport/Developer/Library/Xcode/Plug-ins/CoreBuildTasks.xcplugin/Contents/Resources/DTrace.xcspec',
            '../PlugIns/Xcode3Core.ideplugin/Contents/SharedSupport/Developer/Library/Xcode/Plug-ins/CoreBuildTasks.xcplugin/Contents/Resources/Iconutil.xcspec',
            '../PlugIns/Xcode3Core.ideplugin/Contents/SharedSupport/Developer/Library/Xcode/Plug-ins/CoreBuildTasks.xcplugin/Contents/Resources/Ld.xcspec',
            '../PlugIns/Xcode3Core.ideplugin/Contents/SharedSupport/Developer/Library/Xcode/Plug-ins/CoreBuildTasks.xcplugin/Contents/Resources/Lex.xcspec',
            '../PlugIns/Xcode3Core.ideplugin/Contents/SharedSupport/Developer/Library/Xcode/Plug-ins/CoreBuildTasks.xcplugin/Contents/Resources/Libtool.xcspec',
            '../PlugIns/Xcode3Core.ideplugin/Contents/SharedSupport/Developer/Library/Xcode/Plug-ins/CoreBuildTasks.xcplugin/Contents/Resources/Lipo.xcspec',
            '../PlugIns/Xcode3Core.ideplugin/Contents/SharedSupport/Developer/Library/Xcode/Plug-ins/CoreBuildTasks.xcplugin/Contents/Resources/LSRegisterURL.xcspec',
            '../PlugIns/Xcode3Core.ideplugin/Contents/SharedSupport/Developer/Library/Xcode/Plug-ins/CoreBuildTasks.xcplugin/Contents/Resources/MiG.xcspec',
            '../PlugIns/Xcode3Core.ideplugin/Contents/SharedSupport/Developer/Library/Xcode/Plug-ins/CoreBuildTasks.xcplugin/Contents/Resources/Nasm.xcspec',
            '../PlugIns/Xcode3Core.ideplugin/Contents/SharedSupport/Developer/Library/Xcode/Plug-ins/CoreBuildTasks.xcplugin/Contents/Resources/OpenCL.xcspec',
            '../PlugIns/Xcode3Core.ideplugin/Contents/SharedSupport/Developer/Library/Xcode/Plug-ins/CoreBuildTasks.xcplugin/Contents/Resources/OSACompile.xcspec',
            '../PlugIns/Xcode3Core.ideplugin/Contents/SharedSupport/Developer/Library/Xcode/Plug-ins/CoreBuildTasks.xcplugin/Contents/Resources/PBXCp.xcspec',
            '../PlugIns/Xcode3Core.ideplugin/Contents/SharedSupport/Developer/Library/Xcode/Plug-ins/CoreBuildTasks.xcplugin/Contents/Resources/ProductTypeValidationTool.xcspec',
            '../PlugIns/Xcode3Core.ideplugin/Contents/SharedSupport/Developer/Library/Xcode/Plug-ins/CoreBuildTasks.xcplugin/Contents/Resources/ResMerger.xcspec',
            '../PlugIns/Xcode3Core.ideplugin/Contents/SharedSupport/Developer/Library/Xcode/Plug-ins/CoreBuildTasks.xcplugin/Contents/Resources/Rez.xcspec',
            '../PlugIns/Xcode3Core.ideplugin/Contents/SharedSupport/Developer/Library/Xcode/Plug-ins/CoreBuildTasks.xcplugin/Contents/Resources/StripSymbols.xcspec',
            '../PlugIns/Xcode3Core.ideplugin/Contents/SharedSupport/Developer/Library/Xcode/Plug-ins/CoreBuildTasks.xcplugin/Contents/Resources/TiffUtil.xcspec',
            '../PlugIns/Xcode3Core.ideplugin/Contents/SharedSupport/Developer/Library/Xcode/Plug-ins/CoreBuildTasks.xcplugin/Contents/Resources/Yacc.xcspec',
            '../PlugIns/Xcode3Core.ideplugin/Contents/SharedSupport/Developer/Library/Xcode/Plug-ins/IBCompilerPlugin.xcplugin/Contents/Resources/AssetCatalogCompiler.xcspec',
            '../PlugIns/Xcode3Core.ideplugin/Contents/SharedSupport/Developer/Library/Xcode/Plug-ins/IBCompilerPlugin.xcplugin/Contents/Resources/IBCompiler.xcspec',
            '../PlugIns/Xcode3Core.ideplugin/Contents/SharedSupport/Developer/Library/Xcode/Plug-ins/IBCompilerPlugin.xcplugin/Contents/Resources/IBPostprocessor.xcspec',
            '../PlugIns/Xcode3Core.ideplugin/Contents/SharedSupport/Developer/Library/Xcode/Plug-ins/IBCompilerPlugin.xcplugin/Contents/Resources/IBStoryboardCompiler.xcspec',
            '../PlugIns/Xcode3Core.ideplugin/Contents/SharedSupport/Developer/Library/Xcode/Plug-ins/IBCompilerPlugin.xcplugin/Contents/Resources/IBStoryboardPostprocessor.xcspec',
            '../PlugIns/Xcode3Core.ideplugin/Contents/SharedSupport/Developer/Library/Xcode/Plug-ins/Metal.xcplugin/Contents/Resources/FileTypes.xcspec',
            '../PlugIns/Xcode3Core.ideplugin/Contents/SharedSupport/Developer/Library/Xcode/Plug-ins/Metal.xcplugin/Contents/Resources/Metal Archiver.xcspec',
            '../PlugIns/Xcode3Core.ideplugin/Contents/SharedSupport/Developer/Library/Xcode/Plug-ins/Metal.xcplugin/Contents/Resources/Metal Compiler.xcspec',
            '../PlugIns/Xcode3Core.ideplugin/Contents/SharedSupport/Developer/Library/Xcode/Plug-ins/Metal.xcplugin/Contents/Resources/Metal Linker.xcspec',
            '../PlugIns/Xcode3Core.ideplugin/Contents/SharedSupport/Developer/Library/Xcode/Plug-ins/XCLanguageSupport.xcplugin/Contents/Resources/Swift.pbfilespec',
            '../PlugIns/Xcode3Core.ideplugin/Contents/SharedSupport/Developer/Library/Xcode/Plug-ins/XCLanguageSupport.xcplugin/Contents/Resources/Swift.xcspec',
            '../PlugIns/Xcode3Core.ideplugin/Contents/SharedSupport/Developer/Library/Xcode/Plug-ins/XCLanguageSupport.xcplugin/Contents/Resources/SwiftBuildSettings.xcspec',
            '../PlugIns/Xcode3Core.ideplugin/Contents/SharedSupport/Developer/Library/Xcode/Plug-ins/XCLanguageSupport.xcplugin/Contents/Resources/SwiftBuildSteps.xcspec',
            '../Plugins/Xcode3Core.ideplugin/Contents/Frameworks/DevToolsCore.framework/Resources/BuiltInBuildPhaseTypes.xcspec',
            '../Plugins/Xcode3Core.ideplugin/Contents/Frameworks/DevToolsCore.framework/Resources/BuiltInCompilers.xcspec',
            '../Plugins/Xcode3Core.ideplugin/Contents/Frameworks/DevToolsCore.framework/Resources/BuiltInFileTypes.xcspec',
            '../Plugins/Xcode3Core.ideplugin/Contents/Frameworks/DevToolsCore.framework/Resources/CodeSign.xcspec',
            '../Plugins/Xcode3Core.ideplugin/Contents/Frameworks/DevToolsCore.framework/Resources/CoreBuildSystem.xcspec',
            '../Plugins/Xcode3Core.ideplugin/Contents/Frameworks/DevToolsCore.framework/Resources/EmbeddedBinaryValidationUtility.xcspec',
            '../Plugins/Xcode3Core.ideplugin/Contents/Frameworks/DevToolsCore.framework/Resources/ExternalBuildSystem.xcspec',
            '../Plugins/Xcode3Core.ideplugin/Contents/Frameworks/DevToolsCore.framework/Resources/InfoPlistUtility.xcspec',
            '../Plugins/Xcode3Core.ideplugin/Contents/Frameworks/DevToolsCore.framework/Resources/JamBuildSystem.xcspec',
            '../Plugins/Xcode3Core.ideplugin/Contents/Frameworks/DevToolsCore.framework/Resources/NativeBuildSystem.xcspec',
            '../Plugins/Xcode3Core.ideplugin/Contents/Frameworks/DevToolsCore.framework/Resources/StandardFileTypes.xcspec',
            
        ];
        for path in defaults:
            spec_list = xcspecLoadFileAtRelativeDeveloperPath(path);
            self.specs.update(spec_list);
        
        # updating specs to point to each other and form inheritence.
        for spec_item in self.specs:
            if spec_item.basedOn != None:
                spec_item.basedOn = self.getSpecForIdentifier(spec_item.basedOn);
    
    
    def getSpecForIdentifier(self, identifier):
        results = self.getSpecForFilter(lambda spec: spec.identifier == identifier);
        if results != None:
            return results[0];
        return results;
    
    def getSpecForFilter(self, filter_func):
        results = filter(filter_func, self.specs);
        if len(results) > 0:
            return results;
        else:
            return None;
    
    def defaultBuildRules(self):
        contents = [];
        build_rules_plist_path = os.path.normpath(os.path.join(xcrun.resolve_developer_path(), '../OtherFrameworks/DevToolsCore.framework/Resources/Built-in build rules.plist'));
        if os.path.exists(build_rules_plist_path) == True:
            # loading spec file
            specNSData, errorMessage = Foundation.NSData.dataWithContentsOfFile_options_error_(build_rules_plist_path, Foundation.NSUncachedRead, None);
            if errorMessage == None:
                specString = Foundation.NSString.alloc().initWithData_encoding_(specNSData, Foundation.NSUTF8StringEncoding);
                if specString != None:
                    contents = specString.propertyList();
                else:
                    print 'Could not load string from data';
            else:
                print errorMessage;
        else:
            print 'path does not exist!';
        
        return contents;
    
    def getCompilerForFileReference(self, file_ref):
        file_ref_spec = self.getSpecForIdentifier(file_ref.ftype);
        file_types = file_ref_spec.inheritedTypes();
        
        compiler_identifier = '';
        for rule in self.defaultBuildRules():
            if rule['FileType'] in file_types:
                compiler_identifier = rule['CompilerSpec'];
                break;
        
        compiler = self.getSpecForIdentifier(compiler_identifier);
        