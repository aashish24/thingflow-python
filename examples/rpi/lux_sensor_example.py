"""Demo of lux sensor and led from raspberry pi
"""
import sys
import asyncio
import os.path

from thingflow.base import Scheduler, SensorAsOutputThing
from thingflow.sensors.rpi.lux_sensor import LuxSensor
from thingflow.adapters.rpi.gpio import GpioPinOut
import thingflow.adapters.csv
import thingflow.filters.select

    
            

def setup(threshold=25):
    lux = SensorAsOutputThing(LuxSensor())
    lux.connect(print)
    lux.csv_writer(os.path.expanduser('~/lux.csv'))
    led = GpioPinOut()
    actions = lux.map(lambda event: event.val > threshold)
    actions.connect(led)
    actions.connect(lambda v: print('ON' if v else 'OFF'))
    lux.print_downstream()
    return (lux, led)
    

def main(argv=sys.argv[1:]):
    if len(argv)!=2:
        print("%s threshold interval" % sys.argv[0])
        return 1
    threshold = float(argv[0])
    interval = float(argv[1])
    print("%f seconds interval and an led threshold of %f lux" %
          (interval, threshold))
    (lux, led) = setup(threshold)
    scheduler = Scheduler(asyncio.get_event_loop())
    stop = scheduler.schedule_periodic_on_separate_thread(lux, interval)
    print("starting run...")
    try:
        scheduler.run_forever()
    except KeyboardInterrupt:
        led.on_completed()
        stop()
    return 0

if __name__ == '__main__':
    main()
