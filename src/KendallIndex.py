

def calculateKendallIndex(dataDict):
    concordantPairsNum=0
    disConcordantPairsNum=0
    concordantPairsNumOfBaseline=0
    disConcordantPairsNumOfBaseline=0

    for key, value in dataDict.dataDict.items():
        globals()[key]=value 


    for first_block_binary_reverse in unique_revBiblock:
        for second_block_binary_reverse in unique_revBiblock:
            if BhiveCyclesRevBiBlock[first_block_binary_reverse]==-1 or \
                BhiveCyclesRevBiBlock[second_block_binary_reverse]==-1 or \
                accuracyLLVM[first_block_binary_reverse] <= 0 or \
                accuracyLLVM[second_block_binary_reverse] <= 0 or \
                first_block_binary_reverse==second_block_binary_reverse:
                continue
            if BhiveCyclesRevBiBlock[first_block_binary_reverse] >= BhiveCyclesRevBiBlock[second_block_binary_reverse]:
                if llvmmcaCyclesRevBiBlock[first_block_binary_reverse] >= llvmmcaCyclesRevBiBlock[second_block_binary_reverse]:
                    concordantPairsNum += 1
                else:
                    disConcordantPairsNum += 1
                if BaselineCyclesRevBiBlock[first_block_binary_reverse] >= BaselineCyclesRevBiBlock[second_block_binary_reverse]:
                    concordantPairsNumOfBaseline += 1
                else:
                    disConcordantPairsNumOfBaseline += 1
            else:
                if llvmmcaCyclesRevBiBlock[first_block_binary_reverse] < llvmmcaCyclesRevBiBlock[second_block_binary_reverse]:
                    concordantPairsNum += 1
                else:
                    disConcordantPairsNum += 1
                if BaselineCyclesRevBiBlock[first_block_binary_reverse] < BaselineCyclesRevBiBlock[second_block_binary_reverse]:
                    concordantPairsNumOfBaseline += 1
                else:
                    disConcordantPairsNumOfBaseline += 1

    KendallIndex = (concordantPairsNum - disConcordantPairsNum)*1.0/(concordantPairsNum + disConcordantPairsNum)
    baselineKendallIndex = (concordantPairsNumOfBaseline - disConcordantPairsNumOfBaseline)*1.0 /  (concordantPairsNumOfBaseline + disConcordantPairsNumOfBaseline)
    return [KendallIndex, baselineKendallIndex]


