
from collections import defaultdict
import re
import os
# from rich.progress import track
from tqdm import *
import  time
import sys
from capstone import *
order=0


def LLVM_mca(input):
    global order
    order+=1
    # print("before mca {}/{}\n{}".format(order,num_file,input))
    sys.stdout.flush()
    val=os.popen('echo "'+input+'" | /home/shaojiemike/Install/llvm/bin/llvm-mca -iterations=10000')#  -timeline -show-encoding -all-stats -all-views
    list = val.readlines()
    #Total Cycles:      10005
    # print(list[2])
    regexResult=re.search("Total Cycles:      ([0-9]*)",list[2])
    if regexResult:
        resultCycle=regexResult.group(1)
        print("before mca {}/{} cycle:{}".format(order,num_file,resultCycle))
        return resultCycle
    else:
        print("wrong")
        return -1

def capstone(string):
    CODE = bytes.fromhex(string)
    md = Cs(CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN)
    InputAsm=""
    for i in md.disasm(CODE, 0x1000):
        # print("%s\t%s" %(i.mnemonic, i.op_str))
        InputAsm+="{}\t{}\n".format(i.mnemonic, i.op_str)
    return InputAsm

def capstoneInput(block):
    input2word=""
    for i in range(int((len(block)+1)/9)):
        # print(i)
        input2word+=block[i*9:i*9+2]+block[i*9+2:i*9+4]
        input2word+=block[i*9+4:i*9+6]+block[i*9+6:i*9+8]
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
    global num_file
    fread=open(filename, 'r')
    num_file = sum([1 for i in open(filename, "r")])
    # for line in tqdm(fread,total=num_file):
    for line in fread:
        block=re.search('^(.*),',line).group(1)
        num=re.search(',(.*)$',line).group(1)
        unique_revBiblock.add(block)
        frequencyRevBiBlock[block] += int(num)
        cyclesRevBiBlock[block] = LLVM_mca(capstone(capstoneInput(block)))
    fread.close()


def saveAllResult(taskfilenameprefix,unique_revBiblock,frequencyRevBiBlock,cyclesRevBiBlock):
    writeFilename="{}.LLVM-mca-Pre".format(taskfilenameprefix)
    fwriteblockfreq = open(writeFilename, "w")
    for tmp_block_binary_reverse in unique_revBiblock:
        fwriteblockfreq.writelines(tmp_block_binary_reverse+','+str(frequencyRevBiBlock[tmp_block_binary_reverse])+','+ \
            str(cyclesRevBiBlock[tmp_block_binary_reverse])+"\n")
    fwriteblockfreq.close()

if __name__ == "__main__":
    # taskfilenameprefix="/home/shaojiemike/blockFrequency/tensorflow_41Gdir_00all_skip_2"
    # taskfilenameprefix="/home/shaojiemike/blockFrequency/tensorflow_13G_part_skip_2"
    taskfilenameprefix="/home/shaojiemike/blockFrequency/tensorflow_test_100"
    taskfilenamesubfix="log"
    filename="{}.{}".format(taskfilenameprefix,taskfilenamesubfix)
    unique_revBiblock=set()
    frequencyRevBiBlock = defaultdict(int)
    cyclesRevBiBlock = defaultdict(int)
    readPartFile(unique_revBiblock,frequencyRevBiBlock,cyclesRevBiBlock)
    print("blockSize {} {}".format(len(unique_revBiblock),len(frequencyRevBiBlock)))
    # saveAllResult(taskfilenameprefix,unique_revBiblock,frequencyRevBiBlock,cyclesRevBiBlock)