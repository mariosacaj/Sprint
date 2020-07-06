import subprocess
from annotator.exceptions import *
import json
from annotator.tool.FileManager.ReadFiles import xsd2str as x2s


def owl2json(ref_path):
    process = subprocess.run(['java', '-jar', 'owl2vowl.jar','-echo', '-file', ref_path],
                             stdout=subprocess.PIPE,
                             universal_newlines=True)

    if process.returncode is not 0:
        raise ReferenceError('Could Not Convert')

    st = process.stdout

    st = st[st.find("{"):st.rfind("}")+1]

    return json.loads(st)

def xsd2str(std_path):
    return x2s(std_path)
