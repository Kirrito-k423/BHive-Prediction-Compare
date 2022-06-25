import os
from icecream import ic
def TIMEOUT_COMMAND(command, timeout=10):
    """call shell-command and either return its output or kill it
    if it doesn't normally exit within timeout seconds and return None"""
    import subprocess, datetime, os, time, signal
    cmd = command.split(" ")
    start = datetime.datetime.now()
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,encoding="utf-8")
    ic(process.pid)
    ic(process.poll())
    while process.poll() != 0: # poll()返回0 正常结束， 1 sleep， 2 子进程不存在，-15 kill，None 在运行
        ic(process.poll())
        time.sleep(0.2)
        now = datetime.datetime.now()
        if (now - start).seconds> timeout:
            os.kill(process.pid, signal.SIGKILL)
            # https://blog.csdn.net/zhupenghui176/article/details/109097737
            # os.waitpid(-1, os.WNOHANG)
            (killPid,killSig) = os.waitpid(process.pid, 0)
            ic(killPid)
            ic(killSig)
            print("TIMEOUT_COMMAND kill failed! killPid %d process.pid %d killSig %d" % (killPid, process.pid, killSig) )
            # return 0
    ic(process.poll())
    returnVal = process.stdout.readlines()
    ic(process.pid)
    # (killPid,killSig) = os.waitpid(process.pid, 0)
    # ic(killPid)
    # ic(killSig)
    return returnVal
print(TIMEOUT_COMMAND('ping 127.0.0.1', 3))
