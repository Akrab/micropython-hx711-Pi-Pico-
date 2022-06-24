# micropython-hx711-Pi-Pico
Read HX711 ADC for Weigh Scales on Rasperry Pico
```python
from hx711 import HX711

hx711 = HX711(dt = 17, sck = 16);
hx711.set_scale(1);
hx711.tare();

# check in wait loop
if(hx711.is_ready()):
    units = hx711.get_units(1)
    print(units);
```
