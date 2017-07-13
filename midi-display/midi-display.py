import pygame
import sys
import time
from pygame.locals import *

import midiInput
import codeGenerator
import displayRenderer
import configuration


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
    configuration = configuration.Configuration(debug_log)
    configuration.load("config.json")
    display = displayRenderer.DisplayRenderer(debug_log)
    display.open(configuration.get_config("FULL_SCREEN"))
    midi = midiInput.MidiInput(debug_log)
    midi.open(configuration.get_config("MIDI_DEVICE_ID"))
    codeGen = codeGenerator.CodeGenerator()
    # codeGen = codeGenerator.CodeGenerator(codeGenerator.Algorithm.COUNTER)
    number = 0
    show_debug = configuration.get_config("SHOW_DEBUG")
    while True:
        time.sleep(0.1)
        check_for_quit()
        if midi.connected:
            midi.read_data()
        if show_debug:
            debug_log['midi_connected'] = str(midi.connected)
            display.render_state()
        number = codeGen.calc_number(midi.midi_data)
        number = codeGen.calc_number(midi.midi_data)
        display.render_number(number, codeGen.calc_color(midi.midi_data))
        # display.render_number(number)
        display.update()
