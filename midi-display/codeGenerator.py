from enum import Enum, auto


class Algorithm(Enum):
    """enum to contain all the possible generator algorithms"""
    DEFAULT = auto()
    COUNTER = auto()


class CodeGenerator:
    """class to generate numbers and colors from midi data"""
    
    def __init__(self, algorithm=Algorithm.DEFAULT):
        """constructor
        :param algorithm: select the algorithm from enum with which to generate the number
        """
        self.algorithm = algorithm
        self.calculateColor = True
        self.counter = 0

    def calc_number(self, midi_data):
        """calculates a number from the midi data using the set algorithm
        :param midi_data: midi data to generate number from
        :return: number generated from midi data
        """
        number = 0
        if self.algorithm == Algorithm.DEFAULT:
            for index in range(128):
                if midi_data[index] > 0:
                    number += 2 ** (index % 16)
            number %= 100000
        elif self.algorithm == Algorithm.COUNTER:
            number = self.counter
            self.counter += 1
        else:
            number = 0
        return number

    def calc_color(self, midi_data):
        """calculates the text color from the midi data
        :param midi_data: midi data to render color from
        :return: color calculated from midi data
        """
        if self.calculateColor is False:
            return (255, 255, 255)
        color = 0
        key_counter = 0
        for index in range(128):
            if midi_data[index] > 0:
                key_counter += 1
                color += midi_data[index] * 2
        if key_counter == 0:
            return (0, 0, 0)
        color = color // key_counter
        color = min(color, 255)
        return (color, color, color)
