import subprocess
from SPRINTcode.path import *


class ConversionException(Exception):
    pass


outputPath = standardsInput
schemaPath = standardsInput + sourcefile
process = subprocess.run(['../jaxb-ri/bin/xjc.sh', '-nv', '-d', outputPath, schemaPath],
                         stdout=subprocess.PIPE,
                         universal_newlines=True)
if process.returncode is not 0:
    raise ConversionException('Could Not Convert')
stdout = process.stdout.split('\n')
# Fetch output
for line in stdout:
    print(line.strip())
