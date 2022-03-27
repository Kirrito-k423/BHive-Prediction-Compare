import time
import subprocess
import pprint
from tsjPython.tsjCommonFunc import *

import subprocess, datetime, os, time, signal
timeout=10
# sencond
popenToleranceTime=10
def cmd2(command):
    global popenToleranceTime
    # subp = subprocess.Popen(command,close_fds=True,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding="utf-8")
    # subp.wait(2)
    start = datetime.datetime.now()
    process = subprocess.Popen(command,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,encoding="utf-8")
    while process.poll() is None:
        time.sleep(0.2)
        now = datetime.datetime.now()
        if (now - start).seconds> timeout:
            print("失败超时")
            os.kill(process.pid, signal.SIGKILL)
            os.waitpid(-1, os.WNOHANG)
            return None
    print("success")
    print(process.stdout.readlines())
    return process.stdout.readlines()

def cmd(command):
    global popenToleranceTime
    # subp = subprocess.Popen(command,close_fds=True,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding="utf-8")
    # subp.wait(2)
    start = datetime.datetime.now()
    cmd = command.split(" ")
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,encoding="utf-8")
    while process.poll() is None:
        time.sleep(0.2)
        now = datetime.datetime.now()
        if (now - start).seconds> timeout:
            print("失败超时")
            os.kill(process.pid, signal.SIGKILL)
            os.waitpid(-1, os.WNOHANG)
            return None
    print("success")
    print(process.stdout.readlines())
    return process.stdout.readlines()
    # trytime=popenToleranceTime*5
    # while not subp.poll() and trytime > 0:
    #     yellowPrint(trytime)
    #     trytime-=1
    #     time.sleep(0.2)
    # if subp.poll():
    #     print("success")
    #     print(subp.poll()) #poll(): 检查进程是否终止，如果终止返回 returncode，否则返回 None。
    #     print(subp.communicate())
    #     list = subp.communicate()[0].split("\n")
    #     print(list)
    # else:
    #     print("失败")
    #     subp.kill()
    #     print("超时")

    # trytime=popenToleranceTime*5
    # while not subp.poll() and trytime > 0:
    #     trytime-=1
    #     time.sleep(0.2)
    # list = []
    # if subp.poll():
    #     list = subp.communicate()[0].split("\n")
    # else:
    #     subp.kill()
    #     return -1    



# cmd("java -version")
cmd("ls")
# cmd("ls ddd")
# cmd("/home/shaojiemike/test/bhive-re/bhive/main 10000 0xaa 0x02 0x1f 0x12 0x60 0x76 0x4c 0x39 0x28 0x01 0x00 0xf0 0x00 0x19 0x47 0xb9 0x63 0xf6 0x42 0xb9 0x60 0x86 0x46 0xa9 0xbf 0xd7 0x00 0xb9 0x64 0x82 0x41 0xf9 0xbf 0x6f 0x00 0xf9 0x0d 0x04 0x40 0xf9 0x2e 0x04 0x40 0xf9 0x62 0xfa 0x42 0xb9 0x00 0x17 0x00 0x12 0xa5 0x63 0x40 0xf9 0x61 0xfe 0x42 0xb9 0x42 0x00 0x05 0x8a 0x01 0x27 0xc1 0x9a 0x21 0x14 0x00 0x12 0x82 0x78 0x62 0xf8 0x41 0x24 0xc1 0x9a 0x40 0x24 0xc0 0x9a 0x20 0x00 0x00 0x8a 0xe3 0x03 0x03 0x2a 0x61 0x86 0x41 0xf9 0x00 0x0b 0xc3 0x9a 0x00 0xe0 0x03 0x9b 0x37 0x78 0x60 0xb8 0x60 0x8a 0x41 0xf9 0x61 0xa2 0x0b 0x91 0xb6 0x53 0x07 0xa9 0xfc 0x03 0x0e 0xaa 0xbb 0x43 0x00 0xf9 0xfb 0x03 0x01 0xaa 0x17 0x48 0x37 0x8b 0x60 0xe2 0x0c 0x91 0xba 0x77 0x00 0xf9 0xf6 0x03 0x17 0xaa 0xaa 0x8b 0x00 0xb9 0xf7 0x03 0x0d 0xaa 0xfa 0x03 0x00 0xaa")
# cmd("/home/shaojiemike/github/qcjiang/OSACA/qcjiangOSACA/bin/osaca ")
# cmd("sleep 100")
cmd2("echo \"sub       sp, sp, #0x110\" | /home/qcjiang/codes/llvm-project/build/bin/llvm-mca -iterations=500")
cmd("python /home/qcjiang/softwares/anaconda3/bin/osaca --arch TSV110 /home/qcjiang/tests/bb_test/blockFrequency/tmpOSACAfiles/test_insns_test_5.0326newOSACAagain_OSACAInputTmpAsmBlockRank19")
# cmd("exit 1")
