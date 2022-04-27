from openpyxl import Workbook
from openpyxl.chart import BarChart, PieChart, LineChart, Reference
from OSACA import capstoneInput
from llvm_mca import capstone
import global_variable as glv

def add2Excel(wb,name,isFirstSheet,dataDict):
    #unique_revBiblock,frequencyRevBiBlock,OSACAmaxCyclesRevBiBlock,OSACACPCyclesRevBiBlock,OSACALCDCyclesRevBiBlock,BhiveCyclesRevBiBlock,accuracyMax,accuracyCP,llvmmcaCyclesRevBiBlock,accuracyLLVM):
    # if isFirstSheet==1:
        # ws = wb.active # 找当前Sheet
        # ws.title = name
    wb.create_sheet(name)
    ws = wb[name]
    ws.append(["num","block_binary" , "ARM64_assembly_code", "block_frequency", "LLVM-MCA_result", "BHive", "accuracyLLVM", "accuracyLLVM * block_frequency" ]) # 添加行
    ws.column_dimensions['B'].width = 62 # 修改列宽
    ws.column_dimensions['H'].width = 30 # 修改列宽
    for i in ['C','D','E','F','G','I','J','K']:
        ws.column_dimensions[i].width = 15 # 修改列宽
    validNum=0
    unvalidNum=0
    totalAccuracyLLVM=0.0
    # totalaccuracyMax=0.0
    # totalaccuracyCP=0.0
    totalOSACAavg=0.0
    lineNum=0
    for key, value in dataDict.dataDict.items():
        globals()[key]=value 

    for tmp_block_binary_reverse in unique_revBiblock:
        if BhiveCyclesRevBiBlock[tmp_block_binary_reverse]==0:
            continue
        lineNum+=1
        tmpARMassembly=capstone(capstoneInput(tmp_block_binary_reverse))
        if accuracyLLVM[tmp_block_binary_reverse] != 0:
            validNum+=frequencyRevBiBlock[tmp_block_binary_reverse]
            # totalAccuracyLLVM+=frequencyRevBiBlock[tmp_block_binary_reverse]*accuracyLLVM[tmp_block_binary_reverse]
            totalAccuracyLLVM+=accuracyLLVM_MuliplyFrequency[tmp_block_binary_reverse]
            # totalaccuracyMax+=frequencyRevBiBlock[tmp_block_binary_reverse]*accuracyMax[tmp_block_binary_reverse]
            # totalaccuracyCP+=frequencyRevBiBlock[tmp_block_binary_reverse]*accuracyCP[tmp_block_binary_reverse]

            # count=frequencyRevBiBlock[tmp_block_binary_reverse]
            # OSACAMax=OSACAmaxCyclesRevBiBlock[tmp_block_binary_reverse]
            # OSACACP=OSACACPCyclesRevBiBlock[tmp_block_binary_reverse]
            # realBHive=float(BhiveCyclesRevBiBlock[tmp_block_binary_reverse])
            # tmp=(OSACAMax+OSACACP)/2 * BHiveCount - realBHive
            # totalOSACAavg+=abs(tmp)/realBHive * count

            ws.append(["{:5d} ".format(lineNum), 
                tmp_block_binary_reverse,
                tmpARMassembly,
                frequencyRevBiBlock[tmp_block_binary_reverse],
                # OSACAmaxCyclesRevBiBlock[tmp_block_binary_reverse],
                # OSACACPCyclesRevBiBlock[tmp_block_binary_reverse],
                # OSACALCDCyclesRevBiBlock[tmp_block_binary_reverse],
                llvmmcaCyclesRevBiBlock[tmp_block_binary_reverse],
                BhiveCyclesRevBiBlock[tmp_block_binary_reverse],
                accuracyLLVM[tmp_block_binary_reverse],
                accuracyLLVM_MuliplyFrequency[tmp_block_binary_reverse]]
                # accuracyMax[tmp_block_binary_reverse],
                # accuracyCP[tmp_block_binary_reverse]]
                )

        else:
            unvalidNum+=1
            ws.append(["{:5d} ".format(lineNum), 
                tmp_block_binary_reverse,
                tmpARMassembly,
                frequencyRevBiBlock[tmp_block_binary_reverse],
                # OSACAmaxCyclesRevBiBlock[tmp_block_binary_reverse],
                # OSACACPCyclesRevBiBlock[tmp_block_binary_reverse],
                # OSACALCDCyclesRevBiBlock[tmp_block_binary_reverse],
                llvmmcaCyclesRevBiBlock[tmp_block_binary_reverse],
                BhiveCyclesRevBiBlock[tmp_block_binary_reverse],
                accuracyLLVM[tmp_block_binary_reverse],
                accuracyLLVM_MuliplyFrequency[tmp_block_binary_reverse],
                # accuracyMax[tmp_block_binary_reverse],
                # accuracyCP[tmp_block_binary_reverse]]
                "ops!"])
    if validNum==0:
        llvmerror=0
    else:
        llvmerror=totalAccuracyLLVM/validNum
    # osacaerror=totalOSACAavg/validNum
    osacaerror = 0
    return [llvmerror,osacaerror]

def excelGraphInit():
    wb = Workbook()
    ws = wb.active # 找当前Sheet
    ws.title = 'Graph'
    ws = wb["Graph"]
    ws.column_dimensions['A'].width = 15 # 修改列宽
    ws.column_dimensions['B'].width = 15 # 修改列宽
    ws.column_dimensions['C'].width = 15 # 修改列宽
    ws.append(["applications","LLVM-MCA_error","OSACA_error"])
    return wb

def excelGraphAdd(wb,taskName,llvmerror,osacaerror):
    ws = wb["Graph"]
    ws.append([taskName,llvmerror,osacaerror])

def excelGraphBuild(wb):
    # 一个图两个轴
    ws = wb["Graph"]
    ct_bar = BarChart()
    taskNum=len(glv._get("taskList"))
    ws['D1'] = '误差比值'
    for i in range(2, taskNum+2):
        if ws[f'B{i}'].value==0:
            ws[f'D{i}']=0
        else:
            ws[f'D{i}'] = ws[f'C{i}'].value / ws[f'B{i}'].value
    d_ref = Reference(ws, min_col=2, min_row=1, max_row=taskNum+1, max_col=3)
    ct_bar.add_data(d_ref, titles_from_data=True)
    series = Reference(ws, min_col=1, min_row=2, max_row=taskNum+1)
    ct_bar.set_categories(series)
    ct_bar.x_axis.title = '应用'
    ct_bar.y_axis.title = '误差'
    ct_bar.y_axis.majorGridlines = None
    ct_bar.title = '各应用静态分析误差对比表'
    ct_line = LineChart()
    d_ref = Reference(ws, min_col=4, min_row=1, max_row=taskNum+1)
    ct_line.add_data(d_ref, titles_from_data=True)
    ct_line.y_axis.axId = 200 # 不为空即可
    ct_line.y_axis.title = '误差比值'
    # 让线条和第一图的最大值相交
    ct_line.y_axis.crosses = 'max'
    ct_bar += ct_line # 只支持+=赋值，不能直接+
    ws.add_chart(ct_bar, 'A10')
    wb.save(glv._get("excelOutPath"))
