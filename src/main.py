

import config  # 加载配置
import global_variable as glv
from input_process import inputParameters, isIceEnable
from terminal_command import checkFile
from excel import excelGraphInit


def main():
    ## icecream & input
    args=inputParameters()
    isIceEnable(args.debug)
    checkFile(glv._get("taskfilePath"))
    wb = excelGraphInit()
    
    isFirstSheet=1
    taskList = glv._get("taskList")
    for taskKey, taskName in taskList.items():
        filename=pasteFullFileName(taskKey)
        dataDict = dataDictInit()

        unique_revBiblock=readPartFile(taskName, dataDict)
        print("blockSize {} {}".format(len(dataDict.get("unique_revBiblock")),len(dataDict.get("frequencyRevBiBlock"))))
        [llvmerror,osacaerror] = add2Excel(wb,taskName,isFirstSheet.dataDict)
        excelGraphAdd(wb,taskName,llvmerror,osacaerror)
        isFirstSheet=0
    excelGraphBuild(wb)
if __name__ == "__main__":
    main()