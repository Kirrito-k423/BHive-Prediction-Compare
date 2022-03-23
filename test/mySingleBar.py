import time
from tsjPython.tsjCommonFunc import *
barTotalNum=dict()
barStartTime=dict()
barBeforeTime=dict()
barName=set()

def is_positive(value):
    value = int(value)
    if value <= 0:
         raise TypeError("%s is an invalid positive int value" % value)
    return True

def barString(name,current=0,total=-1):
    global barBeforeTime,barName,barStartTime,barTotalNum
    retSting=""
    if name not in barName:
        if is_positive(total):
            barName.add(name)
            barBeforeTime[name]=time.time()
            barStartTime[name]=time.time()
            barTotalNum[name]=total
        else:
            return retSting
    elif is_positive(current) and barTotalNum[name]>= current:
        total=barTotalNum[name]
        lastTime=int(time.time()-barBeforeTime[name])
        pastTime=int(time.time()-barStartTime[name])
        barBeforeTime[name]=time.time()
        retSting+="[{}:{:2d}%] > |".format(format(name," <10"),int(100*current/total))  #█
        space='█'
        spaceNum=int(format(100*current/total,'0>2.0f'))
        leftNum=100-spaceNum
        retSting=retSting.ljust(spaceNum+len(retSting),space)
        retSting=retSting.ljust(leftNum+len(retSting),' ')
        hour=pastTime//3600
        minutes=(pastTime-hour*3600)//60
        secends=pastTime%60
        retSting+="| {} [{:0>2d}:{:0>2d}:{:0>2d}]".format(str(current)+"/"+str(total),hour,minutes,secends)
        hour=lastTime//3600
        minutes=(lastTime-hour*3600)//60
        secends=lastTime%60
        retSting+=" {:0>2d}:{:0>2d}:{:0>2d} lastItem".format(hour,minutes,secends)
        return retSting



print(int(time.time()))
name="shijifan"

for i in range(100):
    sleepRandom(2)
    print(barString(name,i,100))

# current=23
# total=24
# pastTime=662
# lastTime=23
# retSting="[{}:{}%] > |".format(format(name," <10"),format(100*current/total,'.1f'))  #█
# space='█'
# spaceNum=int(format(100*current/total,'.0f'))
# leftNum=100-spaceNum
# retSting=retSting.ljust(spaceNum+len(retSting),space)
# retSting=retSting.ljust(leftNum+len(retSting),' ')
# hour=pastTime//3600
# minutes=(pastTime-hour*3600)//60
# secends=pastTime%60

# retSting+="| {} [{:0>2d}:{:0>2d}:{:0>2d}]".format(str(current)+"/"+str(total),hour,minutes,secends)
# hour=lastTime//3600
# minutes=(lastTime-hour*3600)//60
# secends=lastTime%60
# retSting+=" {:0>2d}:{:0>2d}:{:0>2d} lastItem".format(hour,minutes,secends)
# print(retSting)