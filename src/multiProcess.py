import global_variable as glv
import multiprocessing as mp
from data import queueDictInit
from multiprocessing import Pipe
from multiBar import *
from collections import defaultdict
from Bhive import *
from llvm_mca import *
from OSACA import *

class Process(mp.Process):
    def __init__(self, *args, **kwargs):
        mp.Process.__init__(self, *args, **kwargs)
        self._pconn, self._cconn = mp.Pipe()
        self._exception = None

    def run(self):
        try:
            mp.Process.run(self)
            self._cconn.send(None)
        except Exception as e:
            tb = traceback.format_exc()
            self._cconn.send((e, tb))
            # raise e  # You can still rise this exception if you need to

    @property
    def exception(self):
        if self._pconn.poll():
            self._exception = self._pconn.recv()
        return self._exception

def paralleReadProcess(filename,sendPipe,rank, startFileLine,endFileLine, queueDict):
    # unique_revBiblock_Queue,frequencyRevBiBlock_Queue,OSACAmaxCyclesRevBiBlock_Queue,OSACACPCyclesRevBiBlock_Queue,OSACALCDCyclesRevBiBlock_Queue,BhiveCyclesRevBiBlock_Queue,accuracyMax_Queue,accuracyCP_Queue,llvmmcaCyclesRevBiBlock_Queue,accuracyLLVM_Queue):
    # print("MPI Process Start {:2d} {}~{}".format(rank,startFileLine,endFileLine))
    fread=open(filename, 'r')

    # subDataDict=dataDictInit()
    
    unique_revBiblock=set()
    frequencyRevBiBlock = defaultdict(int)
    llvmmcaCyclesRevBiBlock = defaultdict(int)
    # OSACAmaxCyclesRevBiBlock = defaultdict(int)
    # OSACACPCyclesRevBiBlock = defaultdict(int)
    # OSACALCDCyclesRevBiBlock =  defaultdict(int)
    BhiveCyclesRevBiBlock = defaultdict(int)
    accuracyLLVM = defaultdict(float)
    accuracyLLVM_MuliplyFrequency = defaultdict(float)
    # accuracyMax = defaultdict(float)
    # accuracyCP = defaultdict(float)
    # for line in tqdm(fread.readlines()[startFileLine:endFileLine],total=endFileLine-startFileLine,desc=str("{:2d}".format(rank))):
    i=1
    try:
        for line in fread.readlines()[startFileLine:endFileLine]:
            if i%5==0:
                sendPipe.send(i)
            i+=1
            # print("rank{}".format(rank))
            block=re.search('^(.*),',line).group(1)
            num=re.search(',(.*)$',line).group(1)
            unique_revBiblock.add(block)
            frequencyRevBiBlock[block] = int(num)
            # print("     rank{}:block{}".format(rank,block))
            BhiveCyclesRevBiBlock[block] = BHive(BHiveInputDel0xSpace(block),BHiveInputDel0xSpace(block),0)
            # print("         rank{}:block{}______{}".format(rank,block,BhiveCyclesRevBiBlock[block]))
            llvmmcaCyclesRevBiBlock[block] = LLVM_mca(capstone(capstoneInput(block)))
            # OSACAInput=saveOSACAInput2File(capstoneList(capstoneInput(block)),rank)
            # OSACAmaxCyclesRevBiBlock[block] = OSACA(password,OSACAInput,"max")
            # OSACACPCyclesRevBiBlock[block] = OSACA(password,OSACAInput,"CP")
            # OSACALCDCyclesRevBiBlock[block] = OSACA(password,OSACAInput,"LCD")
            # print("             rank{}:block{}______{}".format(rank,block,OSACAmaxCyclesRevBiBlock[block]))
            accuracyLLVM[block]= calculateAccuracyLLVM(BhiveCyclesRevBiBlock[block],llvmmcaCyclesRevBiBlock[block])
            accuracyLLVM_MuliplyFrequency[block]=accuracyLLVM[block]* frequencyRevBiBlock[block]
            # accuracyMax[block]= calculateAccuracyOSACA(BhiveCyclesRevBiBlock[block],OSACAmaxCyclesRevBiBlock[block],rank)
            # accuracyCP[block]= calculateAccuracyOSACA(BhiveCyclesRevBiBlock[block],OSACACPCyclesRevBiBlock[block],rank)
            # print("0rank{}".format(rank))
    except Exception as e:
        sendPipe.send(e)
        errorPrint("error = {}".format(e))
        raise TypeError("paralleReadProcess = {}".format(e))
    fread.close() 
    # print("1rank{}".format(rank))
    unique_revBiblock_Queue.put(unique_revBiblock)
    frequencyRevBiBlock_Queue.put(frequencyRevBiBlock)
    # print("2rank{}".format(rank))
    llvmmcaCyclesRevBiBlock_Queue.put(llvmmcaCyclesRevBiBlock)
    OSACAmaxCyclesRevBiBlock_Queue.put(OSACAmaxCyclesRevBiBlock)
    OSACACPCyclesRevBiBlock_Queue.put(OSACACPCyclesRevBiBlock)
    OSACALCDCyclesRevBiBlock_Queue.put(OSACALCDCyclesRevBiBlock)
    BhiveCyclesRevBiBlock_Queue.put(BhiveCyclesRevBiBlock)
    # print("3rank{}".format(rank))
    accuracyLLVM_Queue.put(accuracyLLVM)
    accuracyMax_Queue.put(accuracyMax)
    accuracyCP_Queue.put(accuracyCP)
    sendPipe.send(50000)
    sendPipe.close()
    # print("MPI Process end {:2d} {}~{}".format(rank,startFileLine,endFileLine))

def fileLineNum(filename):
    # filename=glv._get("filename")
    fread=open(filename, 'r')
    num_file = sum([1 for i in open(filename, "r")])
    glv._set("num_file",num_file)
    fread.close() 
    return num_file

def readPartFile(taskName,filename, dataDict):
    # unique_revBiblock,frequencyRevBiBlock,OSACAmaxCyclesRevBiBlock,OSACACPCyclesRevBiBlock,OSACALCDCyclesRevBiBlock,BhiveCyclesRevBiBlock,accuracyMax,accuracyCP,llvmmcaCyclesRevBiBlock,accuracyLLVM):
    num_file=fileLineNum(filename)
    ProcessNum=glv._get("ProcessNum")

    queueDict = queueDictInit(dataDict)

    sendPipe=dict()
    receivePipe=dict()
    total=dict()

    pList=[]
    for i in range(ProcessNum):
        startFileLine=int(i*num_file/ProcessNum)
        endFileLine=int((i+1)*num_file/ProcessNum)
        receivePipe[i], sendPipe[i] = Pipe(False)
        total[i]=endFileLine-startFileLine
        pList.append(Process(target=paralleReadProcess, args=(filename,sendPipe[i],i,startFileLine,endFileLine,queueDict)))

    for p in pList:
        p.start()
    
    # https://stackoverflow.com/questions/19924104/python-multiprocessing-handling-child-errors-in-parent
    multBar(taskName,ProcessNum,total,sendPipe,receivePipe,pList)
    
    while unique_revBiblock_Queue.qsize()<ProcessNum:
        print("QueueNum : {}".format(unique_revBiblock_Queue.qsize()))
        sys.stdout.flush()
        time.sleep(5)
    # for p in pList:
    #     p.join() # 避免僵尸进程
        
    # for i in tqdm(range(ProcessNum)):
    for i in range(ProcessNum):
        # print("MPISum rank : {}, blockNum : {},leftQueueNum : {}".format(i,len(unique_revBiblock),unique_revBiblock_Queue.qsize()))
        unique_revBiblock=unique_revBiblock.union(unique_revBiblock_Queue.get())
        frequencyRevBiBlock.update(frequencyRevBiBlock_Queue.get())
        llvmmcaCyclesRevBiBlock.update(llvmmcaCyclesRevBiBlock_Queue.get())
        OSACAmaxCyclesRevBiBlock.update(OSACAmaxCyclesRevBiBlock_Queue.get())
        OSACACPCyclesRevBiBlock.update(OSACACPCyclesRevBiBlock_Queue.get())
        OSACALCDCyclesRevBiBlock.update(OSACALCDCyclesRevBiBlock_Queue.get())
        BhiveCyclesRevBiBlock.update(BhiveCyclesRevBiBlock_Queue.get())
        accuracyLLVM.update(accuracyLLVM_Queue.get())
        accuracyMax.update(accuracyMax_Queue.get())
        accuracyCP.update(accuracyCP_Queue.get())
    return unique_revBiblock
    # print(unique_revBiblock)
    # print(frequencyRevBiBlock)
    # print(accuracyMax)
    # print(len(unique_revBiblock))
    # print(len(frequencyRevBiBlock))