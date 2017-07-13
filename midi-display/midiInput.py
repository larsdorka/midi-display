import pygame
import pygame.midi


class MidiInput:
    """class for handling all the midi input data"""

    def __init__(self, debug_log=dict()):
        """constructor
        :param debug_log: dictionary to write log entries into
        """
        self.debug_log = debug_log
        self.midi_data = None
        self.connected = False
        self.midi_device = None
        pygame.midi.init()
        self.clear_data()

    def open(self, device_id=-1):
        """initializes the given midi input device or the standard device
        :param device_id: the device_id of the midi input device to open, omit to use default device
        """
        self.debug_log['midi'] = ""
        self.debug_log['midi_connected'] = ""
        self.debug_log['midi_message'] = ""
        if self.midi_device is not None:
            self.midi_device.close()
            self.midi_device = None
        self.connected = False
        if device_id >= 0:
            try:
                self.midi_device = pygame.midi.Input(device_id)
            except pygame.midi.MidiException as ex:
                self.debug_log['midi'] = "error opening midi device: " + str(ex)
            else:
                self.debug_log['midi'] = "midi device: " + str(pygame.midi.get_device_info(device_id)[1])
                self.connected = True
        else:
            default_input_id = pygame.midi.get_default_input_id()
            if default_input_id >= 0:
                try:
                    self.midi_device = pygame.midi.Input(default_input_id)
                except pygame.midi.MidiException as ex:
                    self.debug_log['midi'] = "error opening midi device: " + str(ex)
                else:
                    self.debug_log['midi'] = "midi device: " + str(pygame.midi.get_device_info(default_input_id)[1])
                    self.connected = True
            else:
                self.debug_log['midi'] = "no midi default device found"
                self.midi_device = None
                self.connected = False

    def clear_data(self):
        """clears the midi data store"""
        self.midi_data = []
        for index in range(128):
            self.midi_data.append(0)

    def read_data(self):
        """reads midi input data and stores the key/velocity data in the midi data store"""
        midi_messages = []
        try:
            while self.midi_device.poll():
                midi_messages.append(self.midi_device.read(1))
        except pygame.midi.MidiException as ex:
            self.debug_log['midi'] = "error reading midi device: " + str(ex)
        if midi_messages is not []:
            for message in midi_messages:
                if len(message) > 0:
                    if len(message[0]) > 0:
                        status = message[0][0][0] & 240
                        channel = (message[0][0][0] & 15) + 1
                        key = message[0][0][1]
                        velocity = message[0][0][2]
                        if status == 144:
                            status_event = "keyOn"
                            self.midi_data[key] = velocity
                        elif status == 128:
                            status_event = "keyOff"
                            self.midi_data[key] = 0
                        else:
                            status_event = "none"
                        self.debug_log['midi_message'] = ("last message: status {}, status_event {}, channel {}, "
                                                          "key {}, velocity {}"
                                                          .format(status, status_event, channel, key, velocity))

    def close(self):
        """closes the midi input device"""
        if self.midi_device is not None:
            try:
                self.midi_device.close()
            except pygame.midi.MidiException as ex:
                self.debug_log['midi'] = "error closing midi device: " + str(ex)
