import subprocess
from SPRINTcode.Exceptions.Exceptions import StandardError


def conversion(output_path, schema_path, jaxb_path):
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
