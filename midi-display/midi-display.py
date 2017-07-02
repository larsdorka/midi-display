import pygame
import sys
import time
from pygame.locals import *

import midiInput
import codeGenerator
import displayRenderer

# configuration constants
FULL_SCREEN = False     # set to False to display in 1024/768 window
MIDI_DEVICE_ID = -1     # set to -1 to use default device
SHOW_DEBUG = False      # set to True to render debug info on the screen


# main application loop
if __name__ == '__main__':
    pygame.init()
    display = displayRenderer.DisplayRenderer()
    display.open(FULL_SCREEN)
    midi = midiInput.MidiInput()
    midi.open(MIDI_DEVICE_ID)
    codeGen = codeGenerator.CodeGenerator()
    # codeGen = codeGenerator.CodeGenerator(codeGenerator.Algorithm.COUNTER)
    old_number = 0
    new_number = 0
    while True:
        time.sleep(0.1)
        for event in pygame.event.get(KEYUP):
            if event.key == K_ESCAPE:
                midi.close()
                pygame.quit()
                sys.exit()
        if midi.connected:
            midi.read_data()
        if SHOW_DEBUG:
            display.render_state()
        new_number = codeGen.calc_number(midi.midiData)
        if new_number != old_number:
            display.render_number(new_number, codeGen.calc_color(midi.midiData))
            # display.renderNumber(new_number)
            old_number = new_number
        display.update()
