

def BHiveInputDelimiter(block):
    Delimiter="x"
    input2word=""
    for i in range(int((len(block)+1)/9)):
        input2word+=Delimiter+block[i*9:i*9+2]+Delimiter+block[i*9+2:i*9+4]
        input2word+=Delimiter+block[i*9+4:i*9+6]+Delimiter+block[i*9+6:i*9+8]
    return input2word

# > ~/test/bhive-re/bhive-reg/bhive x2bx7ex41xfd 500

# [CHILD] Test block and tail copied.
# [CHILD] Aux. page mapped at 0x700000000000.
# [PARENT] Child stack at 0xffffc9c0bc70 saved.
# Signo: 19
# Addr: 0x3ee0033eef4
# Event num: 283

block_binary="217c001b e09f40b9"

print(BHiveInputDelimiter(block_binary))