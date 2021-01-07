#!/usr/bin/env python

import glob
import os
import sys

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

import random
import time
import numpy as np

def main():
    client = carla.Client('localhost', 2000)
    client.set_timeout(2.0)
    world = client.load_world('Town02')
    weather = carla.WeatherParameters(
        cloudiness=0.0,
        precipitation=0.0,
        sun_altitude_angle=50.0)
    world.set_weather(weather)
    model3_bp = world.get_blueprint_library().find('vehicle.tesla.model3')
    model3_bp.set_attribute('color', '255,255,255')
    spawn_points = world.get_map().get_spawn_points()
    model3_spawn_point = np.random.choice(spawn_points)
    model3 = world.spawn_actor(model3_bp, model3_spawn_point)
    model3.set_autopilot(True)
    location = model3.get_location()
    print("current location is %s", location)
    model3.set_location(location)
    camera_bp = world.get_blueprint_library().find('sensor.camera.rgb')
    camera = world.spawn_actor(camera_bp,
                               carla.Transform(carla.Location(x=-5.5, z=2.5), carla.Rotation(pitch=8.0)),
                               model3,
                               carla.AttachmentType.SpringArm
                               )
    camera.listen(lambda image: image.save_to_disk('output/%06d.png' % image.frame))
    while 1==1:
        spectator = world.get_spectator()
        transform = model3.get_transform()
        spectator.set_transform(carla.Transform(transform.location + carla.Location(z=20),
        carla.Rotation(pitch=-60)))
        time.sleep(1)


if __name__ == '__main__':
    main()

