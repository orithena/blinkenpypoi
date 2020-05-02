import machine, esp, utime, gc
from machine import SPI, Pin
from util.utils import objdict, hsv2rgb, timed_function
from micropython import const

class ColorSpace:
    RGB = const(0)
    HSV = const(1)
    
class Repetition:
    NOPE = const(-1)
    OK = const(0)
    YES = const(1)

@micropython.native
class LED:
    def __init__(self, led_fb):
        self.framebuffer = led_fb
    def setRGB(self, r, g, b):
        self.framebuffer[0] = 0xff    # global pixel brightness = full, because of low-frequency brightness pwm 
        self.framebuffer[1] = r
        self.framebuffer[2] = g
        self.framebuffer[3] = b
    def setHSV(self, h:int, s:int, v: int):
        self.framebuffer[0] = 0xff    # global pixel brightness = full, because of low-frequency brightness pwm 
        hsv2rgb(h,s,v, self.framebuffer[1:4])
    def getRGB(self):
        return (self.framebuffer[1], self.framebuffer[2], self.framebuffer[3])

@micropython.native
class LEDs:
    MAP_LINEAR=const(0)
    MAP_DOUBLE_LINEAR=const(1)
    
    def __init__(self, pixel_count=25, mapper=MAP_DOUBLE_LINEAR, baud=20000000, sck=17, mosi=16, miso=18):
        self._spi = SPI(2, baudrate=baud, sck=Pin(sck), mosi=Pin(mosi), miso=Pin(miso))
        self.pixel_count = pixel_count
        self.framebuffer = bytearray(pixel_count*4)
        self.fbview = memoryview(self.framebuffer)
        self.outputsize = 4+(pixel_count*4)+4
        self.output = bytearray(self.outputsize)
        self._led = LED(self.framebuffer[0:4])
    def __getitem__(self, idx):
        pos = idx*4
        self._led.framebuffer = self.fbview[pos:pos+4]
        return self._led
    def show(self):
        self.output[0] = 0x00
        self.output[1] = 0x00
        self.output[2] = 0x00
        self.output[3] = 0x00
        for a in range(self.pixel_count):
            p = a * 4
            self.output[p+4] = self.framebuffer[p]
            self.output[p+5] = self.framebuffer[p+3]
            self.output[p+6] = self.framebuffer[p+2]
            self.output[p+7] = self.framebuffer[p+1]
        self.output[self.outputsize-4] = 0xff
        self.output[self.outputsize-3] = 0xff
        self.output[self.outputsize-2] = 0xff
        self.output[self.outputsize-1] = 0xff
        self._spi.write(self.output)
            

class BlinkenPyPoi:
    def __init__(self):
        self.state = PoiState()
        self.state.leds = LEDs()
    
    def mixer(self):
        t1 = utime.ticks_us()
        for effect in self.state.effects:
            effect.paint(self.state)
            t2 = utime.ticks_us()
            gc.collect()
            t3 = utime.ticks_us()
        self.state.leds.show()
        t4 = utime.ticks_us()
        print(t2-t1, t3-t2, t4-t3, t4-t1)
            
    def loop(self):
        while(True):
            self.state.hue = (self.state.hue + 1) % 255
            self.mixer()


@micropython.native
class PoiState(objdict):
    def __init__(self, led_count=25):
        self.ms = 0
        self.frame = 0
        self.effects = [ Effect(), ]
        self.hue = 0
        
@micropython.native
class Effect:
    def __init__(self):
        self.priority = 0
        self.colorspace = ColorSpace.RGB
        self.repeat = Repetition.OK
        print("Effect initialized")
    def paint(self, state):
        for a in range(0,25):
            state.leds[a].setHSV(state.hue, 255, 255)
