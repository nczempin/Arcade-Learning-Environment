#!/usr/bin/env python3
# python_example.py
# Author: Ben Goodrich
#
# This is a direct port to python of the shared library example from
# ALE provided in doc/examples/sharedLibraryInterfaceExample.cpp
import sys, os, distutils.util
import numpy as np
from random import randrange
from ale_python_interface import ALEInterface
from OpenGL.raw.WGL._types import LPRECT
from IPython.nbformat import current

if len(sys.argv) < 2:
  print('Usage: %s rom_file' % sys.argv[0])
  sys.exit()

ale = ALEInterface()
# Get & Set the desired settings
ale.setInt(b'random_seed', 123)

# Load the ROM file
rom_file = str.encode(sys.argv[1])
ale.loadROM(rom_file)
# Get the list of legal actions
legal_actions = ale.getLegalActionSet()

ram_size = ale.getRAMSize()
ignore = 0
directions = []
previous_ram = np.zeros(ram_size, dtype=np.uint8)  # np.array(ram_size, dtype=np.uint8)
current_ram = np.zeros(ram_size, dtype=np.uint8)
ale.getRAM(previous_ram)
score_candidates = [0xb9]
candidates = []
for i in range(0x80):
    candidates.append(i)
for i in range(len(score_candidates)):
    score_candidates[i] = score_candidates[i] & 0x7f

lives_start = 3
lives_candidates = [0xe0]
for i in range(len(lives_candidates)):
    lives_candidates[i] = lives_candidates[i] & 0x7f
for i in range(ram_size):
    if (previous_ram.item(i)!=0):
        #print ("ignoring: ", i)
        directions.append(0)
    else:
        directions.append(None)
#        if (i>1 and previous_ram.item(i-1)==0):
#            candidates.append(i)
        


#ignore the first few frames
for i in range(100):
    ale.act(0)

total_reward = 0
ale.getRAM(current_ram)
to_remove = []
for i in range(0x80):
    if (i>1 and (current_ram.item(i) != 0 or current_ram.item(i-1))):
        to_remove.append(i)
candidates = [x for x in candidates if not x in to_remove]

print ("candidates after removing non-zeroes: ", candidates)            


while not ale.game_over():
#for i in range(500):
    a = legal_actions[randrange(len(legal_actions))]
    # Apply an action and get the resulting reward
    reward = ale.act(a);
    ale.getRAM(current_ram)
    
    to_remove = []
    for i in candidates:
        pr = previous_ram.item(i)
        cr = current_ram.item(i)
        diff = cr - pr
        if (i >0 and diff < 0): #number went down
            lpr = previous_ram.item(i-1)
            lcr = current_ram.item(i-1)
            ld = lcr - lpr
            if (ld != 1): # number to the left didn't go up
                to_remove.append(i)
    if (len(to_remove)> 0):
        print("removing: ", to_remove)
        print ("candidates left: ", candidates)
        for j in candidates:  
            if (j>0):
                print(hex(j), ": ", hex(current_ram.item(j-1)), hex(current_ram.item(j)), hex(current_ram.item(j+1)))
          

    candidates = [x for x in candidates if not x in to_remove]            
    #for i in range(ram_size):
#         d = directions[i]
#         pr = previous_ram.item(i)
#         cr = current_ram.item(i)
#         diff = cr - pr
#         if ((i&0x7f) in score_candidates):
#             print("***check score: ",hex(i), ": ", hex(pr),"=",pr, "->", hex(cr),"=",cr, "  d=", d)
# 
# 
#         if ((i&0x7f) in lives_candidates):
#             print("***checklives: ",hex(i), ": ", hex(pr),"=",pr, "->", hex(cr),"=",cr, "  d=", d)
#         if (d != 0):
#             pr = previous_ram.item(i)
#             cr = current_ram.item(i)
#             diff = cr - pr
#             if (d == None or d == 1):
#                 if (cr > pr):
#                     directions[i] = 1
#                     if (len(score_candidates) >0):
#                         if (i in score_candidates):
#                             print (hex(i), ": ", hex(pr),"=",pr, "->", hex(cr),"=",cr)
#                             for j in score_candidates:
#                                 ppr = previous_ram.item(j)
#                                 ccr = current_ram.item(j)
#                                 if (i >0 and i < 0x80):
#                                     print (hex(j), ": ", hex(ppr),"=",ppr, "->", hex(ccr),"=",ccr)
#                     else:
#                         print (hex(i), ": ", hex(pr),"=",pr, "->", hex(cr),"=",cr)
# 
#                     print("==============================")
#                 elif (cr < pr):
#                     directions[i] = -1
#             elif (d == 1):
#                 if (cr < pr):
#                     if (i >0 and (directions[i-1]==1 or directions[i-1]==None)):
#                         #print ("juicy: ", hex(i), "=", i)
# #                            if (i==candidate):
# #                                print ("candy!!")
# #                        else:
#                         directions[i] = 0
#                 #elif (cr > pr):
#                     #print (hex(i), ": ", hex(pr),"=",pr, "->", hex(cr),"=",cr)
# #            if (d == None or d == -1 ):
#         if ((lives_start == None or lives_start>=cr) and diff==-1 and ((len(lives_candidates)==0 and cr < 10)  or (i in lives_candidates))):
#                     #if (cr == 0):
#             print ("lives?", hex(i), ": ", hex(pr),"=",pr, "->", hex(cr),"=",cr)
#      #       elif (ignore == 0 and cr > pr+1):
#      #               directions[i] = 0
#     count = 0
#     for i in range(ram_size):
#         d = directions[i]
#         if (d == 1):
#             count += 1
#     #if (count > 0):
#      #   print (count)
#     if (count < 25):
#         for i in range(ram_size):
#             d = directions[i]
            #if (d == 1):
                #print (i , ", " , current_ram.item(i), ": ", hex(current_ram.item(i)))
#     print (previous_ram.item(0), ", ", previous_ram.item(1), ", ", hex(previous_ram.item(2)))
#     print (current_ram.item(0), ", ", current_ram.item(1), ", ", hex(current_ram.item(2)))
    previous_ram = current_ram.copy()
                             
#     total_reward += reward
#     if (reward > 0):
#         print ("reward ", reward, "->" , total_reward);
#print('Episode %d ended with score: %d' % (episode, total_reward))
print ("candidates left: ", candidates)
for j in candidates:  
    if (j>0):
        print(hex(j), ": ", hex(current_ram.item(j-1)), hex(current_ram.item(j)), hex(current_ram.item(j+1)))

ale.reset_game()
