

import config  # 加载配置
from config import pasteFullFileName
import global_variable as glv
from input_process import inputParameters, isIceEnable
from terminal_command import checkFile
from heatmap import generateHeatmapPic
from excel import *
from data import dataDictInit,readDictFromJson,saveDict2Json
from multiProcess import *
import time

def main():
    ## icecream & input
    args=inputParameters()
    isIceEnable(args.debug)
    checkFile(glv._get("taskfilePath"))
    wb = excelGraphInit()
    
    isFirstSheet=1
    taskList = glv._get("taskList")
    processBeginTime=time.time()
    colorPrint("\n\rstart multiple taskList at: {}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),"magenta")
    
    for taskKey, taskName in taskList.items():
        # glv._set("filename",pasteFullFileName(taskKey))
        filename=pasteFullFileName(taskKey)
        ic(filename)
        dataDict = dataDictInit()
        glv._set("historyDict",readDictFromJson(taskName))
        

        dataDict = readPartFile(taskName,filename, dataDict)
        saveDict2Json(taskName,dataDict.dataDict)
        print("blockSize {} {}".format(len(dataDict.get("unique_revBiblock")),len(dataDict.get("frequencyRevBiBlock"))))
        generateHeatmapPic(taskName,dataDict)

        [llvmerror,baselineError,validBlockNum,validInstructionNum] = add2Excel(wb,taskName,isFirstSheet,dataDict)
        excelGraphAdd(wb,taskName,llvmerror,baselineError,validBlockNum,validInstructionNum)
        isFirstSheet=0
    excelGraphBuild(wb,processBeginTime)
    colorPrint("wait {} to finish taskList at: {}".format(time2String(int(time.time()-processBeginTime)),time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),"magenta")
if __name__ == "__main__":
    main()