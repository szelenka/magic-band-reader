# Write your code here :-)
# SPDX-FileCopyrightText: 2022 Noe Ruiz, Scott Zelenka for Adafruit Industries
# SPDX-License-Identifier: MIT
# Magic Band Reader with Wiz Kit RFID
import random
import board
import time
import digitalio
import audiobusio
from audiocore import WaveFile
import neopixel
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.color import (
    RED,
    YELLOW,
    ORANGE,
    GREEN,
    BLUE,
    PURPLE,
    PINK,
    BLACK,
)

# Setup button switch
button = digitalio.DigitalInOut(board.A1)
button.switch_to_input(pull=digitalio.Pull.DOWN)

# LRC is word_select, BCLK is bit_clock, DIN is data_pin.
# Feather RP2040
audio = audiobusio.I2SOut(bit_clock=board.D24, word_select=board.D25, data=board.A3)

# Make the neopixel object
pixels = neopixel.NeoPixel(board.D6, 24, brightness=.4)

# Setup the LED animations
solid = Solid(pixels, color=BLACK)

#Fuction for playing audio
def play_wav(name):
    print("playing", name)
    wave_file = open('sounds/' + name + '.wav', 'rb')
    wave = WaveFile(wave_file)
    audio.play(wave)

# sound-color-map
sound_color_map = {
    'chime': Chase(pixels, speed=0.02, color=YELLOW, size=4, spacing=24),
    'startours': Chase(pixels, speed=0.02, color=PINK, size=4, spacing=24),
    'mandalorian': Chase(pixels, speed=0.02, color=GREEN, size=4, spacing=24),
    'bb8': Chase(pixels, speed=0.02, color=ORANGE, size=4, spacing=24),
    'r2d2': Chase(pixels, speed=0.02, color=BLUE, size=4, spacing=24),
    'lightsaber': Chase(pixels, speed=0.02, color=PURPLE, size=4, spacing=24),
    'vader': Chase(pixels, speed=0.02, color=RED, size=4, spacing=24),
}

while True:
    print("Waiting for button press to continue!")
    # repeat displaying BLACK
    while not button.value:
        solid.animate()

    # select random sound/animation and play to completion
    sound = random.choice(list(sound_color_map.keys()))
    play_wav(sound)
    # wait for the board to release the button to prevent continous trigger
    while audio.playing or button.value:
        sound_color_map[sound].animate()
