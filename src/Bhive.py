def checkBHiveResultStable(password,input,showinput,trytime):
    global BHiveCount
    order=0 
    if trytime==0:
        order=order+1
    elif trytime>5:
        return -1
    sys.stdout.flush()
    command=BHivePath+' '+input
    list=TIMEOUT_COMMAND(command)
    
    if list is None or len(list)==0:
        regexResult=None
    else:
        regexResult=re.search("Event num: ([0-9]*)",list[-1])
        # if not regexResult:
        #     regexResult=re.search("Event num: ([0-9]*)",list[-2])
    if regexResult:
        resultCycle=regexResult.group(1)
        return resultCycle
    else:
        return checkBHiveResultStable(password,input,showinput,trytime+1)
        
def BHive(password,input,showinput,trytime):
    global BHiveCount
    order=0 
    if trytime==0:
        order=order+1
    elif trytime>5:
        # print("trytime {}/{} {}".format(order,num_file,input))
        # print("trytime {}/{} {}".format(order,num_file,showinput))
        # print("trytime > 5")
        return -1
    # print("before main {}/{} {}".format(order,num_file,input))
    # print("before main {}/{} {}".format(order,num_file,showinput))
    sys.stdout.flush()
    # begin_time=time.time()
    command=BHivePath+' '+input
    list=TIMEOUT_COMMAND(command)

    if list is None or len(list)==0:
        regexResult=None
    else:
        regexResult=re.search("Event num: ([0-9]*)",list[-1])
        # if not regexResult:
        #     regexResult=re.search("Event num: ([0-9]*)",list[-2])
    if regexResult:
        resultCycle=regexResult.group(1)
        # print(resultCycle)
        return resultCycle
	#checkCycle=checkBHiveResultStable(password,input,showinput,0)
        #if arroundPercent(5,resultCycle,checkCycle):
        #    return resultCycle
        #else:
        #    return BHive(password,input,showinput,trytime+1)   
    else:
        # print("trytime: {} {}".format(trytime ,list[-1]))
        # print("else {}/{} {}".format(order,num_file,input))
        # print("else {}/{} {}".format(order,num_file,showinput))
        return BHive(password,input,showinput,trytime+1)

def BHiveInput(block):
    # print(block)
    # print((len(block)+1)/9)
    input2word=""
    for i in range(int((len(block)+1)/9)):
        # print(i)
        input2word+=" 0x"+block[i*9:i*9+2]+" 0x"+block[i*9+2:i*9+4]
        input2word+=" 0x"+block[i*9+4:i*9+6]+" 0x"+block[i*9+6:i*9+8]
    # print(input2word)
    return input2word

def BHiveInputDel0xSpace(block):
    # print(block)
    # print((len(block)+1)/9)
    input2word=""
    for i in range(int((len(block)+1)/9)):
        # print(i)
        input2word+=block[i*9:i*9+2]+block[i*9+2:i*9+4]
        input2word+=block[i*9+4:i*9+6]+block[i*9+6:i*9+8]
    # print(input2word)
    return input2word

def BHiveInputDel0x(block):
    # print(block)
    # print((len(block)+1)/9)
    input2word=""
    for i in range(int((len(block)+1)/9)):
        # print(i)
        input2word+=" "+block[i*9:i*9+2]+" "+block[i*9+2:i*9+4]
        input2word+=" "+block[i*9+4:i*9+6]+" "+block[i*9+6:i*9+8]
    # print(input2word)
    return input2word
