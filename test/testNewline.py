
from tsjPython.tsjCommonFunc import *
from multiprocessing import Process, Pipe
import curses
ProcessNum=10
barTotalNum=dict()
barStartTime=dict()
barBeforeTime=dict()
barName=set()
stdscr = curses.initscr()

def is_positive(value):
    value = int(value)
    if value <= 0:
         raise TypeError("%s is an invalid positive int value" % value)
    return True

def time2String(timeNum):
    if timeNum < 3600:
        minutes=timeNum//60
        secends=timeNum%60
        return "{:0>2d}:{:0>2d}".format(minutes,secends)
    else:
        hour=timeNum//3600
        minutes=(timeNum-hour*3600)//60
        secends=timeNum%60
        return "{:0>2d}:{:0>2d}:{:0>2d}".format(hour,minutes,secends)

def barString(name,current=0,total=-1):
    global barBeforeTime,barName,barStartTime,barTotalNum
    retSting=""
    if name not in barName:
        if is_positive(total):
            barName.add(name)
            barBeforeTime[name]=time.time()
            barStartTime[name]=time.time()
            barTotalNum[name]=total
        return "bar is ready……"
    elif is_positive(current):
        if barTotalNum[name]<current:
            current=barTotalNum[name]
        total=barTotalNum[name]
        lastTime=int(time.time()-barBeforeTime[name])
        pastTime=int(time.time()-barStartTime[name])
        restTime=int(pastTime/current*(total-current))
        barBeforeTime[name]=time.time()
        retSting+="[{}:{:3d}%] > |".format(format(name," <10"),int(100*current/total))  #█
        space='█'
        spaceNum=int(format(100*current/total,'0>2.0f'))
        leftNum=100-spaceNum
        retSting=retSting.ljust(spaceNum+len(retSting),space)
        retSting=retSting.ljust(leftNum+len(retSting),' ')
        retSting+="| {} [{}<{}, {} s/it]".format(str(current)+"/"+str(total),time2String(pastTime),time2String(restTime),time2String(lastTime))
        return retSting

def display_info(str, x, y, colorpair=2):
    '''''使用指定的colorpair显示文字'''  
    global stdscr
    stdscr.addstr(y, x,str, curses.color_pair(colorpair))
    stdscr.refresh()

def set_win():
    '''''控制台设置'''
    global stdscr
    #使用颜色首先需要调用这个方法
    curses.start_color()
    #文字和背景色设置，设置了两个color pair，分别为1和2
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    #关闭屏幕回显
    # curses.noecho()
    #输入时不需要回车确认
    # curses.cbreak()
    #设置nodelay，使得控制台可以以非阻塞的方式接受控制台输入，超时1秒
    # stdscr.nodelay(1)

def unset_win():
    '''控制台重置'''
    global stdstr
    #恢复控制台默认设置（若不恢复，会导致即使程序结束退出了，控制台仍然是没有回显的）
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    #结束窗口
    curses.endwin()

def sonProcess(ProcessID,sendPipe):
    total=ProcessID*10+10
    # sendCurrent=total
    # sendPipe.send(sendCurrent)
    for i in range(total):
        sleepRandom(0.5)
        sendPipe.send(i+1)
    sendPipe.close()

def multBar(Msg,ProcessNum,total,sendPipe,receivePipe):
    processBeginTime=time.time()
    print("{} : start Process at: {}".format(Msg,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    # set total num
    for ProcessID in range(ProcessNum):     
        display_info(barString(ProcessID,0,total[ProcessID]),0,ProcessID+1,1)

    #close parent sendPipe
    for ProcessID , sendID in sendPipe.items():
        sendID.close()

    remainReceive=1
    whileTimes=0
    while remainReceive:
        whileTimes+=1
        display_info("check time: "+str(whileTimes),0,0,2)
        remainReceive=0
        deleteReceivePipeID=[]
        for ProcessID , receiveID in receivePipe.items():
            msg=receiveID.recv()
            display_info(barString(ProcessID,msg),0,ProcessID+1,1)
            if(msg>=barTotalNum[ProcessID]):
                deleteReceivePipeID.append(ProcessID)
            remainReceive=1
        for ProcessID in deleteReceivePipeID:
            del receivePipe[ProcessID]
    unset_win()
    print("{} : wait Process to finish: {}".format(Msg,time2String(int(time.time()-processBeginTime))))

if __name__ == "__main__":
    sendPipe=dict()
    receivePipe=dict()
    total=dict()
    set_win()
    unset_win()
    # curses.nonl()
    # curses.noraw()
    print("11223",end="\n\r")
    print("11223")
    print("11223\n",end="\n\r")
    password=input("password:")

    

    # multBar("task1",ProcessNum,total,sendPipe,receivePipe)
    
        