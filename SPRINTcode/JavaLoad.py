from importlib import import_module
import jpype.imports


def dynamic_import(abs_module_path, class_name):
    module_object = import_module(abs_module_path)

    target_class = getattr(module_object, class_name)

    return target_class


def instantiate_java_code_manipulator(java_path, URIToolFilePath):
    """
    Loads java library for java code manipulation. Library can be accessed via python thanks to jpype.
    Usage:
    JavaCodeMan.generateFromSchema(standard_file_absolute_path)
    JavaCodeMan.writeDownAnnotation(standard_concept: str, reference_concept: str, reference_type: str)
    JavaCodeMan.build()
    :return: Java Code Manipulator
    """

    # Launch the JVM
    # Needs Java13
    # If you have it there's no need to specify jvmpath
    jpype.startJVM(jvmpath='/Library/Java/JavaVirtualMachines/openjdk.jdk/Contents/Home/lib/libjli.dylib',
                   ignoreUnrecognized=False, classpath=[URIToolFilePath], convertStrings=False)

    JavaCodeMan = dynamic_import('com.sprint.annotation.model', 'JavaCodeMan')
    return JavaCodeMan(java_path)
