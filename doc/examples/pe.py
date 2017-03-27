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

if len(sys.argv) < 2:
  print('Usage: %s rom_file' % sys.argv[0])
  sys.exit()

ale = ALEInterface()
print("1")
# Get & Set the desired settings
ale.setInt(b'random_seed', 123)

# Set USE_SDL to true to display the screen. ALE must be compilied
# with SDL enabled for this to work. On OSX, pygame init is used to
# proxy-call SDL_main.
# USE_SDL = distutils.util.strtobool(os.environ["USE_SDL"])
USE_SDL = False
if USE_SDL:
  if sys.platform == 'darwin':
    import pygame
    pygame.init()
    ale.setBool('sound', False)  # Sound doesn't work on OSX
  elif sys.platform.startswith('linux'):
    ale.setBool(None, "j")  # True)  #3,"sound")#, 23)#True)
  ale.setBool('display_screen', True)

# Load the ROM file
rom_file = str.encode(sys.argv[1])
print("2")
ale.loadROM(rom_file)
print("3")
# Get the list of legal actions
legal_actions = ale.getLegalActionSet()

ram_size = ale.getRAMSize()
ignore = 0
directions = []
previous_ram = np.zeros(ram_size, dtype=np.uint8)  # np.array(ram_size, dtype=np.uint8)
current_ram = np.zeros(ram_size, dtype=np.uint8)
ale.getRAM(previous_ram)
for i in range(ram_size):
    if (previous_ram.item(i)>0):
        #print ("ignoring: ", i)
        directions.append(0)
    else:
         directions.append(None)

total_reward = 0
#while not ale.game_over():
for i in range(200):
    a = legal_actions[randrange(len(legal_actions))]
    # Apply an action and get the resulting reward
    reward = ale.act(a);
    if (ignore == 0):
        ale.getRAM(current_ram)
        #print (current_ram.item(2))
        for i in range(ram_size):
            d = directions[i]
            if (d != 0):
                pr = previous_ram.item(i)
                cr = current_ram.item(i)
                if d == None:
                    if (cr > pr):
                        directions[i] = 1
                        #print (hex(i), ": ", hex(pr),"=",pr, "->", hex(cr),"=",cr)
                    elif (cr < pr):
                        directions[i] = -1
                elif (d == 1):
                    if (cr < pr):
                        #if (i >0 and (directions[i-1]==1 or directions[i-1]==None)):
                            #print ("juicy: ", hex(i), "=", i)
                        directions[i] = 0
                    #elif (cr > pr):
                        #print (hex(i), ": ", hex(pr),"=",pr, "->", hex(cr),"=",cr)
                elif (d == -1):
                    if (cr > pr):
                        directions[i] = 0
        count = 0
        for i in range(ram_size):
            d = directions[i]
            if (d == 1):
                count += 1
        #if (count > 0):
         #   print (count)
        if (count < 25):
            for i in range(ram_size):
                d = directions[i]
                #if (d == 1):
                    #print (i , ", " , current_ram.item(i), ": ", hex(current_ram.item(i)))
    else:
        ignore -= 1
#     print (previous_ram.item(0), ", ", previous_ram.item(1), ", ", hex(previous_ram.item(2)))
#     print (current_ram.item(0), ", ", current_ram.item(1), ", ", hex(current_ram.item(2)))
    previous_ram = current_ram.copy()
                     
    total_reward += reward
#print('Episode %d ended with score: %d' % (episode, total_reward))
ale.reset_game()
