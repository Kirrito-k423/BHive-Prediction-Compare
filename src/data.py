from collections import defaultdict
from multiprocessing import Queue
from logPrint import *
import sys
import global_variable as glv

class dataDictClass():
    def __init__(self):
        """在主模块初始化"""
        self.dataDict = {}

    def set(self, name, value):
        """设置"""
        try:
            self.dataDict[name] = value
            return True
        except KeyError:
            return False

    def get(self, name):
        """取值"""
        try:
            return self.dataDict[name]
        except KeyError:
            return "Not Found"

def dataDictInit():
    dataDict = dataDictClass()

    dataDict.set("unique_revBiblock",set())
    dataDict.set("frequencyRevBiBlock" , defaultdict(int))
    dataDict.set("llvmmcaCyclesRevBiBlock" , defaultdict(int))
    dataDict.set("BaselineCyclesRevBiBlock" , defaultdict(int))
    # dataDict.set("OSACAmaxCyclesRevBiBlock" , defaultdict(int))
    # dataDict.set("OSACACPCyclesRevBiBlock" , defaultdict(int))
    # dataDict.set("OSACALCDCyclesRevBiBlock" , defaultdict(int))
    dataDict.set("BhiveCyclesRevBiBlock" , defaultdict(int))
    dataDict.set("accuracyLLVM" , defaultdict(float))
    dataDict.set("accuracyLLVM_MuliplyFrequency" , defaultdict(float))
    dataDict.set("accuracyBaseline" , defaultdict(float))
    dataDict.set("accuracyBaseline_MuliplyFrequency" , defaultdict(float))
    # dataDict.set("accuracyMax" , defaultdict(float))
    # dataDict.set("accuracyCP" , defaultdict(float))
    return dataDict

def queueDictInit(dataDict):
    queueDict = dataDictClass()

    for key in dataDict.dataDict:
        ic(key)
        queueDict.set(key, Queue())
    return queueDict

def readDictFromJson(taskName):
    historyDict = dataDictInit()
    if glv._get("useBhiveHistoryData")=="no" and glv._get("useBaselineHistoryData")=="no" and glv._get("useLLVMHistoryData")=="no":
        ic("hb hm lv is all NO!")
        glv._set("isPageExisted","no")
        return historyDict
    if not isExcelPageExisted(taskName):
        ic(taskName,"is Not Existed!")
        glv._set("isPageExisted","no")
        return historyDict
    ic(taskName,"is Existed!")
    glv._set("isPageExisted","yes")
    beginTime=timeBeginPrint(sys._getframe().f_code.co_name)
    import json
    rf = open(glv._get("HistoryDataFile")+"_"+taskName)      # 将文件中的数据反序列化成内置的dict类型
    historyDict.dataDict=json.load(fp=rf)
    timeEndPrint(sys._getframe().f_code.co_name,beginTime)
    return historyDict

def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError
def saveDict2Json(taskName,dataDict):
    beginTime=timeBeginPrint(sys._getframe().f_code.co_name)
    import json
    wf = open(glv._get("excelOutPath")+"_"+taskName, 'w')  # 将dict类型对象序列化存储到文件中           
    json.dump(obj=dataDict, fp=wf, default=set_default)
    timeEndPrint(sys._getframe().f_code.co_name,beginTime)
    