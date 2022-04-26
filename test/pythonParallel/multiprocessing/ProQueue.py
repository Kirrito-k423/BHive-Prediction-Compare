from multiprocessing import Process, Queue
import queue
from collections import defaultdict
import re
def f(startFileLine,endFileLine,unique_revBiblock_Queue,frequencyRevBiBlock_Queue):

    fread=open(filename, 'r')
    
    unique_revBiblock=set()
    frequencyRevBiBlock = defaultdict(int)

    for line in fread.readlines()[startFileLine:endFileLine]:
        block=re.search('^(.*),',line).group(1)
        num=re.search(',(.*)$',line).group(1)
        unique_revBiblock.add(block)
        frequencyRevBiBlock[block] += int(num)
    unique_revBiblock_Queue.put(unique_revBiblock)
    frequencyRevBiBlock_Queue.put(frequencyRevBiBlock)

if __name__ == '__main__':
    global filename
    taskfilenameprefix="/home/shaojiemike/blockFrequency/tensorflow_test_13"
    taskfilenamesubfix="log"
    filename="{}.{}".format(taskfilenameprefix,taskfilenamesubfix)

    num_file = sum([1 for i in open(filename, "r")])


    #rank = i
    #from i*num_file/ProcessNum

    unique_revBiblock=set()
    frequencyRevBiBlock = defaultdict(int)
    ProcessNum=3

    unique_revBiblock_Queue =Queue()
    frequencyRevBiBlock_Queue = Queue()


    for i in range(ProcessNum):
        startFileLine=int(i*num_file/ProcessNum)
        endFileLine=int((i+1)*num_file/ProcessNum)
        print(startFileLine,endFileLine)
        p = Process(target=f, args=(startFileLine,endFileLine,unique_revBiblock_Queue,frequencyRevBiBlock_Queue))
        p.start()

    # n=5
    # unique_revBiblock.add(-n)
    # frequencyRevBiBlock[-n]=n*n*n

    print(unique_revBiblock)
    print(frequencyRevBiBlock)
    # print(unique_revBiblock_Queue.get())
    # print(frequencyRevBiBlock_Queue.get())
    for i in range(ProcessNum):
        unique_revBiblock=unique_revBiblock.union(unique_revBiblock_Queue.get())
        frequencyRevBiBlock.update(frequencyRevBiBlock_Queue.get())
    print(unique_revBiblock)
    print(frequencyRevBiBlock)
    print(len(unique_revBiblock))
    print(len(frequencyRevBiBlock))