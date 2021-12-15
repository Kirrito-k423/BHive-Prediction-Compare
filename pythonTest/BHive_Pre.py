
from collections import defaultdict
import re
import os
# from rich.progress import track
from tqdm import *
import  time

def BHive(input):
    val=os.popen('sudo /home/shaojiemike/test/bhive-re/bhive/main'+input)
    list = val.readlines()
    # print(list[-1])
    regexResult=re.search("core cyc: ([0-9]*)",list[-1])
    if regexResult:
        resultCycle=regexResult.group(1)
        # print(resultCycle)
        return resultCycle
    else:
        return -1

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

def readPartFile(unique_revBiblock,frequencyRevBiBlock,cyclesRevBiBlock):
    # print(filename)
    # with open(filename, 'r') as f:#with语句自动调用close()方法
    #     line = f.readline()
    #     while line:
    #         # print(re.search('^(.*),',line).group(1))
    #         # print(re.search(',(.*)$',line).group(1))
    #         block=re.search('^(.*),',line).group(1)
    #         num=re.search(',(.*)$',line).group(1)
    #         unique_revBiblock.add(block)
    #         frequencyRevBiBlock[block] += int(num)
    #         cyclesRevBiBlock[block] = BHive(BHiveInput(block))
    #         line = f.readline()
    fread=open(filename, 'r')
    num_file = sum([1 for i in open(filename, "r")])
    for line in tqdm(fread,total=num_file):
        block=re.search('^(.*),',line).group(1)
        num=re.search(',(.*)$',line).group(1)
        unique_revBiblock.add(block)
        frequencyRevBiBlock[block] += int(num)
        cyclesRevBiBlock[block] = BHive(BHiveInput(block))
    fread.close()


def saveAllResult(taskfilenameprefix,unique_revBiblock,frequencyRevBiBlock,cyclesRevBiBlock):
    writeFilename="{}.BHivePre".format(taskfilenameprefix)
    fwriteblockfreq = open(writeFilename, "w")
    for tmp_block_binary_reverse in unique_revBiblock:
        fwriteblockfreq.writelines(tmp_block_binary_reverse+','+str(frequencyRevBiBlock[tmp_block_binary_reverse])+','+ \
            str(cyclesRevBiBlock[tmp_block_binary_reverse])+"\n")
    fwriteblockfreq.close()

if __name__ == "__main__":
    global filename
    taskfilenameprefix="/home/shaojiemike/blockFrequency/tensorflow_41Gdir_00all_skip_2"
    # taskfilenameprefix="/home/shaojiemike/blockFrequency/tensorflow_test"
    taskfilenamesubfix="log"
    filename="{}.{}".format(taskfilenameprefix,taskfilenamesubfix)
    unique_revBiblock=set()
    frequencyRevBiBlock = defaultdict(int)
    cyclesRevBiBlock = defaultdict(int)
    readPartFile(unique_revBiblock,frequencyRevBiBlock,cyclesRevBiBlock)
    print("blockSize {} {}".format(len(unique_revBiblock),len(frequencyRevBiBlock)))
    saveAllResult(taskfilenameprefix,unique_revBiblock,frequencyRevBiBlock,cyclesRevBiBlock)