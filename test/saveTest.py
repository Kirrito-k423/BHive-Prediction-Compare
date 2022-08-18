


def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError

import json
x=[1,2,3]
y=[11,22,33]
z=[1.1,2.2,3.3]
saveDict={
    "x":x,
    "y":y,
    "z":z
    }
wf = open("saveTest.json", 'w',encoding='utf-8')      
json.dump(obj=saveDict, fp=wf)
wf.close()


# read
rf = open("saveTest.json",'r',encoding='utf-8')
readDict=json.load(fp=rf)
rf.close()
print(readDict['x'][2])
print(readDict['z'][1])