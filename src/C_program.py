import os
import re
os.popen('ls -l')
# 输出：<open file 'ls -l', mode 'r' at 0x7f46af044930>
os.popen('ls -l').read() #返回字符串类型的结果
# 输出：'total 0\n-rw-rw-r-- 1 roaddb roaddb 0 Dec 11 10:09 a.txt\n-rw-rw-r-- 1 roaddb roaddb 0 Dec 11 10:09 b.txt\n'
os.popen('ls -l').readlines() #返回一个list类型的结果
# 输出：['total 0\n', '-rw-rw-r-- 1 roaddb roaddb 0 Dec 11 10:09 a.txt\n', '-rw-rw-r-- 1 roaddb roaddb 0 Dec 11 10:09 b.txt\n']

# val=os.popen('ls -al')
# for i in val.readlines():
#     print(i)  

val=os.popen('sudo /home/shaojiemike/test/bhive-re/bhive/main')
list = val.readlines()
print(list[-1])

resultCycle=re.search("core cyc: ([0-9]*)",list[-1]).group(1)
print(resultCycle)

