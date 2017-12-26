import base64, re, binascii

# still need to make it work with inputs where message/key are different
# all inputs are valid

# XOR function
def xor_two_str(a,b):
    return ''.join([hex(ord(a[i%len(a)]) ^ ord(b[i%(len(b))]))[2:] for i in range(max(len(a), len(b)))])

# M = message, K = key
message = raw_input("Input message (any length): ")
key = raw_input("Input key (8 bits or less): ") 

M = ''.join(format(ord(x), 'b').rjust(8, '0') for x in message)
K = ''.join(format(ord(x), 'b').rjust(8, '0') for x in key)

# padding if necessary
M = M.ljust(64, '0') #isn't necessary after I use indv_blocks 
K= K.ljust(64, '0')

# truncating key if input key was >8 bits
K = K[:64]

# splitting M into individual blocks of 64
indv_blocks = re.findall('.{1,64}', M)
for i in range(0, len(indv_blocks)):
    indv_blocks[i] = indv_blocks[i].ljust(64, '0')

output = ""
idx = [57,49,41,33,25,17,9,
    1,58,50,42,34,26,18,
    10,2,59,51,43,35,27,
    19,11,3,60,52,44,36,
    63,55,47,39,31,23,15,
    7,62,54,46,38,30,22,
    14,6,61,53,45,37,29,
    21,13,5,28,20,12,4]

cnt = 0
tmp = ""
for i in idx:
    tmp += K[i-1]
    cnt += 1
    if cnt == 7:
        output += tmp
        tmp = ""
        cnt = 0
        
c = output[:28]
d = output[28:]

keys = []

for i in range(1, 17):
    c = c[1:] + c[0]
    d = d[1:] + d[0]
    if 3 <= i <= 8 or 10 <= i <= 15:
        c = c[1:] + c[0]
        d = d[1:] + d[0]

    keys.append(c + d)

idx = [14,17,11,24,1,5,
        3,28,15,6,21,10,
        23,19,12,4,26,8,
        16,7,27,20,13,2,
        41,52,31,37,47,55,
        30,40,51,45,33,48,
        44,49,39,56,34,53,
        46,42,50,36,29,32]
        
subkeys = []

cnt = 0
output = ""
tmp = ""
for key in keys:
    for i in idx:
        tmp += key[i-1]
        cnt += 1
        if cnt == 6:
            output += tmp
            tmp = ""
            cnt = 0
    subkeys.append(output)
    output = ""


#################### Replace M with indv_blocks
#################### Oh god this is gonna be disgusting

for blocks in indv_blocks:
    idx=[58,50,42,34,26,18,10,2,
        60,52,44,36,28,20,12,4,
        62,54,46,38,30,22,14,6,
        64,56,48,40,32,24,16,8,
        57,49,41,33,25,17, 9,1,
        59,51,43,35,27,19,11,3,
        61,53,45,37,29,21,13,5,
        63,55,47,39,31,23,15,7]
        
    cnt = 0
    ip = ""
    tmp = ""
    for i in idx:
        tmp += blocks[i-1]
        cnt += 1
        if cnt == 8:
            ip += tmp
            tmp = ""
            cnt = 0
    
    sboxes = [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7], [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8], 
    [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0], [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]], 
    [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10], [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5], 
    [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15], [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]], 
    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8], [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1], 
    [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7], [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]], 
    [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15], [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9], 
    [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4], [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]], 
    [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9], [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6], 
    [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14], [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]], 
    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11], [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8], 
    [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6], [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]], 
    [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1], [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6], 
    [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2], [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]], 
    [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7], [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2], 
    [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8], [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]
    
    pbox=[16,7,20,21,
        29,12,28,17,
        1,15,23,26,
        5,18,31,10,
        2,8,24,14,
        32,27,3,9,
        19,13,30,6,
        22,11,4,25]
            
    ebit=[32,1,2,3,4,5,
        4,5,6,7,8,9,
        8,9,10,11,12,13,
        12,13,14,15,16,17,
        16,17,18,19,20,21,
        20,21,22,23,24,25,
        24,25,26,27,28,29,
        28,29,30,31,32,1]
        
    ipRev=[40,8,48,16,56,24,64,32,
        39,7,47,15,55,23,63,31,
        38,6,46,14,54,22,62,30,
        37,5,45,13,53,21,61,29,
        36,4,44,12,52,20,60,28,
        35,3,43,11,51,19,59,27,
        34,2,42,10,50,18,58,26,
        33,1,41,9,49,17,57,25]    
        
    l_vals = []
    r_vals = []
    
    l_vals.append(ip[:32])
    r_vals.append(ip[32:])
    
    for i in range(1, 17):
        l_vals.append(r_vals[i-1])
    
        currKey = subkeys[i-1]
    
        eR = ""
        for x in ebit:
            eR += r_vals[i-1][x-1]
            
        xord = xor_two_str(eR, currKey)
        xord = re.findall('......',xord)
        
        sout = ""
        for j in range(len(xord)):
            col = int(xord[j][0] + xord[j][5], 2)
            row = int(xord[j][1] + xord[j][2] + xord[j][3] + xord[j][4], 2)
            sout += '{0:04b}'.format(sboxes[j][col][row])
        
        f = ""
        for pidx in pbox:
            f += sout[pidx-1]
        r_vals.append(xor_two_str(l_vals[i-1], f))
    
    rl = r_vals[16] + l_vals[16]
    hexout = ""
    for irev in ipRev:
        hexout += rl[irev-1]
        
    print "ciphertext: " + str(hex(int(hexout, 2))[2:])

###### End Encoding