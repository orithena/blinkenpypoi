import machine, esp, utime
from machine import SPI, Pin
from micropython_dotstar import DotStar, START_HEADER_SIZE
from util.utils import objdict, hsv2rgb
from micropython import const

class ColorSpace:
    RGB = const(0)
    HSV = const(1)
    
class Repetition:
    NOPE = const(-1)
    OK = const(0)
    YES = const(1)

class BlinkenPyPoi:
    def __init__(self):
        self.spi = SPI(2, baudrate=20000000, sck=Pin(17), mosi=Pin(16), miso=Pin(18))
        self.leds = DotStar(self.spi, 25)
        self.state = PoiState()
        self.state.leds = memoryview(self.leds._buf)[START_HEADER_SIZE:START_HEADER_SIZE+100]
    
    def mixer(self):
        for effect in self.state.effects:
            effect.paint(self.state)
        self.leds.show()
            
    def loop(self):
        while(True):
            self.state.hue = (self.state.hue + 1) % 255
            self.mixer()


class PoiState(objdict):
    def __init__(self, led_count=25):
        self.ms = 0
        self.frame = 0
        self.effects = [ Effect(), ]
        self.hue = 0
        
        
class Effect:
    def __init__(self):
        self.priority = 0
        self.colorspace = ColorSpace.RGB
        self.repeat = Repetition.OK
        print("Effect initialized")
    def paint(self, state):
        for a in range(0,25):
            x = (a*4)
            state.leds[x+0] = 255
            hsv2rgb(state.hue, 255, 255, state.leds[x+1:x+4])
