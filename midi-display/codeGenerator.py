class CodeGenerator:
    '''class to generate numbers and colors from midi data'''
    
    def __init__(self):
        self.algorithm = "default"
        self.calculateColor = True
        
    
    def calcNumber(self, midiData):
        number = 0
        if self.algorithm == "default":
            for index in range(128):
                if midiData[index] > 0:
                    number += 2 ** (index % 16)
            number %= 100000
        return number


    def calcColor(self, midiData):
        if self.calculateColor == False:
            return (255, 255, 255)
        color = 0
        keyCounter = 0
        for index in range(128):
            if midiData[index] > 0:
                keyCounter += 1
                color += midiData[index] * 2
        print (keyCounter)
        if keyCounter == 0:
            return (0, 0, 0)
        color = color // keyCounter
        color = min(color, 255)
        print (color)
        return (color, color, color)
