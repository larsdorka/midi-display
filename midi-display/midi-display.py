import pygame
import sys
import time
from pygame.locals import *

import midiInput
import codeGenerator
import displayRenderer

# configuration constants
FULL_SCREEN = False
MIDI_DEVICE_ID = -1


# main application loop
if __name__ == '__main__':
    pygame.init()
    display = displayRenderer.DisplayRenderer()
    display.open(FULL_SCREEN)
    midi = midiInput.MidiInput()
    midi.open(MIDI_DEVICE_ID)
    codeGen = codeGenerator.CodeGenerator()
    # codeGen.algorithm = "counter"
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
        new_number = codeGen.calc_number(midi.midiData)
        if new_number != old_number:
            display.render_number(new_number, codeGen.calc_color(midi.midiData))
            # display.renderNumber(new_number)
            old_number = new_number
