import rdflib
import re
g=rdflib.Graph()
g.load('/Users/safiakalwar/Documents/Polimi-Phd/Sprint/InputData/gtfs.ttl', format="ttl")
prop=rdflib.URIRef('http://xmlns.com/foaf/0.1/LabelProperty')
obj= rdflib.URIRef('http://www.w3.org/2000/01/rdf-schema')

ttlList=[]
flist=[]
for s,p,o in g:
    term = re.findall(r'#(\w+)', s)
    print(term)
    flist.append(term)

mlist=[]
for i in flist:
    for m in i:
        mlist.append(m)
newlist = sorted(set(mlist), key=lambda x:mlist.index(x))
