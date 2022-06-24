from machine import Pin
import time
import array as arr

class HX711(object):
    
    GAIN = 1
    SCALE = 1
    OFFSET = 0
    def __init__(self, dt, sck, gain = 128):   
        self.dt_pin = Pin(dt, Pin.IN, Pin.PULL_UP)
        self.sck_pin = Pin(sck, Pin.OUT) 
        
        self.set_gain(gain);
            
    def set_gain(self, gain):
        if(gain == 128):
            self.GAIN = 1
        if(gain == 64):
            self.GAIN = 3
        if(gain == 32):
            self.GAIN = 2
            
    def tare(self, value = 1):
        self.set_offset(self.read_average(value))
            
    def set_scale(self, value):
        self.SCALE = value;
    
    def set_offset(self, value):
        self.OFFSET = value;
        
    def is_ready(self):
        return self.dt_pin.value() == 0;
        
    def is_read(self):
        pass;
    
    def wait_ready(self, delay_ms):
        pass;
    
    def get_value(self, count = 10):
        return self.read_average(count) - self.OFFSET # add offset tare
    
    def get_units(self, count = 10):
        return self.get_value(count) / self.SCALE;
        
    def read_average(self, count = 10):
        sumValues = 0
        for i in range(0, count):
            sumValues += self.read();
            time.sleep_us(1);
             
        return sumValues / count;
    
    def read(self):
        value = 0;
        data = arr.array('i',[0,0,0]);
        filler = 0x00;
        self.sck_pin.off();
        data[2] = self.shiftInSlow();
        data[1] = self.shiftInSlow();
        data[0] = self.shiftInSlow();
        
        for i in range(0, self.GAIN):
            self.sck_pin.on();
            time.sleep_us(1);
            self.sck_pin.off();
            
        if (data[2] & 0x80):
            filler = 0xFF;
        else:
            filler = 0x00;
            
        value = filler << 24 | data[2] << 16 | data[1] << 8 | data[0];
        return value;
	
    
    def shiftInSlow(self):
        value8_t = 0;
        self.sck_pin.off();
        time.sleep_us(1);
        for i in range(0, 8):
            self.sck_pin.on();
            time.sleep_us(1);
            d = self.dt_pin.value()
            self.sck_pin.off();
            value8_t |= d<< (7 - i)
            time.sleep_us(1);
            
        return value8_t;
