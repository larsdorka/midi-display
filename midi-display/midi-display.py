import pygame
import sys
import time
from pygame.locals import *

import midiInput
import codeGenerator
import displayRenderer

# configuration constants
FULL_SCREEN = False  # set to False to display in 1024/768 window
MIDI_DEVICE_ID = -1  # set to -1 to use default device
SHOW_DEBUG = True  # set to True to render debug info on the screen


def terminate():
    """terminate the program"""
    midi.close()
    pygame.quit()
    sys.exit()


def check_for_quit():
    """process termination request"""
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()


# main application loop
if __name__ == '__main__':
    pygame.init()
    debug_log = dict()
    display = displayRenderer.DisplayRenderer(debug_log)
    display.open(FULL_SCREEN)
    midi = midiInput.MidiInput(debug_log)
    midi.open(MIDI_DEVICE_ID)
    codeGen = codeGenerator.CodeGenerator()
    # codeGen = codeGenerator.CodeGenerator(codeGenerator.Algorithm.COUNTER)
    number = 0
    while True:
        time.sleep(0.1)
        check_for_quit()
        if midi.connected:
            midi.read_data()
        if SHOW_DEBUG:
            debug_log['midi_connected'] = str(midi.connected)
            display.render_state()
        number = codeGen.calc_number(midi.midiData)
        number = codeGen.calc_number(midi.midiData)
        display.render_number(number, codeGen.calc_color(midi.midiData))
        # display.render_number(number)
        display.update()
