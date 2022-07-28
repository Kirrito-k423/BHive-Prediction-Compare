from logPrint import *

def calculateKendallIndex(dataDict):
    processBeginTime=timeBeginPrint("calculateKendallIndex")
    concordantPairsNum=0
    disConcordantPairsNum=0
    concordantPairsNumOfBaseline=0
    disConcordantPairsNumOfBaseline=0

    for key, value in dataDict.dataDict.items():
        globals()[key]=value 


    for first_block_binary_reverse in unique_revBiblock:
        tmpFirstBhive=BhiveCyclesRevBiBlock[first_block_binary_reverse]
        tmpFirstBaseline = BaselineCyclesRevBiBlock[first_block_binary_reverse]
        tmpFirstLLVM = llvmmcaCyclesRevBiBlock[first_block_binary_reverse]
        if tmpFirstBhive==-1 or \
                accuracyLLVM[first_block_binary_reverse] <= 0:
                continue
        for second_block_binary_reverse in unique_revBiblock:
            tmpSecondBhive=BhiveCyclesRevBiBlock[second_block_binary_reverse]
            if first_block_binary_reverse==second_block_binary_reverse or \
                tmpSecondBhive ==-1 or \
                accuracyLLVM[second_block_binary_reverse] <= 0 :
                continue
            if tmpFirstBhive >= tmpSecondBhive:
                if tmpFirstLLVM >= llvmmcaCyclesRevBiBlock[second_block_binary_reverse]:
                    concordantPairsNum += 1
                else:
                    disConcordantPairsNum += 1
                if tmpFirstBaseline >= BaselineCyclesRevBiBlock[second_block_binary_reverse]:
                    concordantPairsNumOfBaseline += 1
                else:
                    disConcordantPairsNumOfBaseline += 1
            else:
                if tmpFirstLLVM < llvmmcaCyclesRevBiBlock[second_block_binary_reverse]:
                    concordantPairsNum += 1
                else:
                    disConcordantPairsNum += 1
                if tmpFirstBaseline < BaselineCyclesRevBiBlock[second_block_binary_reverse]:
                    concordantPairsNumOfBaseline += 1
                else:
                    disConcordantPairsNumOfBaseline += 1

    KendallIndex = (concordantPairsNum - disConcordantPairsNum)*1.0/(concordantPairsNum + disConcordantPairsNum)
    baselineKendallIndex = (concordantPairsNumOfBaseline - disConcordantPairsNumOfBaseline)*1.0 /  (concordantPairsNumOfBaseline + disConcordantPairsNumOfBaseline)
    timeEndPrint("calculateKendallIndex",processBeginTime)
    return [KendallIndex, baselineKendallIndex]


