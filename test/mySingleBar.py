import time
from tsjPython.tsjCommonFunc import *
barTotalNum=dict()
barStartTime=dict()
barBeforeTime=dict()
barName=set()

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
    elif is_positive(current) and barTotalNum[name]>= current:
        total=barTotalNum[name]
        lastTime=int(time.time()-barBeforeTime[name])
        pastTime=int(time.time()-barStartTime[name])
        restTime=int(pastTime/current*(total-current))
        barBeforeTime[name]=time.time()
        retSting+="[{}:{:2d}%] > |".format(format(name," <10"),int(100*current/total))  #█
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
    curses.noecho()
    #输入时不需要回车确认
    curses.cbreak()
    #设置nodelay，使得控制台可以以非阻塞的方式接受控制台输入，超时1秒
    stdscr.nodelay(1)

def unset_win():
    '''控制台重置'''
    global stdstr
    #恢复控制台默认设置（若不恢复，会导致即使程序结束退出了，控制台仍然是没有回显的）
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    #结束窗口
    curses.endwin()

import curses
# https://www.cnblogs.com/starof/p/4703820.html
stdscr = curses.initscr()
print(int(time.time()))
name="shijifan"
try:
    set_win()
    for i in range(100):
        sleepRandom(2)
        display_info(barString(name,i,100),0,0,1)
except Exception as e:
    raise e
finally:
    unset_win()

# current=23
# total=24
# pastTime=662
# lastTime=23
# retSting="[{}:{}%] > |".format(format(name," <10"),format(100*current/total,'.1f'))  #█
# space='█'
# spaceNum=int(format(100*current/total,'.0f'))
# leftNum=100-spaceNum
# retSting=retSting.ljust(spaceNum+len(retSting),space)
# retSting=retSting.ljust(leftNum+len(retSting),' ')
# hour=pastTime//3600
# minutes=(pastTime-hour*3600)//60
# secends=pastTime%60

# retSting+="| {} [{:0>2d}:{:0>2d}:{:0>2d}]".format(str(current)+"/"+str(total),hour,minutes,secends)
# hour=lastTime//3600
# minutes=(lastTime-hour*3600)//60
# secends=lastTime%60
# retSting+=" {:0>2d}:{:0>2d}:{:0>2d} lastItem".format(hour,minutes,secends)
# print(retSting)