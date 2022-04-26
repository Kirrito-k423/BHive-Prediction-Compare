# bhive
Reimplementation of the BHive profiler on ARMv7 kunpeng processor. The original can be found here: https://github.com/ithemal/bhive.

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