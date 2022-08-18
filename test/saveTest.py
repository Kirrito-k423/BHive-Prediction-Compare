


def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError

import json
import numpy as np
from icecream import ic
fineness = 100 # xy轴的粒度
XYMax=10
scale = fineness/XYMax
X, Y = np.around(np.mgrid[0:XYMax:complex(0, fineness), 0:XYMax:complex(0, fineness)], decimals=1)
y=[11,22,33]
z=[1.1,2.2,3.3]
saveDict={
    "x":X.tolist(),
    "y":y,
    "z":z
    }
ic(saveDict)
wf = open("saveTest.json", 'w',encoding='utf-8')      
json.dump(obj=saveDict, fp=wf)
wf.close()


# read
rf = open("saveTest.json",'r',encoding='utf-8')
readDict=json.load(fp=rf)
rf.close()
print(readDict['x'][2])
print(readDict['z'][1])