# Bhive VS llvm-mca (vs OSACA) on ARMv7
Reimplementation of the BHive profiler on ARMv7 kunpeng processor. The original can be found here: https://github.com/ithemal/bhive.

## 安装
### 安装Bhive
位于 `./bhive-reg`下，`make`产生`bhive`可执行文件
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
#cmake  -DCMAKE_BUILD_TYPE=Debug ../llvm -v

make llvm-mca -j VERBOSE=1
```
### python库
```
pip install -r requirements.txt
```

## 运行
### 运行前必须修改的选项
执行文件等信息在`./src/config.py`下

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

restructure my **shit** code