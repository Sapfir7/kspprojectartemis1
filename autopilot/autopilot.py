import math
import time
import krpc

turn_start_altitude = 250
turn_end_altitude = 45000
target_altitude = 100000

conn = krpc.connect(name="Launch into orbit")
canvas = conn.ui.stock_canvas
vessel = conn.space_center.active_vessel
srf_frame = vessel.orbit.body.reference_frame
screen_size = canvas.rect_transform.size
panel = canvas.add_panel()
rect = panel.rect_transform
rect.size = (200, 80)
rect.position = (110 - (screen_size[0] / 2), 400)

text = panel.add_text("Dynamic Pr.: 0 kN")
text.rect_transform.position = (0, 20)
text.color = (1, 1, 1)
text.size = 18
text2 = panel.add_text("Speed: 0 m/s")
text2.rect_transform.position = (0, 0)
text2.color = (1, 1, 1)
text2.size = 18
text3 = panel.add_text("Altitude:")
text3.rect_transform.position = (0, -20)
text3.color = (1, 1, 1)
text3.size = 18

ut = conn.add_stream(getattr, conn.space_center, "ut")
altitude = conn.add_stream(getattr, vessel.flight(), "mean_altitude")
apoapsis = conn.add_stream(getattr, vessel.orbit, "apoapsis_altitude")
srf_speed = conn.add_stream(getattr, vessel.flight(srf_frame), "speed")
dynamic_pressure = conn.add_stream(
    getattr, vessel.flight(srf_frame), "dynamic_pressure"
)
stage_2_resources = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
srb_fuel = conn.add_stream(stage_2_resources.amount, "LiquidFuel")

vessel.control.sas = False
vessel.control.rcs = False
vessel.control.throttle = 0.5

print("3...")
time.sleep(1)
print("2...")
time.sleep(1)
print("1...")
time.sleep(1)
print("Launch!")

vessel.control.pitch = -0.2
vessel.control.activate_next_stage()
vessel.auto_pilot.target_pitch_and_heading(90, 90)
vessel.auto_pilot.engage()

srbs_separated = False
turn_angle = 0
c = True

num_time = time.time()
timer = dict()

while True:
    if dynamic_pressure() / 4000 > 1:
        x = 0.5 - (dynamic_pressure() / 4000) / 5
        vessel.control.throttle = x
    elif dynamic_pressure() / 4000 < 0.8:
        vessel.control.throttle = 1
    else:
        x = float((1 - dynamic_pressure() / 4000) + 0.8)
        vessel.control.throttle = x

    text.content = "Dynamic Pr.: %d psi" % (dynamic_pressure())
    text2.content = "Speed: %d m/s" % (srf_speed())
    text3.content = "Altitude: %d m" % (vessel.flight(srf_frame).surface_altitude)

    if altitude() > turn_start_altitude and altitude() < turn_end_altitude:
        frac = (altitude() - turn_start_altitude) / (
            turn_end_altitude - turn_start_altitude
        )
        new_turn_angle = frac * 90

        if abs(new_turn_angle - turn_angle) > 0.5:
            turn_angle = new_turn_angle
            vessel.auto_pilot.target_pitch_and_heading(90 - turn_angle, 90)
    if not srbs_separated:
        if (
            vessel.resources_in_decouple_stage(
                vessel.control.current_stage - 1, cumulative=False
            ).amount("SolidFuel")
            < 0.1
        ):
            vessel.control.activate_next_stage()
            srbs_separated = True
            time.sleep(0.1)
            print("separated")

    if apoapsis() > target_altitude * 0.9:
        print("Approaching target apoapsis")
        break
    timer[int(time.time() - num_time)] = f'{srf_speed()} - {dynamic_pressure()} - {vessel.flight(srf_frame).surface_altitude} - {turn_angle} - {vessel.mass} - {vessel.available_thrust} - {vessel.specific_impulse}'

def write_dict_to_file(dictionary, filename):
    with open(filename, 'w') as file:
        for key, value in dictionary.items():
            file.write(f'{key}: {value}\n')


vessel.control.throttle = 0.25


timer[int(time.time() - num_time)] = f'{srf_speed()} - {dynamic_pressure()} - {vessel.flight(srf_frame).surface_altitude} - {turn_angle} - {vessel.mass} - {vessel.available_thrust} - {vessel.specific_impulse}'
while apoapsis() < target_altitude:
    text.content = "Dynamic Pressure: %d psi" % (vessel.thrust / 1000)
    text2.content = "Speed: %d m/s" % (vessel.flight(srf_frame).speed)
    text3.content = "Altitude: %d m" % (vessel.flight(srf_frame).surface_altitude)
    time.sleep(0.1)
    if c and altitude() == 60000:
        c = False
        vessel.control.activate_next_stage()

    timer[int(time.time() - num_time)] = f'{srf_speed()} - {dynamic_pressure()} - {vessel.flight(srf_frame).surface_altitude} - {turn_angle} - {vessel.mass} - {vessel.available_thrust} - {vessel.specific_impulse}'
print("Target apoapsis reached")
vessel.control.throttle = 0.0

print("Coasting out of atmosphere")
while altitude() < 99500:
    timer[int(time.time() - num_time)] = f'{srf_speed()} - {dynamic_pressure()} - {vessel.flight(srf_frame).surface_altitude} - {turn_angle} - {vessel.mass} - {vessel.available_thrust} - {vessel.specific_impulse}'
    if c and altitude() == 60000:
        c = False
        vessel.control.activate_next_stage()
    text.content = "Dynamic Pressure: %d psi" % (vessel.thrust / 1000)
    text2.content = "Speed: %d m/s" % (vessel.flight(srf_frame).speed)
    text3.content = "Altitude: %d m" % (vessel.flight(srf_frame).surface_altitude)
    time.sleep(0.1)
vessel.control.throttle = 1.0
orbit = vessel.orbit
while apoapsis() < 130000:
    continue
vessel.control.throttle = 0.0
hehehe = 1






timer[int(time.time() - num_time) - 1] = '--------------------------The orbit has been reached--------------------------'
timer[int(time.time() - num_time)] = f'{srf_speed()} - {dynamic_pressure()} - {vessel.flight(srf_frame).surface_altitude} - {turn_angle} - {vessel.mass} - {vessel.available_thrust} - {vessel.specific_impulse}'
while True:
    text.content = "Dynamic Pressure: %d psi" % (vessel.thrust / 1000)
    text2.content = "Speed: %d m/s" % (vessel.flight(srf_frame).speed)
    text3.content = "Altitude: %d m" % (vessel.flight(srf_frame).surface_altitude)
    timer[int(time.time() - num_time)] = f'{srf_speed()} - {dynamic_pressure()} - {vessel.flight(srf_frame).surface_altitude} - {turn_angle} - {vessel.mass} - {vessel.available_thrust} - {vessel.specific_impulse}'
    time.sleep(0.5)
    if int(time.time() - num_time) > 120 and hehehe:
        write_dict_to_file(timer, 'dictionary.txt')
        break
