import pygame
import sys
import time
import os
from pygame.locals import *

import midiInput
import codeGenerator
import displayRenderer
import configuration

MENU_STRUCTURE = ["1 - select midi input device",
                  "2 - display fullscreen: {}",
                  "3 - show debug info: {}",
                  "0 - close menu"]


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
        elif event.key == K_SPACE:
            result = "menu"
        elif event.key == K_0:
            result = "0"
        elif event.key == K_1:
            result = "1"
        elif event.key == K_2:
            result = "2"
        elif event.key == K_3:
            result = "3"
    return result


def format_menu_structure(set_fullscreen, show_debug):
    menu = list()
    menu.append(MENU_STRUCTURE[0])
    menu.append(MENU_STRUCTURE[1].format(str(set_fullscreen)))
    menu.append(MENU_STRUCTURE[2].format(str(show_debug)))
    menu.append(MENU_STRUCTURE[3])
    return menu


# main application loop
if __name__ == '__main__':
    pygame.init()
    debug_log = dict()
    configuration = configuration.Configuration(debug_log)
    configuration.load(os.path.normpath("data/config.json"))
    display = displayRenderer.DisplayRenderer(debug_log)
    fullscreen = configuration.get_config('FULL_SCREEN')
    set_fullscreen = fullscreen
    show_debug = configuration.get_config('SHOW_DEBUG')
    chord = configuration.get_config('CHORD')
    show_menu = False
    menu_page = format_menu_structure(set_fullscreen, show_debug)
    display.open(fullscreen)
    midi = midiInput.MidiInput(debug_log)
    midi.open(configuration.get_config('MIDI_DEVICE_ID'))
    codeGen = codeGenerator.CodeGenerator()
    number = 0
    note_name = ""
    color = None
    while True:
        time.sleep(0.1)
        input_value = check_for_input()
        if input_value == "menu":
            show_menu = True
            menu_page = format_menu_structure(set_fullscreen, show_debug)
        if show_menu:
            if input_value == "0":
                show_menu = False
                if fullscreen != set_fullscreen:
                    fullscreen = set_fullscreen
                    display.open(fullscreen)
            elif input_value == "1":
                pass
            elif input_value == "2":
                set_fullscreen = not set_fullscreen
                menu_page = format_menu_structure(set_fullscreen, show_debug)
            elif input_value == "3":
                show_debug = not show_debug
                menu_page = format_menu_structure(set_fullscreen, show_debug)
            display.render_menu(menu_page)
        elif show_debug:
            debug_log['midi_connected'] = str(midi.connected)
            display.render_state()
        if midi.connected:
            midi.read_data()
        number = codeGen.calc_number(midi.midi_data)
        note_name = codeGen.calc_note_name(midi.get_flat_midi_data(), chord)
        color = codeGen.calc_color(midi.midi_data)
        display.render_number(number, color)
        display.render_note_name(note_name, color)
        display.render_note_image(note_name, color)
        display.update()
