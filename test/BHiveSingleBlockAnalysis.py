import re
import sys
import os
import math

BHiveCount=10000

def checkBHiveResultStable(password,input,showinput,trytime):
    global BHiveCount
    order=0 
    if trytime==0:
        order=order+1
    elif trytime>5:
        return -1
    sys.stdout.flush()
    val=os.popen('echo '+password+' | sudo -S /home/shaojiemike/test/bhive-re/bhive/main '+str(BHiveCount)+input)
    list = val.readlines()
    if list is None or len(list)==0:
        regexResult=None
    else:
        regexResult=re.search("core cyc: ([0-9]*)",list[-1])
    if regexResult:
        resultCycle=regexResult.group(1)
        return resultCycle
    else:
        return checkBHiveResultStable(password,input,showinput,trytime+1)

def BHiveInput(block):
    # print(block)
    # print((len(block)+1)/9)
    input2word=""
    for i in range(int((len(block)+1)/9)):
        # print(i)
        input2word+=" 0x"+block[i*9:i*9+2]+" 0x"+block[i*9+2:i*9+4]
        input2word+=" 0x"+block[i*9+4:i*9+6]+" 0x"+block[i*9+6:i*9+8]
    # print(input2word)
    return input2word

input1="c10240b9 e003012a 000018ca 00fc41d3 d6120091 c10240b9 e003012a 000018ca 00fc41d3 d6120091 c10240b9 e003012a 000018ca 00fc41d3 668a41f9 e70317aa a05f40f9 e403152a e00f00f9 c60206cb a05b40f9 c6fc4293 e00b00f9 c57c4092 a3e340b9 a504058b a15340f9 e20319aa a05740f9 850f058b fb6b00a9 f403062a a86700f9"

list1=input1.split(" ")
tmp=""
for input in list1:
    print("{} {}".format(int(checkBHiveResultStable("acsa1411",BHiveInput(input),"2",0))/BHiveCount,math.ceil(len(input)/9)))
print("------------------------------")
for input in list1:
    tmp+=input+" "
    print("{} {}".format(int(checkBHiveResultStable("acsa1411",BHiveInput(tmp),"2",0))/BHiveCount,math.ceil(len(tmp)/9)))