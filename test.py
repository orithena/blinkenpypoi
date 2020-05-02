import utime

def timed_function(f, *args, **kwargs):
    myname = str(f).split(' ')[1]
    def new_func(*args, **kwargs):
        t = utime.ticks_us()
        result = f(*args, **kwargs)
        delta = utime.ticks_diff(utime.ticks_us(), t)
        print('Function {} Time = {:6.3f}ms'.format(myname, delta/1000))
        return result
    return new_func

def hsv2rgb(h,s,v, buf):
        h60 = h/60
        def f(n):
            k = (n + h60) % 6
            return v - (v * s * max(min(k, 4 - k, 1), 0))

        def f2(x):
            return round(f(x) * 255)

        buf[0] = f2(5)
        buf[1] = f2(3)
        buf[2] = f2(1)

HSV_SECTION_3 = const(86)

@micropython.viper
def hsv2rgb_raw(h: int, s: int, v:int, buf: ptr8):
    value = int(v)
    saturation = int(s)

    invsat = 255 - saturation
    brightness_floor = (value * invsat) // 256

    color_amplitude = value - brightness_floor

    section = int(h // HSV_SECTION_3)  # 0..2
    offset = int(h % HSV_SECTION_3)    # 0..63

    rampup = offset   # 0..63
    rampdown = int((HSV_SECTION_3 - 1) - offset)  # 63..0

    rampup_amp_adj   = int((rampup   * color_amplitude) // HSV_SECTION_3)
    rampdown_amp_adj = int((rampdown * color_amplitude) // HSV_SECTION_3)

    rampup_adj_with_floor   = rampup_amp_adj   + brightness_floor
    rampdown_adj_with_floor = rampdown_amp_adj + brightness_floor

    if section > 0 :
        if section == 1:
            # section 1: 0x40..0x7F
            buf[0] = brightness_floor
            buf[1] = rampdown_adj_with_floor
            buf[2] = rampup_adj_with_floor
        else:
            # section 2; 0x80..0xBF
            buf[0] = rampup_adj_with_floor
            buf[1] = brightness_floor
            buf[2] = rampdown_adj_with_floor
    else:
        # section 0: 0x00..0x3F
        buf[0] = rampdown_adj_with_floor
        buf[1] = rampup_adj_with_floor
        buf[2] = brightness_floor

def printhsv():
    buf = bytearray(3)
    for a in range(256):
        hsv2rgb_raw(a,255,255,buf)
        print(a,":",buf[0],buf[1],buf[2])

@timed_function
def floatmul():
    a = 1.001
    for x in range(1000):
        a = a * a
    return a

@timed_function
def floatdiv():
    a = 1.001
    for x in range(1000):
        a = a / 1.001
    return a

@timed_function
def floatmulv():
    return  floatmulviper()
    
@micropython.viper
def floatmulviper():
    a = float(1.001)
    for x in range(1000):
        a = a * a
    return a

@timed_function
def floatdivv():
    return floatdivviper()
    
@micropython.viper
def floatdivviper():
    a = float(1.001)
    for x in range(1000):
        a = a / 1.001
    return a

@timed_function
def floatmuln():
    return  floatmulnative()
    
@micropython.native
def floatmulnative():
    a = float(1.001)
    for x in range(1000):
        a = a * a
    return a

@timed_function
def floatdivn():
    return floatdivnative()
    
@micropython.native
def floatdivnative():
    a = float(1.001)
    for x in range(1000):
        a = a / 1.001
    return a

@timed_function
def test1():
    buf = bytearray(3)
    hsv2rgb(0, 1.0, 1.0, buf)
    return buf
    
@timed_function
def test100():
    buf = bytearray(3)
    for a in range(360):
        hsv2rgb(a, 1.0, 1.0, buf)
    return buf
    
@timed_function
def ftest1():
    buf = bytearray(3)
    hsv2rgb_raw(0, 255, 255, buf)
    return buf
    
@timed_function
def ftest100():
    buf = bytearray(3)
    for a in range(255):
        hsv2rgb_raw(a, 255, 255, buf)
    return buf
    
printhsv()
print("Test: hsv2rgb Python 1 round:", test1())
print("Test: hsv2rgb Python 360 rounds:", test100())
print("Test: hsv2rgb Viper 1 round:", ftest1())
print("Test: hsv2rgb Viper 255 rounds:", ftest100())
print("Test: 1000 floatmul:", floatmul())
print("Test: 1000 floatdiv:", floatdiv())
print("Test: 1000 floatmulviper:", floatmulv())
print("Test: 1000 floatdivviper:", floatdivv())
print("Test: 1000 floatmulnative:", floatmuln())
print("Test: 1000 floatdivnative:", floatdivn())
