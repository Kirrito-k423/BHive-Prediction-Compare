

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

def dataDictInit()
    dataDict = dataDictClass()

    dataDict.set("unique_revBiblock",set())
    dataDict.set("frequencyRevBiBlock" , defaultdict(int))
    dataDict.set("llvmmcaCyclesRevBiBlock" , defaultdict(int))
    dataDict.set("OSACAmaxCyclesRevBiBlock" , defaultdict(int))
    dataDict.set("OSACACPCyclesRevBiBlock" , defaultdict(int))
    dataDict.set("OSACALCDCyclesRevBiBlock" , defaultdict(int))
    dataDict.set("BhiveCyclesRevBiBlock" , defaultdict(int))
    dataDict.set("accuracyLLVM" , defaultdict(float))
    dataDict.set("accuracyMax" , defaultdict(float))
    dataDict.set("accuracyCP" , defaultdict(float))

    return dataDict