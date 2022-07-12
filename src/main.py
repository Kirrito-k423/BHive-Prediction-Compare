

import config  # 加载配置
from config import pasteFullFileName
import global_variable as glv
from input_process import inputParameters, isIceEnable
from terminal_command import checkFile
from heatmap import generateHeatmapPic
from excel import *
from data import dataDictInit
from multiProcess import *

def main():
    ## icecream & input
    args=inputParameters()
    isIceEnable(args.debug)
    checkFile(glv._get("taskfilePath"))
    wb = excelGraphInit()
    
    isFirstSheet=1
    taskList = glv._get("taskList")
    for taskKey, taskName in taskList.items():
        # glv._set("filename",pasteFullFileName(taskKey))
        filename=pasteFullFileName(taskKey)
        ic(filename)
        dataDict = dataDictInit()

        dataDict = readPartFile(taskName,filename, dataDict)
        print("blockSize {} {}".format(len(dataDict.get("unique_revBiblock")),len(dataDict.get("frequencyRevBiBlock"))))
        generateHeatmapPic(taskName,dataDict)
        [llvmerror,osacaerror] = add2Excel(wb,taskName,isFirstSheet,dataDict)
        excelGraphAdd(wb,taskName,llvmerror,osacaerror)
        isFirstSheet=0
    excelGraphBuild(wb)
if __name__ == "__main__":
    main()