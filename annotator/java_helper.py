from importlib import import_module
import jpype.imports

from Sprint.settings import ONT_TOOL_PATH, ANNOTATOR_TOOL_PATH


def dynamic_import(abs_module_path, class_name):
    module_object = import_module(abs_module_path)

    target_class = getattr(module_object, class_name)

    return target_class


def startJVM():
    # Launch the JVM
    # Needs Java13
    # If you have it there's no need to specify jvmpath
    if not jpype.isJVMStarted():
        jpype.startJVM(ignoreUnrecognized=False, classpath=[ANNOTATOR_TOOL_PATH, ONT_TOOL_PATH], convertStrings=False)

    # jvmpath='/usr/lib/jvm/java-13-oracle/bin'

def instantiate_java_code_manipulator(java_path):
    """
    Loads java library for java code manipulation. Library can be accessed via python thanks to jpype.
    Usage:
    JavaCodeMan.generateFromSchema(standard_file_absolute_path)
    JavaCodeMan.writeDownAnnotation(standard_concept: str, reference_concept: str, reference_type: str)
    JavaCodeMan.build()
    :return: Java Code Manipulator
    """
    startJVM()
    JavaCodeMan = dynamic_import('com.sprint.annotation.model', 'JavaCodeMan')
    return JavaCodeMan(java_path)


def instantiate_ont_converter():
    """
    Convert turtle (TTL) standards into XSD/RDF standards (with OWL semantics). Needed for GUI
    :return: Ontology Converter
    """
    startJVM()
    Converter = jpype.JPackage('it').polimi.converter.Converter
    return Converter
