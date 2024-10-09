# test-a-cpb.py
import board, time, neopixel, digitalio, touchio,  busio, adafruit_lis3dh, pwmio
from adafruit_led_animation.color import RED, YELLOW, ORANGE, GREEN, TEAL, CYAN, BLUE, \
    PURPLE, MAGENTA, GOLD, PINK, AQUA, JADE, AMBER, OLD_LACE, WHITE, BLACK

print("RUNNING TESTS!")

# Audio setup for CircuitPlayground boards - can skip if only using external speaker
speaker = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
speaker.direction = digitalio.Direction.OUTPUT
speaker.value = True

# Set up board for tone audio play
tone = pwmio.PWMOut(board.AUDIO, variable_frequency = True)
volume = 10000
tone.duty_cycle = volume # about 32760 is full volume

# Play Tones to test speaker
for f in (262, 294, 330, 349, 392, 440, 494, 523):
        tone.frequency = f
        print(f"Tone: {f}")
        time.sleep(0.1)
tone.duty_cycle = 0

pixel = neopixel.NeoPixel(board.NEOPIXEL, 10)
colors = [RED, YELLOW, ORANGE, GREEN, TEAL, CYAN, BLUE, PURPLE, MAGENTA, GOLD, PINK, AQUA,
          JADE, AMBER, OLD_LACE, WHITE, BLACK]

for i in range(len(pixel)):
    pixel[i] = colors[i]
    time.sleep(0.2)

for color in colors:
    pixel.fill(color)
    time.sleep(0.2)

pixel.fill(BLACK)

# setup accelerometer for CircuitPlayground Bluefruit/Express
i2c = busio.I2C(board.ACCELEROMETER_SCL, board.ACCELEROMETER_SDA)
accelerometer = adafruit_lis3dh.LIS3DH_I2C(i2c, address=0x19)

# set range
accelerometer.range = adafruit_lis3dh.RANGE_2_G

# Setup buttons
button_A = digitalio.DigitalInOut(board.BUTTON_A)
button_A.switch_to_input(digitalio.Pull.DOWN)

button_B = digitalio.DigitalInOut(board.BUTTON_B)
button_B.switch_to_input(digitalio.Pull.DOWN)

# setup touchpads
pads = [board.A1, board.A2, board.A3, board.A4, board.A5, board.A6, board.TX]

# create an empty list of touchpads
touchpads = []
for pad in pads:
    # and add (append) a new element to touchpads for pad[i]
    touchpads.append(touchio.TouchIn(pad))
    # now you can test each touchpad's .value property like this:
    # touchpad[i].value

while True:
    x, y, z = accelerometer.acceleration
    # print((x, y, z)) # for plotting in Mu
    print(f"x:{x:6.2f}, y:{y:6.2f}, z:{z:6.2f}")

    if button_A.value:
        print("Button A Pressed!")
        pixel.fill(PURPLE)
    elif button_B.value:
        pixel.fill(TEAL)
    else:
        pixel.fill(BLACK)

    for i in range(len((touchpads))):
        if touchpads[i].value:
            pixel.fill(colors[i])
            time.sleep(0.2)
            pixel.fill(BLACK)

    time.sleep(0.1)