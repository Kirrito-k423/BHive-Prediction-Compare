# Bhive VS llvm-mca (vs OSACA) on ARMv7


[![OSCS Status](https://www.oscs1024.com/platform/badge/Kirrito-k423/BHive-Prediction-Compare.svg?size=small)](https://www.oscs1024.com/project/Kirrito-k423/BHive-Prediction-Compare?ref=badge_small)

Reimplementation of the BHive profiler on ARMv7 kunpeng processor. The original can be found here: https://github.com/ithemal/bhive.

## 仓库功能

![](https://shaojiemike.oss-cn-hangzhou.aliyuncs.com/img/20220712154020.png)

该仓库属于流程图的淡紫色模块的实现。
## 程序运行流程简述

1. 对于每个汇编的log文件(基本块二进制，以及次数)
2. readPartFile分别读取，并并行执行
	1. 每个子进程负责自己的部分，运行BHive和llvm-mca的值，并进行比较，计算偏差。
3. Reduce结果
4. 写入Excel文件。

## 安装
### 安装Bhive
位于 `./bhive-reg`下，`make`产生`bhive`可执行文件。

安装完，测试如下：
```
qcjiang@brainiac1:~/tests$ bhive \xc1\x02\x40\xb9\xe0\x03\x01\x2a\x00\x00\x18\xca\x00\xfc\x41\xd3\xd6\x12\x00\x91\xc1\x02\x40\xb9\xe0\x03\x01\x2a

[CHILD] Test block and tail copied.
[CHILD] Aux. page mapped at 0x700000000000.
[PARENT] Child stack at 0xfffff407ff90 saved.
Signo: 19
Addr: 0x3ed0011e114
Event num: 229
```
### 安装llvm-mca
代码在https://github.com/qcjiang/llvm-project，有个tsv110的branch，直接在github上fork这个仓库，之后有提交的话提pull request
```
mkdir build && cd build
cmake -DLLVM_TARGETS_TO_BUILD="AArch64" -DCMAKE_BUILD_TYPE=Debug ../llvm
make llvm-mca -j VERBOSE=1
```
### python库
```
pip install -r requirements.txt
```

## 运行
### 运行前必须修改的选项
执行文件等信息在`./src/config.py`下。(必须修改Bhive，llvm-mca可执行文件路径)

### 查看选项
```
> python3 ./src/main.py -h
You can change all parameters in config.py except enter some parameters

usage: main.py [-h] [-b BHIVECOUNT] [-p PROCESSNUM] [-t TIMEOUT] [-d {yes,no}]

please enter some parameters

optional arguments:
  -h, --help            show this help message and exit
  -b BHIVECOUNT, --BHiveCount BHIVECOUNT
                        BHive Count Num (maybe useless depends on bin/bhive use
  -p PROCESSNUM, --ProcessNum PROCESSNUM
                        multiple Process Numbers
  -t TIMEOUT, --timeout TIMEOUT
                        sub program interrupt time(eg. llvm-mca, bhive, OSACA. less time causes less useful output
  -d {yes,no}, --debug {yes,no}
                        is print debug informations
```
### 推荐运行
```
python3 ./src/main.py -b 500 -p 20 -d no
```
## features

1. base on armV7
2. compare OSACA, LLVM-mca, Bhive
3. multiProcess
4. result in excel file with graph
5. icecream for debug
	* 优雅打印对象：函数名，结构体
	* 打印行号和栈（没用输入时
	* 允许嵌套（会将输入传递到输出
	* 允许带颜色`ic.format(*args)`获得ic打印的文本
	* debug `ic.disable()`and `ic.enable()`
	* 允许统一前缀 `ic.configureOutput(prefix='Debug | ')`
	* 不用每个文件import
	```
	from icecream import install
	install()

	ic.configureOutput(prefix='Debug -> ', outputFunction=yellowPrint)
	```
## To do
### bugs（已经修复）

<details>

<summary>python的子程序实现有问题，运行中，会有bhive-reg遗留下来（多达20个，需要按照下面手动kill，这也是核数建议为总核数的1/3的原因</summary>

### check process create time
```
ps -eo pid,lstart,cmd |grep bhive
date
```
### kill all process by name
```
 sudo ps -ef | grep 'bhive-re' | grep -v grep | awk '{print $2}' | sudo xargs -r kill -9
```

### 以为的原因

subProcess.pool 返回程序状态的时候，除了运行和结束状态，还有休眠等其他状态。也就是程序在发射之后并不是直接进入运行状态的。判断程序是否超时不能通过判断是否运行，因为一开始while循环进不去
```
while process.poll() is None:
```
而应该是判断是否正常结束(208是BHive结束返回值，不同程序不同)
```
while process.poll() != 208:
```
### 继续分析
实际debug还是有
![](https://shaojiemike.oss-cn-hangzhou.aliyuncs.com/img/20220625173740.png)

在debug输出里没有这些pid

check了，输出的个数是符合的。

不懂了，我都没调用，这僵尸进程哪里来的？除非是BHive产生的。

### 实际原因
调用的Bhive会产生子进程，原本的python实现不能杀死子进程的子进程。需要改用杀死进程组的实现

### 杀死进程组

![](https://shaojiemike.oss-cn-hangzhou.aliyuncs.com/img/20220625185611.png)

可能设定是timeout是20秒，但是htop程序运行了2分钟也没有kill。这是正常的，因为主程序挤占资源导致挂起了，导致无法及时判断和kill
</details>
