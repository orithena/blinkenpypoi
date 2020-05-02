import micropython

class objdict(dict):
    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError("No such attribute: " + name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("No such attribute: " + name)

def timed_function(f, *args, **kwargs):
    myname = str(f).split(' ')[1]
    def new_func(*args, **kwargs):
        t = utime.ticks_us()
        result = f(*args, **kwargs)
        delta = utime.ticks_diff(utime.ticks_us(), t)
        print('Function {} Time = {:6.3f}ms'.format(myname, delta/1000))
        return result
    return new_func

HSV_SECTION_3 = const(86)

@micropython.viper
def hsv2rgb(h: int, s: int, v:int, buf: ptr8):
    value = int(v)
    saturation = int(s)

    invsat = 255 - saturation
    brightness_floor = (value * invsat) // 256

    color_amplitude = value - brightness_floor

    section = int(h // HSV_SECTION_3)  
    offset = int(h % HSV_SECTION_3)    

    rampup = offset   
    rampdown = int((HSV_SECTION_3 - 1) - offset) 

    rampup_amp_adj   = int((rampup   * color_amplitude) // HSV_SECTION_3)
    rampdown_amp_adj = int((rampdown * color_amplitude) // HSV_SECTION_3)

    rampup_adj_with_floor   = rampup_amp_adj   + brightness_floor
    rampdown_adj_with_floor = rampdown_amp_adj + brightness_floor

    if section > 0 :
        if section == 1:
            buf[0] = brightness_floor
            buf[1] = rampdown_adj_with_floor
            buf[2] = rampup_adj_with_floor
        else:
            buf[0] = rampup_adj_with_floor
            buf[1] = brightness_floor
            buf[2] = rampdown_adj_with_floor
    else:
        buf[0] = rampdown_adj_with_floor
        buf[1] = rampup_adj_with_floor
        buf[2] = brightness_floor

    
