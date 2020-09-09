from importlib import import_module
import jpype.imports


def dynamic_import(abs_module_path, class_name):
    module_object = import_module(abs_module_path)

    target_class = getattr(module_object, class_name)

    return target_class


def startJVM(URIToolFilePath, OntologyConverter):
    # Launch the JVM
    # Needs Java13
    # If you have it there's no need to specify jvmpath
    if not jpype.isJVMStarted():
        jpype.startJVM(ignoreUnrecognized=False, classpath=[URIToolFilePath, OntologyConverter], convertStrings=False)


def instantiate_java_code_manipulator(java_path):
    """
    Loads java library for java code manipulation. Library can be accessed via python thanks to jpype.
    Usage:
    JavaCodeMan.generateFromSchema(standard_file_absolute_path)
    JavaCodeMan.writeDownAnnotation(standard_concept: str, reference_concept: str, reference_type: str)
    JavaCodeMan.build()
    :return: Java Code Manipulator
    """

    JavaCodeMan = dynamic_import('com.sprint.annotation.model', 'JavaCodeMan')
    return JavaCodeMan(java_path)


# jvmpath='/usr/lib/jvm/java-13-oracle/bin',
def instantiate_ont_converter():
    Converter = dynamic_import('it.polimi.converter', 'Converter')
    return Converter
