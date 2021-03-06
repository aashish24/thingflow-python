"""
This is an example thingflow program that is described in tutorial.rst.
"""

# First, let's define a sensor that generates a random number each time
# it is sampled.

import random
random.seed()
from thingflow.base import SensorAsOutputThing



class RandomSensor:
    def __init__(self, sensor_id, mean, stddev, stop_after):
        """This sensor will signal it is completed after the
        specified number of events have been sampled.
        """
        self.sensor_id = sensor_id
        self.mean = mean
        self.stddev = stddev
        self.events_left = stop_after

    def sample(self):
        if self.events_left>0:
            data = random.gauss(self.mean, self.stddev)
            self.events_left -= 1
            return data
        else:
            raise StopIteration
        
    def __str__(self):
        return "RandomSensor(%s, %s, %s)" % \
            (self.sensor_id, self.mean, self.stddev)


# Instantiate our sensor
MEAN = 100
STDDEV = 10
sensor = SensorAsOutputThing(RandomSensor(1, MEAN, STDDEV, stop_after=5))


# Now, we will define a pretend LED as a subscriber. Each time is it passed
# True, it will print 'On'. Each time it is passed False, it will print 'Off'.
from thingflow.base import InputThing
class LED(InputThing):
    def on_next(self, x):
        if x:
            print("On")
        else:
            print("Off")

    def on_error(self, e):
        print("Got an error: %s" % e)

    def on_completed(self):
        print("LED Completed")

    def __str__(self):
        return 'LED'

# instantiate an LED
led = LED()


# Now, build a pipeline to sample events returned from the sensor,
# convert to a boolean based on whether the value is greater than
# the mean, and output to the LED.
import thingflow.filters.map
sensor.map(lambda evt: evt.val > MEAN).connect(led)

# If you want to see the raw value of each sensor, just add the output() element
import thingflow.filters.output
sensor.output()

# Call a debug method on the base output_thing class to see the element tree rooted
# at sensor.
sensor.print_downstream()

# Now, we need to schedule the sensor to be sampled
import asyncio
from thingflow.base import Scheduler
scheduler = Scheduler(asyncio.get_event_loop())
scheduler.schedule_periodic(sensor, 1.0) # sample once a second
scheduler.run_forever() # run until all sensors complete
print("That's all folks!")
        

        
