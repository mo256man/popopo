import time
import board
import neopixel
import random

from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.rainbowchase import RainbowChase
from adafruit_led_animation.animation.rainbowcomet import RainbowComet
from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
from adafruit_led_animation.animation.sparklepulse import SparklePulse
from adafruit_led_animation.animation.colorcycle import ColorCycle
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.animation.comet import Comet

class Music():
    def __init__(self):
        self.ini_time = 0
        self.bpm = 130
        self.score = [
            {"beat":4, "lyric":"ポポーポポポポ", "effect":"rainbowchase", "reverse":False},
            {"beat":4, "lyric":"ポポーポポポポ", "effect":"rainbowchase", "reverse":True},
            {"beat":4, "lyric":"ポポポポポー", "effect":"rainbowcomet", "reverse":False},
            {"beat":4, "lyric":"ポポーポポー", "effect":"rainbowcomet", "reverse":True},
            {"beat":4, "lyric":"ポポポポポー", "effect":"rainbowchase", "reverse":False},
            {"beat":4, "lyric":"ポポポポポー", "effect":"rainbowchase", "reverse":True},
            {"beat":4, "lyric":"ポポポポ ポ・ポ", "effect":"rainbowchase", "reverse":True},
            {"beat":1, "lyric":"ポ！", "effect":"sparklepulse", "reverse":None},
            {"beat":1, "lyric":"ポ！", "effect":"sparklepulse", "reverse":None},
            {"beat":1, "lyric":"ポ！", "effect":"sparklepulse", "reverse":None},
            {"beat":1, "lyric":"ポ！", "effect":"sparklepulse", "reverse":None},
            {"beat":4, "lyric":"ポポーポポポポ", "effect":"rainbowcomet", "reverse":True},
            {"beat":4, "lyric":"ポポーポポポポ", "effect":"rainbowchase", "reverse":True},
            {"beat":4, "lyric":"ポーーーー", "effect":"rainbowcomet", "reverse":True},
            {"beat":4, "lyric":"", "effect":"rainbowcomet", "reverse":True},
            ]

class Player():
    def __init__(self, name, pin, delay, music):
        self.name = name
        self.pin = pin
        self.led = neopixel.NeoPixel(self.pin, NUM_LEDS, brightness=0.05)
        self.score = []
        self.playing = 0    # 0:not yet, 1:playing, 2:finished
        self.cnt = 0
        elapsed_time = music.ini_time + delay * 60 / music.bpm
        for dict in music.score:
            mydict = dict.copy()
            mydict["time"] = elapsed_time
            elapsed_time += mydict["beat"] * 60 / music.bpm
            self.score.append(mydict)

    def play(self, t):
        if self.playing != 2:		# not finished
            if t > self.score[self.cnt]["time"]:
                if self.cnt == 0:
                    self.playing = 1
                    print(f"{self.pin} is ON")
                score = self.score[self.cnt]
                print(f"{self.name}:{t:.4f}:{score['lyric']}")
                self.effect = eval(score["effect"])(self.led, score)
                self.cnt += 1
                if self.cnt >= len(self.score):
                    self.playing = 2
                    print(f"{self.name} end")
                    self.led.fill(0)
                    self.led.show()
            if self.playing == 1:
                self.effect.animate()
            time.sleep(0.001)

def rainbowchase(led, score):
    reverse = score["reverse"]
    return RainbowChase(led, speed=0.1, reverse=reverse)

def rainbowcomet(led, score):
    reverse = score["reverse"]
    return RainbowComet(led, speed=0.1, tail_length=NUM_LEDS, ring=True, reverse=reverse)

def sparklepulse(led, score):
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    return SparklePulse(led, speed=0.1, color=color)

def clear_all():
    for player in [player1, player2, player3]:
        player.led.fill(0)
        player.led.show()

def main():
    start_time = time.time()
    print("start")
    while True:
        t = time.time() - start_time
        player1.play(t)
        player2.play(t)
        player3.play(t)
        
        if player3.playing == 2:
            break
    print("all end")


NUM_LEDS = 12
music = Music()
player1 = Player(name="Fr", pin=board.D4, delay=0, music=music)
player2 = Player(name="RH", pin=board.D5, delay=4, music=music)
player3 = Player(name="LH", pin=board.D6, delay=8, music=music)

if __name__ == "__main__":
    clear_all()
    try:
        main()
    except KeyboardInterrupt:
        print("quitted")
    finally:
        clear_all()
