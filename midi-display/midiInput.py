import pygame
import pygame.midi


class MidiInput:
    """class for handling all the midi input data"""
    
    def __init__(self):
        self.midiData = None
        self.connected = False
        self.midiDevice = None
        pygame.midi.init()
        self.clear_data()
        
    def open(self, device_id=-1):
        if self.midiDevice is not None:
            self.midiDevice.close()
            self.midiDevice = None
        if device_id >= 0:
            self.midiDevice = pygame.midi.Input(device_id)
        else:
            default_input_id = pygame.midi.get_default_input_id()
            if default_input_id >= 0:
                print(pygame.midi.get_device_info(default_input_id))
                self.midiDevice = pygame.midi.Input(default_input_id)
                self.connected = True
            else:
                print("ERROR: no midi default device found!")
                self.midiDevice = None
                self.connected = False

    def clear_data(self):
        self.midiData = []
        for index in range(128):
            self.midiData.append(0)

    def read_data(self):
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
        if self.midiDevice is not None:
            self.midiDevice.close()
