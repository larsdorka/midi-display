import pygame
import sys
import time
import os
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


def check_for_input():
    """process termination request"""
    result = ""
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        elif event.key == K_d:
            result = "debug"
    return result


# main application loop
if __name__ == '__main__':
    pygame.init()
    debug_log = dict()
    configuration = configuration.Configuration(debug_log)
    configuration.load(os.path.normpath("data/config.json"))
    display = displayRenderer.DisplayRenderer(debug_log)
    display.open(configuration.get_config('FULL_SCREEN'))
    midi = midiInput.MidiInput(debug_log)
    midi.open(configuration.get_config('MIDI_DEVICE_ID'))
    codeGen = codeGenerator.CodeGenerator()
    # codeGen = codeGenerator.CodeGenerator(codeGenerator.Algorithm.COUNTER)
    number = 0
    note_name = ""
    color = None
    show_debug = configuration.get_config('SHOW_DEBUG')
    chord = configuration.get_config('CHORD')
    while True:
        time.sleep(0.1)
        input_value = check_for_input()
        if input_value == "debug":
            show_debug = not show_debug
        if midi.connected:
            midi.read_data()
        if show_debug:
            debug_log['midi_connected'] = str(midi.connected)
            display.render_state()
        number = codeGen.calc_number(midi.midi_data)
        note_name = codeGen.calc_note_name(midi.get_flat_midi_data(), chord)
        color = codeGen.calc_color(midi.midi_data)
        display.render_number(number, color)
        display.render_note_name(note_name, color)
        display.render_note_image(note_name, color)
        display.update()
