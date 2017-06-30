import pygame
import sys
import time
from pygame.locals import *

import midiInput
import codeGenerator
import displayRenderer

# configuration constants
FULLSCREEN = False
MIDIDEVICEID = -1


# exit application
def checkForExit():
    for event in pygame.event.get(KEYUP):
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
                

# main application loop
if __name__ == '__main__':
    pygame.init()
    display = displayRenderer.DisplayRenderer()
    display.open()
    midi = midiInput.MidiInput()
    midi.open(MIDIDEVICEID)
    codeGen = codeGenerator.CodeGenerator()
    # codeGen.algorithm = "counter"
    old_number = 0
    new_number = 0
    while True:
        time.sleep(0.1)
        checkForExit()
        if midi.connected:
            midi.readData()
        new_number = codeGen.calcNumber(midi.midiData)
        if new_number != old_number:
            display.renderNumber(new_number, codeGen.calcColor(midi.midiData))
            # display.renderNumber(new_number)
            old_number = new_number
