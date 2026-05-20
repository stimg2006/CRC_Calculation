# -*- coding: utf-8 -*-
"""
@author: FUJIIK
"""
print('Please input first value.')
val1_string = input()
print('Please input second value.')
val2_string = input()

List_val1 = list(val1_string)
List_val2 = list(val2_string)

XORed = []
if(len(List_val1) == len(List_val2)):
    for i, (value1, value2) in enumerate(zip(List_val1, List_val2)):
        # value2 = List_val2[i]
        XORed.append(format(int(value1, 16) ^ int(value2, 16),"01X"))
    
    print(XORed)
    Joined_XORed = ''.join(map(str,XORed))
    print(Joined_XORed)
        
else:
    print('Val1 and Val2 length does\'t match. Please input matching number of data.')
    
