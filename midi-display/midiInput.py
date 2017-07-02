import pygame
import pygame.midi


class MidiInput:
    """class for handling all the midi input data"""

    def __init__(self, debug_log=dict()):
        self.debug_log = debug_log
        self.midiData = None
        self.connected = False
        self.midiDevice = None
        pygame.midi.init()
        self.clear_data()

    def open(self, device_id=-1):
        """initializes the given midi input device or the standard device"""
        self.debug_log['midi'] = ""
        if self.midiDevice is not None:
            self.midiDevice.close()
            self.midiDevice = None
        self.connected = False
        if device_id >= 0:
            try:
                self.midiDevice = pygame.midi.Input(device_id)
            except pygame.midi.MidiException as ex:
                self.debug_log['midi'] = "error opening midi device: " + str(ex)
            else:
                self.debug_log['midi'] = "midi device: " + str(pygame.midi.get_device_info(device_id)[1])
                self.connected = True
        else:
            default_input_id = pygame.midi.get_default_input_id()
            if default_input_id >= 0:
                try:
                    self.midiDevice = pygame.midi.Input(default_input_id)
                except pygame.midi.MidiException as ex:
                    self.debug_log['midi'] = "error opening midi device: " + str(ex)
                else:
                    self.debug_log['midi'] = "midi device: " + str(pygame.midi.get_device_info(default_input_id)[1])
                    self.connected = True
            else:
                self.debug_log['midi'] = "no midi default device found"
                self.midiDevice = None
                self.connected = False

    def clear_data(self):
        """clears the midi data store"""
        self.midiData = []
        for index in range(128):
            self.midiData.append(0)

    def read_data(self):
        """reads midi input data and stores the key/velocity data in the midi data store"""
        midi_messages = []
        while self.midiDevice.poll():
            midi_messages.append(self.midiDevice.read(1))
        if midi_messages is not []:
            for message in midi_messages:
                print(message)
                if len(message) > 0:
                    if len(message[0]) > 0:
                        status = message[0][0][0] & 240
                        key = message[0][0][1]
                        velocity = message[0][0][2]
                        print("status: {}, key: {}, velocity: {}".format(status, key, velocity))
                        self.midiData[key] = velocity

    def close(self):
        """closes the midi input device"""
        if self.midiDevice is not None:
            self.midiDevice.close()
