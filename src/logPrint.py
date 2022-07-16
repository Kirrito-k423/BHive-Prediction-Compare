
from multiBar import time2String
import time
from tsjPython.tsjCommonFunc import *

def timeBeginPrint(Msg):
    processBeginTime=time.time()
    colorPrint("\n\rstart {} at: {}".format(Msg,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),"magenta")
    return processBeginTime

def timeEndPrint(Msg, beginTime):
    colorPrint("wait {} to finish {} at: {}".format(time2String(int(time.time()-beginTime)),Msg,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),"magenta")