import global_variable as glv
import multiprocessing as mp
from data import queueDictInit
from multiprocessing import Pipe,Queue
from multiBar import *
from collections import defaultdict
from Bhive import *
from llvm_mca import *
from OSACA import *
from collections import defaultdict
from KendallIndex import calculateKendallIndex
from data import dataDictInit,readDictFromJson,saveDict2Json,dataDictClass


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
    fread=open(filename, 'r') 

    unique_revBiblock=set()
    frequencyRevBiBlock = defaultdict(int)
    llvmmcaCyclesRevBiBlock = defaultdict(int)
    BaselineCyclesRevBiBlock = defaultdict(int)

    OSACA_TPLCDmax_CyclesRevBiBlock = defaultdict(float)
    OSACA_TPLCDavg_CyclesRevBiBlock = defaultdict(float)
    OSACATPCyclesRevBiBlock = defaultdict(float)
    OSACALCDCyclesRevBiBlock =  defaultdict(float)

    BhiveCyclesRevBiBlock = defaultdict(int)
    accuracyLLVM = defaultdict(float)
    accuracyLLVM_MuliplyFrequency = defaultdict(float)
    accuracyBaseline = defaultdict(float)
    accuracyBaseline_MuliplyFrequency = defaultdict(float)

    accuracyMax = defaultdict(float)
    accuracyAvg = defaultdict(float)
    accuracyCP = defaultdict(float)

    i=1
    sendSkipNum=int((endFileLine-startFileLine)/100)+1
    try:
        for line in fread.readlines()[startFileLine:endFileLine]:
            if i%sendSkipNum==0:
                sendPipe.send(i)
            i+=1

            block=re.search('^(.*),',line).group(1)
            num=re.search(',(.*)$',line).group(1)

            unique_revBiblock.add(block)
            frequencyRevBiBlock[block] = int(num)
            BhiveCyclesRevBiBlock[block] = BHive(block,BHiveInputDelimiter(block))
            llvmmcaCyclesRevBiBlock[block] = LLVM_mca(block,capstone(capstoneInput(block)))
            BaselineCyclesRevBiBlock[block] = LLVM_mcaBaseline(block,capstone(capstoneInput(block)))

            OSACAInput=saveOSACAInput2File(capstoneList(capstoneInput(block)),rank)
            [OSACA_TPLCDmax_CyclesRevBiBlock[block], OSACA_TPLCDavg_CyclesRevBiBlock[block] ,\
             OSACATPCyclesRevBiBlock[block],         OSACALCDCyclesRevBiBlock[block]] = OSACA(block,OSACAInput)

            accuracyLLVM[block]= calculateAccuracyLLVM(BhiveCyclesRevBiBlock[block],llvmmcaCyclesRevBiBlock[block])
            accuracyLLVM_MuliplyFrequency[block]=accuracyLLVM[block]* frequencyRevBiBlock[block]
            accuracyBaseline[block]= calculateAccuracyLLVM(BhiveCyclesRevBiBlock[block],BaselineCyclesRevBiBlock[block])
            accuracyBaseline_MuliplyFrequency[block]=accuracyBaseline[block]* frequencyRevBiBlock[block]

            accuracyMax[block]= calculateAccuracyOSACA(BhiveCyclesRevBiBlock[block],OSACA_TPLCDmax_CyclesRevBiBlock[block],rank)
            accuracyAvg[block]= calculateAccuracyOSACA(BhiveCyclesRevBiBlock[block],OSACA_TPLCDavg_CyclesRevBiBlock[block],rank)
            accuracyCP[block]= calculateAccuracyOSACA(BhiveCyclesRevBiBlock[block],OSACATPCyclesRevBiBlock[block],rank)
    except Exception as e:
        sendPipe.send(e)
        errorPrint("error = {}".format(e))
        raise TypeError("paralleReadProcess = {}".format(e))
    fread.close() 
    queueDict.get("unique_revBiblock").put(unique_revBiblock)
    queueDict.get("frequencyRevBiBlock").put(frequencyRevBiBlock)
    queueDict.get("llvmmcaCyclesRevBiBlock").put(llvmmcaCyclesRevBiBlock)
    queueDict.get("BaselineCyclesRevBiBlock").put(BaselineCyclesRevBiBlock)

    queueDict.get("OSACA_TPLCDmax_CyclesRevBiBlock").put(OSACA_TPLCDmax_CyclesRevBiBlock)
    queueDict.get("OSACA_TPLCDavg_CyclesRevBiBlock").put(OSACA_TPLCDavg_CyclesRevBiBlock)
    queueDict.get("OSACATPCyclesRevBiBlock").put(OSACATPCyclesRevBiBlock)
    queueDict.get("OSACALCDCyclesRevBiBlock").put(OSACALCDCyclesRevBiBlock)
    
    queueDict.get("BhiveCyclesRevBiBlock").put(BhiveCyclesRevBiBlock)
    queueDict.get("accuracyLLVM").put(accuracyLLVM)
    queueDict.get("accuracyLLVM_MuliplyFrequency").put(accuracyLLVM_MuliplyFrequency)
    queueDict.get("accuracyBaseline").put(accuracyBaseline)
    queueDict.get("accuracyBaseline_MuliplyFrequency").put(accuracyBaseline_MuliplyFrequency)

    queueDict.get("accuracyMax").put(accuracyMax)
    queueDict.get("accuracyAvg").put(accuracyAvg)
    queueDict.get("accuracyCP").put(accuracyCP)

    sendPipe.send(i+sendSkipNum)
    sendPipe.close()

def fileLineNum(filename):
    fread=open(filename, 'r')
    num_file = sum([1 for i in open(filename, "r")])
    glv._set("num_file",num_file)
    fread.close() 
    return num_file

def mergeQueue2dataDict(queueDict,dataDict):
    for key, value in dataDict.dataDict.items():
        # ic(key,type(value))
        if isinstance(value,set):
            # ic("set")
            dataDict.dataDict[key]=dataDict.dataDict[key].union(queueDict.dataDict[key].get())
        elif isinstance(value,defaultdict):
            # ic("defaultdict(int)")
            ic(key)
            if key == "frequencyRevBiBlock":
                a=dataDict.dataDict[key]
                b=queueDict.dataDict[key].get()
                for key2 in b:
                    dataDict.dataDict[key][key2]=a[key2]+b[key2]
            else:
                dataDict.dataDict[key].update(queueDict.dataDict[key].get())
    return dataDict

def mergeHistory2dataDict(historyDict,dataDict):
    for key, value in dataDict.dataDict.items():
        # ic(key,type(value))
        if isinstance(value,set):
            # ic("set")
            dataDict.dataDict[key]=dataDict.dataDict[key].union(historyDict.dataDict[key])
        elif isinstance(value,defaultdict):
            # ic("defaultdict(int)")
            ic(key)
            if key == "frequencyRevBiBlock":
                a=dataDict.dataDict[key]
                b=historyDict.dataDict[key]
                for key2 in b:
                    dataDict.dataDict[key][key2]=a[key2]+b[key2]
            else:
                dataDict.dataDict[key].update(historyDict.dataDict[key])
    return dataDict

def parallelReadPartFile(taskName,filename, dataDict):
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
    if glv._get("debug")=='no':
        stdscr = curses.initscr()
        multBar(taskName,ProcessNum,total,sendPipe,receivePipe,pList,stdscr)
    
    while queueDict.get("unique_revBiblock").qsize()<ProcessNum:
        print("QueueNum : {}".format(queueDict.get("unique_revBiblock").qsize()))
        sys.stdout.flush()
        time.sleep(5)

    yellowPrint("Reducing parallel processes result...")
        
    for i in range(ProcessNum):
        dataDict=mergeQueue2dataDict(queueDict,dataDict)
    # 不需要merge，不然误差会降低一半
    # if glv._get("isPageExisted")=="yes":
    #     dataDict=mergeHistory2dataDict(glv._get("historyDict"),dataDict)
    return dataDict

def mergeKendallIndexQueueDict(queueDict,ProcessNum):
    concordantPairsNum=0
    disConcordantPairsNum=0
    concordantPairsNumOfBaseline=0
    disConcordantPairsNumOfBaseline=0


    for i in range(0,ProcessNum):
        concordantPairsNum+=queueDict.dataDict["concordantPairsNum"].get()
        disConcordantPairsNum+=queueDict.dataDict["disConcordantPairsNum"].get()
        concordantPairsNumOfBaseline+=queueDict.dataDict["concordantPairsNumOfBaseline"].get()
        disConcordantPairsNumOfBaseline+=queueDict.dataDict["disConcordantPairsNumOfBaseline"].get()
            
    return [concordantPairsNum,disConcordantPairsNum,concordantPairsNumOfBaseline,disConcordantPairsNumOfBaseline]

def parallelCalculateKendallIndex(taskName,dataDict):
    ProcessNum=glv._get("ProcessNum")

    # queueDictInit
    queueDict = dataDictClass()
    queueDict.set("concordantPairsNum",Queue())
    queueDict.set("disConcordantPairsNum",Queue())
    queueDict.set("concordantPairsNumOfBaseline",Queue())
    queueDict.set("disConcordantPairsNumOfBaseline",Queue())

    taskList=list(dataDict.get("unique_revBiblock"))
    task_num=len(taskList)

    sendPipe=dict()
    receivePipe=dict()
    total=dict()

    pList=[]
    for i in range(ProcessNum):
        startTaskNum=int(i*task_num/ProcessNum)
        endTaskNum=int((i+1)*task_num/ProcessNum)
        receivePipe[i], sendPipe[i] = Pipe(False)
        total[i]=endTaskNum-startTaskNum
        pList.append(Process(target=calculateKendallIndex, args=(taskList,dataDict,sendPipe[i],i,startTaskNum,endTaskNum,queueDict)))

    for p in pList:
        p.start()
    

    # https://stackoverflow.com/questions/19924104/python-multiprocessing-handling-child-errors-in-parent
    if glv._get("debug")=='no':
        stdscr = curses.initscr()
        multBar(taskName+"_KendallIndex",ProcessNum,total,sendPipe,receivePipe,pList,stdscr)
    
    while queueDict.get("disConcordantPairsNumOfBaseline").qsize()<ProcessNum:
        print("QueueNum : {}".format(queueDict.get("disConcordantPairsNumOfBaseline").qsize()))
        sys.stdout.flush()
        time.sleep(5)

    [concordantPairsNum,disConcordantPairsNum,concordantPairsNumOfBaseline,disConcordantPairsNumOfBaseline]\
            =mergeKendallIndexQueueDict(queueDict,ProcessNum)
    # 不需要merge，不然误差会降低一半
    # if glv._get("isPageExisted")=="yes":
    #     dataDict=mergeHistory2dataDict(glv._get("historyDict"),dataDict)
    KendallIndex = (concordantPairsNum - disConcordantPairsNum)*1.0/(concordantPairsNum + disConcordantPairsNum)
    baselineKendallIndex = (concordantPairsNumOfBaseline - disConcordantPairsNumOfBaseline)*1.0 /  (concordantPairsNumOfBaseline + disConcordantPairsNumOfBaseline)
    
    return [KendallIndex, baselineKendallIndex]