from m5stack import *
from m5ui import *
from uiflow import *
import imu
import time
import random

imu0 = imu.IMU()
image0 = M5Img(0, 31, "res/box.jpg", True)
image1 = M5Img(0, 190, "res/bag.jpg", True)
image2 = M5Img(-10, 69, "res/coin.jpg", True)
image3 = M5Img(-10, 108, "res/bomb.jpg", True)
image7 = M5Img(-10, 69, "res/coin.jpg", True)
image8 = M5Img(-10, 69, "res/coin.jpg", True)
image9 = M5Img(-10, 69, "res/coin.jpg", True)
image10 = M5Img(-10, 69, "res/coin.jpg", True)
image11 = M5Img(-10, 108, "res/bomb.jpg", True)

timing = 0
speed_box = 5
speed_coin = 17
box_x = 0
bag_x = 0
value_x = 0
coin_pos = []
bomb_pos = []
bag_y = 226
heart = 3
num = 0
Loop = 1
coin_num = 0
bomb_num = 0

def draw_screen():
    global timing, lcd, num, heart
    axp.setLcdBrightness(50)
    setScreenColor(0xffffff)
    lcd.line(0, 30, 135, 30, 0x000000)
    lcd.font(lcd.FONT_DefaultSmall)

    timing += random.randint(1, 3)
    lcd.print("SCORE:",1, 1, 0x000000,)
    lcd.print(num, 50, 1, 0x000000)
    lcd.print("YOUR LIFE:",1, 16, 0x000000,)
    lcd.print(heart, 72, 16, 0x000000)


def defeat():
    global num, Loop, heart
    while True:
        setScreenColor(0xffffff)
        lcd.font(lcd.FONT_Default)
        lcd.print('you lose', 20, 50, 0x000000)
        lcd.print('press A', 20, 100, 0x000000)
        lcd.print('to restart', 20, 150, 0x000000)

        wait_ms(100)
        btnA.wasPressed(buttonA_wasPressed)
        if Loop == 1:
            heart = 3
            num = 0
            coin_pos = []
            bomb_pos = []
            coin_num = 0
            bomb_num = 0
            bag_x = 0
            break
def buttonA_wasPressed():
    global Loop
    Loop = 1

def birthing():
    global bomb_y, bomb_x, timing, coin_y, coin_x, coin_num, bomb_num, bomb_pos, coin_pos, heart

    if timing % 21 == 1 and bomb_num <= 1:
        bomb_pos.append([box_x, 45, 1])
        bomb_num += 1
    if timing % 7 == 1 and coin_num <= 4:
        coin_pos.append([box_x, 45, 0])
        coin_num += 1


# 碰撞判定
def hit():
    global Loop, VICTORY, num, heart, bag_y, coin_num, bomb_num, bomb_pos, coin_pos
    for i in range(len(coin_pos)):
        coin_x = coin_pos[i][0]
        coin_y = coin_pos[i][1]
        if bag_x - 10 <= coin_x <= bag_x + 10 and bag_y - 5 <= coin_y <= bag_y + 10:
            num += 1
            del coin_pos[i]
            coin_num -= 1
            break
    for i in range(len(bomb_pos)):
        bomb_x = bomb_pos[i][0]
        bomb_y = bomb_pos[i][1]
        if bag_x - 10 <= bomb_x <= bag_x + 10 and bag_y - 5 <= bomb_y <= bag_y + 10:
            heart -= 1
            del bomb_pos[i]
            bomb_num -= 1
            if heart == 0:
                Loop = -Loop
                VICTORY = 2
            break


def coin_movement():
    global bomb_pos, coin_pos, coin_num, bomb_num, heart

    for i in range(0, len(coin_pos)):
        coin_pos[i][1] += speed_coin
        if coin_pos[i][1] >= 240:
            del coin_pos[i]
            coin_num -= 1
            break
    if len(coin_pos) == 5:
        image2.setPosition(coin_pos[0][0], coin_pos[0][1])
        image7.setPosition(coin_pos[1][0], coin_pos[1][1])
        image8.setPosition(coin_pos[2][0], coin_pos[2][1])
        image9.setPosition(coin_pos[3][0], coin_pos[3][1])
        image10.setPosition(coin_pos[4][0], coin_pos[4][1])
    if len(coin_pos) == 4:
        image2.setPosition(coin_pos[0][0], coin_pos[0][1])
        image7.setPosition(coin_pos[1][0], coin_pos[1][1])
        image8.setPosition(coin_pos[2][0], coin_pos[2][1])
        image9.setPosition(coin_pos[3][0], coin_pos[3][1])
    if len(coin_pos) == 3:
        image2.setPosition(coin_pos[0][0], coin_pos[0][1])
        image7.setPosition(coin_pos[1][0], coin_pos[1][1])
        image8.setPosition(coin_pos[2][0], coin_pos[2][1])
    if len(coin_pos) == 2:
        image2.setPosition(coin_pos[0][0], coin_pos[0][1])
        image7.setPosition(coin_pos[1][0], coin_pos[1][1])
    if len(coin_pos) == 1:
        image2.setPosition(coin_pos[0][0], coin_pos[0][1])
    for i in range(0, len(bomb_pos)):
        bomb_pos[i][1] += speed_coin
        if bomb_pos[i][1] >= 240:
            del bomb_pos[i]
            bomb_num -= 1
            break
        if len(bomb_pos) == 2:
            image3.setPosition(bomb_pos[0][0], bomb_pos[0][1])
            image11.setPosition(bomb_pos[1][0], bomb_pos[1][1])
        if len(bomb_pos) == 1:
            image3.setPosition(bomb_pos[0][0], bomb_pos[0][1])
    wait_ms(90)


def box_movement():
    global speed_box, box_x, value_x
    box_x = box_x + speed_box
    if box_x <= 0:
        speed_box = 3
    if box_x >= 121:
        speed_box = -3
    image0.setPosition(box_x, 31)


def bag_movement():
    global bag_x, value_x
    value_x = str((imu0.ypr[2]))
    value_x = float(value_x)

    if value_x <= -15:
        bag_x = 0
    if value_x >= 20:
        box_x = 130
    if -15 < value_x < 20:
        bag_x = int(4 * (float(value_x))) + 50

    image1.setPosition(bag_x, 228)


while True:

    draw_screen()
    birthing()
    bag_movement()
    box_movement()
    coin_movement()
    if Loop == -1:  # -1为失败
        defeat()
    hit()










