import pygame
import pygame.midi


class MidiInput:
    """class for handling all the midi input data"""
    
    def __init__(self):
        self.midiData = None
        self.connected = False
        self.midiDevice = None
        pygame.midi.init()
        self.clearData()
        
    def open(self, deviceId=-1):
        if self.midiDevice is not None:
            self.midiDevice.close()
            self.midiDevice = None
        if deviceId >= 0:
            self.midiDevice = pygame.midi.Input(deviceId)
        else:
            defaultInputId = pygame.midi.get_default_input_id()
            if defaultInputId >= 0:   
                print(pygame.midi.get_device_info(defaultInputId))
                self.midiDevice = pygame.midi.Input(defaultInputId)
                self.connected = True
            else:
                print("ERROR: no midi default device found!")
                self.midiDevice = None
                self.connected = False

    def clearData(self):
        self.midiData = []
        for index in range(128):
            self.midiData.append(0)

    def readData(self):
            midiInputData = []
            while self.midiDevice.poll():
                midiInputData.append(self.midiDevice.read(1))
            if midiInputData is []:
                for message in midiInputData:
                    print(message)
                    if len(message) > 0:
                        if len(message[0]) > 0:
                            status = message[0][0][0] & 240
                            key = message[0][0][1]
                            velocity = message[0][0][2]
                            print("status: {}, key: {}, velocity: {}".format(status, key, velocity))
                            self.midiData[key] = velocity
