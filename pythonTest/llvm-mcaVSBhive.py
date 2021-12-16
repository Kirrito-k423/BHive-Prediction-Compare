
from collections import defaultdict
import re
import os
# from rich.progress import track
from tqdm import *
import  time
import sys
from capstone import *
BHiveCount=10000
order=0


def LLVM_mca(input):
    global order
    # order+=1
    # print("before mca {}/{}\n{}".format(order,num_file,input))
    sys.stdout.flush()
    val=os.popen('echo "'+input+'" | /home/shaojiemike/Install/llvm/bin/llvm-mca -iterations=10000')#  -timeline -show-encoding -all-stats -all-views
    list = val.readlines()
    #Total Cycles:      10005
    # print(list[2])
    regexResult=re.search("Total Cycles:      ([0-9]*)",list[2])
    if regexResult:
        resultCycle=regexResult.group(1)
        # print("mca {}/{} cycle:{}".format(order,num_file,resultCycle))
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


def BHive(input,showinput,trytime):
    global order,BHiveCount
    if trytime==0:
        order=order+1
    elif trytime>5:
        print("trytime {}/{} {}".format(order,num_file,input))
        print("trytime {}/{} {}".format(order,num_file,showinput))
        print("trytime > 5")
        return -1
    # print("before main {}/{} {}".format(order,num_file,input))
    # print("before main {}/{} {}".format(order,num_file,showinput))
    sys.stdout.flush()
    # begin_time=time.time()
    val=os.popen('echo '+password+' | sudo -S /home/shaojiemike/test/bhive-re/bhive/main '+str(BHiveCount)+input)
    # call_main_time=time.time()-begin_time
    # print("after  main {}/{} {}s".format(order,num_file,call_main_time))
    # sys.stdout.flush()
    list = val.readlines()
    # real_main_time=time.time()-begin_time
    # print("real  main {}/{} {}s".format(order,num_file,real_main_time))
    # if real_main_time>20:
    #     print("Attention!")
    # sys.stdout.flush()
    # print(list[-1])
    regexResult=re.search("core cyc: ([0-9]*)",list[-1])
    if regexResult:
        resultCycle=regexResult.group(1)
        # print(resultCycle)
        return resultCycle
    else:
        # print("trytime: {} {}".format(trytime ,list[-1]))
        # print("else {}/{} {}".format(order,num_file,input))
        # print("else {}/{} {}".format(order,num_file,showinput))
        return BHive(input,showinput,trytime+1)

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

def BHiveInputDel0x(block):
    # print(block)
    # print((len(block)+1)/9)
    input2word=""
    for i in range(int((len(block)+1)/9)):
        # print(i)
        input2word+=" "+block[i*9:i*9+2]+" "+block[i*9+2:i*9+4]
        input2word+=" "+block[i*9+4:i*9+6]+" "+block[i*9+6:i*9+8]
    # print(input2word)
    return input2word

def calculateAccuracy(accurateCycles,predictionCycles):
    if accurateCycles == -1 or predictionCycles == -1:
        return 0
    else:
        # print("{} {}".format(accurateCycles,predictionCycles))
        return int(predictionCycles)/int(accurateCycles)

def readPartFile(unique_revBiblock,frequencyRevBiBlock,llvmmcaCyclesRevBiBlock,BhiveCyclesRevBiBlock,accuracy):
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
    for line in tqdm(fread,total=num_file):
    # for line in fread:
        block=re.search('^(.*),',line).group(1)
        num=re.search(',(.*)$',line).group(1)
        unique_revBiblock.add(block)
        frequencyRevBiBlock[block] += int(num)
        BhiveCyclesRevBiBlock[block] = BHive(BHiveInput(block),BHiveInputDel0x(block),0)
        llvmmcaCyclesRevBiBlock[block] = LLVM_mca(capstone(capstoneInput(block)))
        accuracy[block]= calculateAccuracy(BhiveCyclesRevBiBlock[block],llvmmcaCyclesRevBiBlock[block])
    fread.close() 


def saveAllResult(taskfilenameprefix,unique_revBiblock,frequencyRevBiBlock,llvmmcaCyclesRevBiBlock,BhiveCyclesRevBiBlock,accuracy):
    writeFilename="{}_count{}.llvmmcaVSBHive".format(taskfilenameprefix,BHiveCount)
    fwriteblockfreq = open(writeFilename, "w")
    validNum=0
    unvalidNum=0
    totalAccuracy=0.0
    for tmp_block_binary_reverse in unique_revBiblock:
        fwriteblockfreq.writelines(tmp_block_binary_reverse+','+str(frequencyRevBiBlock[tmp_block_binary_reverse])+','+ \
            str(llvmmcaCyclesRevBiBlock[tmp_block_binary_reverse])+' _ '+
            str(BhiveCyclesRevBiBlock[tmp_block_binary_reverse])+' _ '+
            str(accuracy[tmp_block_binary_reverse])+"\n")
        if accuracy[tmp_block_binary_reverse] != 0:
            validNum+=frequencyRevBiBlock[tmp_block_binary_reverse]
            totalAccuracy+=frequencyRevBiBlock[tmp_block_binary_reverse]*accuracy[tmp_block_binary_reverse]
        else:
            unvalidNum+=1
    fwriteblockfreq.writelines("validTotalNum & unvalidBlockNum :"+str(validNum)+" "+str(unvalidNum)+"\n")
    fwriteblockfreq.writelines("avg accuracy is "+str(totalAccuracy/validNum))
    print("avg accuracy is "+str(totalAccuracy/validNum)) 
    fwriteblockfreq.close()

if __name__ == "__main__":
    global filename,password
    print("请输入sudo密码")
    password=input("password:")
    taskfilenameprefix="/home/shaojiemike/blockFrequency/tensorflow_41Gdir_00all_skip_2"
    # taskfilenameprefix="/home/shaojiemike/blockFrequency/tensorflow_13G_part_skip_2"
    # taskfilenameprefix="/home/shaojiemike/blockFrequency/tensorflow_test"
    taskfilenamesubfix="log"
    filename="{}.{}".format(taskfilenameprefix,taskfilenamesubfix)
    unique_revBiblock=set()
    frequencyRevBiBlock = defaultdict(int)
    llvmmcaCyclesRevBiBlock = defaultdict(int)
    BhiveCyclesRevBiBlock = defaultdict(int)
    accuracy = defaultdict(float)
    readPartFile(unique_revBiblock,frequencyRevBiBlock,llvmmcaCyclesRevBiBlock,BhiveCyclesRevBiBlock,accuracy)
    print("blockSize {} {}".format(len(unique_revBiblock),len(frequencyRevBiBlock)))
    saveAllResult(taskfilenameprefix,unique_revBiblock,frequencyRevBiBlock,llvmmcaCyclesRevBiBlock,BhiveCyclesRevBiBlock,accuracy)
