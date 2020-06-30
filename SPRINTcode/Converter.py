import os
from importlib import import_module
# Allow Java modules to be imported
import jpype.imports

standardInput = os.getcwd() + '/data/standard/'
referenceInput = os.getcwd() + '/data/reference/'
output_path = os.getcwd() + '/data/output_map/'
java_path = os.getcwd() + '/data/javaclass/'
modelpath = os.getcwd() + '/data/model/GoogleNews-vectors-negative300.bin'
jaxb_path = 'jaxb-ri/bin/xjc.sh'
source_rw = 's_SumArray3.csv'
target_rw = 't_SumArray3.csv'
write_pathVecRaw = 'SumVecRaw.csv'
write_pathVecThr = 'SumVecThr.csv'
write_pathVecOrgRaw = 'SumVecOrgRaw.csv'
write_pathVecOrgThr = 'SumVecOrgThr.csv'
readpathCompound = 'SumVecOrgThr.csv'
writepathCompound = 'Sumst_MatchCount.csv'
URIToolFilePath = os.getcwd() + '/URIConverterTool.jar'
standard_file = 'StructuralModel-XSD/GeoInfra/Transportation.xsd'


def dynamic_import(abs_module_path, class_name):
    module_object = import_module(abs_module_path)

    target_class = getattr(module_object, class_name)

    return target_class


# Import all standard Java types into the global scope
# Import each of the decorators into the global scope

# Launch the JVM
# Needs Java13
# If you have it there's no need to specify jvmpath
jpype.startJVM(jvmpath='/Library/Java/JavaVirtualMachines/openjdk.jdk/Contents/Home/lib/libjli.dylib',
               ignoreUnrecognized=False, classpath=['URIConverterTool.jar'], convertStrings=False)

JavaCodeModel = dynamic_import('com.sprint.annotation.model', 'JavaCodeModel')
jcm = JavaCodeModel(standardInput + standard_file, java_path)
print(jcm.test())
# jcm.setUri('org.pts_fsm.domainmodel._2015._10._29.transportation')
pass
