
def decode(ciphertext):
    # decode here
    length = len(ciphertext)
    # the output string
    b=""
    # use flag to decide whether this letter should be an indicator or not
    flag=0
    for i in range(length-1):
        if flag==1:
            flag=0
            continue
        if (ciphertext[i]=='V' or ciphertext[i]=='D' or ciphertext[i]=='F'):
            b=b+ciphertext[i+1]
            flag=1
    return b

if __name__ == '__main__':
    print decode(file('./vfd.txt').read())
