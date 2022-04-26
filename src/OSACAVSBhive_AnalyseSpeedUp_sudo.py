
from collections import defaultdict
import re
import os
from rich.progress import track
from rich.progress import Progress
from tqdm import *
import  time
import sys
from capstone import *
from multiprocessing import Process, Queue


BHiveCount=10000
ProcessNum=40

def OSACA(inputFile,maxOrCP):
    val=os.popen('/home/shaojiemike/test/OSACA/osacaEnv/bin/osaca --arch TSV110 '+str(inputFile))#  -timeline -show-encoding -all-stats -all-views
    list = val.readlines()
    for listObj in list[20:]:
        # print(listObj)
        regexResult=re.search("max_tp_sum:([.0-9]*),min_tp_sum:([.0-9]*),avg_tp_sum:([.0-9]*),cp_sum:([.0-9]*)",listObj)# 需要修改osaca来有个标记位匹配
        if regexResult:
            maxresultCycle=regexResult.group(1)
            minresultCycle=regexResult.group(2)
            avgresultCycle=regexResult.group(3)
            CPresultCycle=regexResult.group(4)
            # print("before mca {}/{} cycle:{}".format(order,num_file,resultCycle))
            # print("  maxresultCycle :{}".format(maxresultCycle))
            if maxOrCP == "max":
                return maxresultCycle
            elif maxOrCP == "CP":
                return CPresultCycle
            else:
                return -1
    # print("  wrong")
    return -1

def saveOSACAInput2File(InputAsmList,rank):
    writeFilename="{}.OSACAInputTmpAsmBlockRank{}".format(taskfilenameprefix,rank)
    fwriteblockfreq = open(writeFilename, "w")
    for tmp_InputAsmList in InputAsmList:
        fwriteblockfreq.writelines(tmp_InputAsmList)
    fwriteblockfreq.close()
    return writeFilename

def capstoneList(string):
    CODE = bytes.fromhex(string)
    md = Cs(CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN)
    InputAsmList=[]
    for i in md.disasm(CODE, 0x1000):
        # print("%s\t%s" %(i.mnemonic, i.op_str))
        InputAsmList.append("{}\t{}\n".format(i.mnemonic, i.op_str))
    return InputAsmList

def capstoneInput(block):
    input2word=""
    for i in range(int((len(block)+1)/9)):
        # print(i)
        input2word+=block[i*9:i*9+2]+block[i*9+2:i*9+4]
        input2word+=block[i*9+4:i*9+6]+block[i*9+6:i*9+8]
    return input2word


def BHive(password,input,showinput,trytime):
    global BHiveCount
    order=0 
    if trytime==0:
        order=order+1
    elif trytime>5:
        # print("trytime {}/{} {}".format(order,num_file,input))
        # print("trytime {}/{} {}".format(order,num_file,showinput))
        # print("trytime > 5")
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
        return BHive(password,input,showinput,trytime+1)

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

def calculateAccuracy(accurateCycles,predictionCycles,rank):
    # print(" rank{}-tsj".format(rank))
    if int(accurateCycles) == -1 or float(predictionCycles) == -1 or int(accurateCycles) == 0:
        # print(" rank{}-0".format(rank))
        return 0
    else:
        # print(" rank{}-tsj2".format(rank))
        # print("{} {}".format(accurateCycles,predictionCycles))
        gap=abs(BHiveCount*float(predictionCycles)-int(accurateCycles))
        # print(" rank{}-{}".format(rank,int(gap)/int(accurateCycles)))
        return int(gap)/int(accurateCycles) # accuracy variable is error

def paralleReadProcess(rank,password, startFileLine,endFileLine,unique_revBiblock_Queue,frequencyRevBiBlock_Queue,OSACAmaxCyclesRevBiBlock_Queue,OSACACPCyclesRevBiBlock_Queue,BhiveCyclesRevBiBlock_Queue,accuracyMax_Queue,accuracyCP_Queue):
    print("MPI Process Start {:2d} {}~{}".format(rank,startFileLine,endFileLine))
    fread=open(filename, 'r')
    unique_revBiblock=set()
    frequencyRevBiBlock = defaultdict(int)
    OSACAmaxCyclesRevBiBlock = defaultdict(int)
    OSACACPCyclesRevBiBlock = defaultdict(int)
    BhiveCyclesRevBiBlock = defaultdict(int)
    accuracyMax = defaultdict(float)
    accuracyCP = defaultdict(float)
    for line in tqdm(fread.readlines()[startFileLine:endFileLine],total=endFileLine-startFileLine,desc=str("{:2d}".format(rank))):
    # for line in fread:
        # print("rank{}".format(rank))
        block=re.search('^(.*),',line).group(1)
        num=re.search(',(.*)$',line).group(1)
        unique_revBiblock.add(block)
        frequencyRevBiBlock[block] += int(num)
        # print("     rank{}:block{}".format(rank,block))
        BhiveCyclesRevBiBlock[block] = BHive(password,BHiveInput(block),BHiveInputDel0x(block),0)
        # print("         rank{}:block{}______{}".format(rank,block,BhiveCyclesRevBiBlock[block]))
        OSACAInput=saveOSACAInput2File(capstoneList(capstoneInput(block)),rank)
        OSACAmaxCyclesRevBiBlock[block] = OSACA(OSACAInput,"max")
        OSACACPCyclesRevBiBlock[block] = OSACA(OSACAInput,"CP")
        # print("             rank{}:block{}______{}".format(rank,block,OSACAmaxCyclesRevBiBlock[block]))
        accuracyMax[block]= calculateAccuracy(BhiveCyclesRevBiBlock[block],OSACAmaxCyclesRevBiBlock[block],rank)
        accuracyCP[block]= calculateAccuracy(BhiveCyclesRevBiBlock[block],OSACACPCyclesRevBiBlock[block],rank)
        # print("0rank{}".format(rank))
    fread.close() 
    # print("1rank{}".format(rank))
    unique_revBiblock_Queue.put(unique_revBiblock)
    frequencyRevBiBlock_Queue.put(frequencyRevBiBlock)
    # print("2rank{}".format(rank))
    OSACAmaxCyclesRevBiBlock_Queue.put(OSACAmaxCyclesRevBiBlock)
    OSACACPCyclesRevBiBlock_Queue.put(OSACACPCyclesRevBiBlock)
    BhiveCyclesRevBiBlock_Queue.put(BhiveCyclesRevBiBlock)
    # print("3rank{}".format(rank))
    accuracyMax_Queue.put(accuracyMax)
    accuracyCP_Queue.put(accuracyCP)
    print("MPI Process end {:2d} {}~{}".format(rank,startFileLine,endFileLine))

def readPartFile(password, unique_revBiblock,frequencyRevBiBlock,OSACAmaxCyclesRevBiBlock,OSACACPCyclesRevBiBlock,BhiveCyclesRevBiBlock,accuracyMax,accuracyCP):
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
    global num_file,ProcessNum
    fread=open(filename, 'r')
    num_file = sum([1 for i in open(filename, "r")])
    fread.close() 
    unique_revBiblock_Queue =Queue()
    frequencyRevBiBlock_Queue = Queue()
    OSACAmaxCyclesRevBiBlock_Queue=Queue()
    OSACACPCyclesRevBiBlock_Queue=Queue()
    BhiveCyclesRevBiBlock_Queue=Queue()
    accuracyMax_Queue=Queue()
    accuracyCP_Queue=Queue()


    for i in range(ProcessNum):
        startFileLine=int(i*num_file/ProcessNum)
        endFileLine=int((i+1)*num_file/ProcessNum)
        p = Process(target=paralleReadProcess, args=(i,password, startFileLine,endFileLine,unique_revBiblock_Queue,frequencyRevBiBlock_Queue,OSACAmaxCyclesRevBiBlock_Queue,OSACACPCyclesRevBiBlock_Queue,BhiveCyclesRevBiBlock_Queue,accuracyMax_Queue,accuracyCP_Queue))
        p.start()

    while unique_revBiblock_Queue.qsize()<ProcessNum:
        print("QueueNum : {}".format(unique_revBiblock_Queue.qsize()))
        sys.stdout.flush()
        time.sleep(5)
    # for i in tqdm(range(ProcessNum)):
    for i in range(ProcessNum):
        print("MPISum rank : {}, blockNum : {},leftQueueNum : {}".format(i,len(unique_revBiblock),unique_revBiblock_Queue.qsize()))
        unique_revBiblock=unique_revBiblock.union(unique_revBiblock_Queue.get())
        frequencyRevBiBlock.update(frequencyRevBiBlock_Queue.get())
        OSACAmaxCyclesRevBiBlock.update(OSACAmaxCyclesRevBiBlock_Queue.get())
        OSACACPCyclesRevBiBlock.update(OSACACPCyclesRevBiBlock_Queue.get())
        BhiveCyclesRevBiBlock.update(BhiveCyclesRevBiBlock_Queue.get())
        accuracyMax.update(accuracyMax_Queue.get())
        accuracyCP.update(accuracyCP_Queue.get())
    return unique_revBiblock
    # print(unique_revBiblock)
    # print(frequencyRevBiBlock)
    # print(accuracyMax)
    # print(len(unique_revBiblock))
    # print(len(frequencyRevBiBlock))
    


def saveAllResult(taskfilenameprefix,unique_revBiblock,frequencyRevBiBlock,OSACAmaxCyclesRevBiBlock,OSACACPCyclesRevBiBlock,BhiveCyclesRevBiBlock,accuracyMax,accuracyCP):
    writeFilename="{}_count{}.OSACAVSBHive".format(taskfilenameprefix,BHiveCount)
    wrongResultFilename="{}_count{}.OSACAVSBHive_wrongResult".format(taskfilenameprefix,BHiveCount)
    fwriteblockfreq = open(writeFilename, "w")
    wrongResultFile = open(wrongResultFilename, "w")
    validNum=0
    unvalidNum=0
    totalaccuracyMax=0.0
    totalaccuracyCP=0.0
    lineNum=0
    for tmp_block_binary_reverse in unique_revBiblock:
        lineNum+=1
        if accuracyMax[tmp_block_binary_reverse] != 0 and accuracyCP[tmp_block_binary_reverse] != 0:
            validNum+=frequencyRevBiBlock[tmp_block_binary_reverse]
            totalaccuracyMax+=frequencyRevBiBlock[tmp_block_binary_reverse]*accuracyMax[tmp_block_binary_reverse]
            totalaccuracyCP+=frequencyRevBiBlock[tmp_block_binary_reverse]*accuracyCP[tmp_block_binary_reverse]
            fwriteblockfreq.writelines("{:5d} ".format(lineNum)+tmp_block_binary_reverse+','+str(frequencyRevBiBlock[tmp_block_binary_reverse])+',max '+ \
                str(OSACAmaxCyclesRevBiBlock[tmp_block_binary_reverse])+' _CP '+
                str(OSACACPCyclesRevBiBlock[tmp_block_binary_reverse])+' _Bh '+
                str(BhiveCyclesRevBiBlock[tmp_block_binary_reverse])+' _ '+
                str(accuracyMax[tmp_block_binary_reverse])+' _ '+
                str(accuracyCP[tmp_block_binary_reverse])+"\n")
        else:
            unvalidNum+=1
            fwriteblockfreq.writelines("{:5d} ".format(lineNum)+tmp_block_binary_reverse+','+str(frequencyRevBiBlock[tmp_block_binary_reverse])+',max '+ \
                str(OSACAmaxCyclesRevBiBlock[tmp_block_binary_reverse])+' _CP '+
                str(OSACACPCyclesRevBiBlock[tmp_block_binary_reverse])+' _Bh '+
                str(BhiveCyclesRevBiBlock[tmp_block_binary_reverse])+' _ '+
                str(accuracyMax[tmp_block_binary_reverse])+' _ '+
                str(accuracyCP[tmp_block_binary_reverse])+" wrong\n")
            wrongResultFile.writelines("{:5d} ".format(lineNum)+tmp_block_binary_reverse+','+str(frequencyRevBiBlock[tmp_block_binary_reverse])+',max '+ \
                str(OSACAmaxCyclesRevBiBlock[tmp_block_binary_reverse])+' _CP '+
                str(OSACACPCyclesRevBiBlock[tmp_block_binary_reverse])+' _Bh '+
                str(BhiveCyclesRevBiBlock[tmp_block_binary_reverse])+' _ '+
                str(accuracyMax[tmp_block_binary_reverse])+' _ '+
                str(accuracyCP[tmp_block_binary_reverse])+" wrong\n")
    fwriteblockfreq.writelines("validTotalNum & unvalidBlockNum :"+str(validNum)+" "+str(unvalidNum)+"\n")
    fwriteblockfreq.writelines("avg accuracyMax is "+str(totalaccuracyMax/validNum)+"\n")
    fwriteblockfreq.writelines("avg accuracyCP is "+str(totalaccuracyCP/validNum)+"\n")
    print("avg Max error rate is "+str(totalaccuracyMax/validNum)+"\n") 
    print("avg CP error rate is "+str(totalaccuracyCP/validNum)+"\n") 
    fwriteblockfreq.close()
    wrongResultFile.close()

if __name__ == "__main__":
    global filename
    print("请输入sudo密码")
    password=input("password:")
    taskfilenameprefix="/home/shaojiemike/blockFrequency/tensorflow_41Gdir_00all_skip_2"
    # taskfilenameprefix="/home/shaojiemike/blockFrequency/tensorflow_13G_part_skip_2"
    # taskfilenameprefix="/home/shaojiemike/blockFrequency/tensorflow_test_100"
    taskfilenamesubfix="log"
    filename="{}.{}".format(taskfilenameprefix,taskfilenamesubfix)
    unique_revBiblock=set()
    frequencyRevBiBlock = defaultdict(int)
    # OSACAmaxCyclesRevBiBlock = defaultdict(int)
    OSACAmaxCyclesRevBiBlock = defaultdict(int)
    OSACACPCyclesRevBiBlock = defaultdict(int)
    BhiveCyclesRevBiBlock = defaultdict(int)
    accuracyMax = defaultdict(float)
    accuracyCP = defaultdict(float)
    unique_revBiblock=readPartFile(password, unique_revBiblock,frequencyRevBiBlock,OSACAmaxCyclesRevBiBlock,OSACACPCyclesRevBiBlock,BhiveCyclesRevBiBlock,accuracyMax,accuracyCP)
    print("blockSize {} {}".format(len(unique_revBiblock),len(frequencyRevBiBlock)))
    saveAllResult(taskfilenameprefix,unique_revBiblock,frequencyRevBiBlock,OSACAmaxCyclesRevBiBlock,OSACACPCyclesRevBiBlock,BhiveCyclesRevBiBlock,accuracyMax,accuracyCP)
