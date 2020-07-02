import subprocess
from SPRINTcode.Exceptions import StandardError
import xml.dom.minidom as xp


def conversion(output_path, schema_path, jaxb_path, URIConverterPath):
    process = subprocess.run([jaxb_path, '-nv', '-d', output_path, '-no-header', schema_path],
                             stdout=subprocess.PIPE,
                             universal_newlines=True)

    ### DEBUG, please remove
    stdout = process.stdout.split('\n')
    for line in stdout:
        print(line.strip())
    ### END DEBUG

    if process.returncode is not 0:
        raise StandardError('Could Not Convert')

    docread = xp.parse(schema_path)
    elem = docread.getElementsByTagName('xsd:schema')
    package_uri = elem[0].getAttribute('targetNamespace')

    process = subprocess.run(['java', '-jar', URIConverterPath, package_uri],
                             stdout=subprocess.PIPE,
                             universal_newlines=True)

    ### DEBUG, please remove
    stdout = process.stdout.split('\n')
    for line in stdout:
        print(line.strip())
    ### END DEBUG

    if process.returncode is not 0:
        raise StandardError('Could Not Retrieve Package Path')

    return stdout[0]
