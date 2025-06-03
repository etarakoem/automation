from time import sleep
from ppadb.client import Client
import argparse
import time
import sys

def get_device():
    adb = Client(host="127.0.0.1", port=5037)
    devices = adb.devices()
    if not devices:
        print("No device attached")
        quit()
    return devices[0]

screen_width = 1080
screen_height = 2340

scale_w = screen_width / 1080
scale_h = screen_height / 2340

tap_point = screen_width // 8
screen_section = screen_width // 4

menu_row = [ screen_section*i - tap_point for i in range(1, 5) ]
top_menu = int(2050 * scale_h)
bot_menu = int(2150 * scale_h)


soul_y = int(1800 * scale_h)

soul_row_1 = int(screen_height / 8 * 2 * scale_h)
soul_row_2 = int(screen_height / 8 * 2.5 * scale_h)

retrain_y = int(screen_height / 8 * 0.85 * scale_h)

soul_col = [menu_row[0] + int(140 * scale_w) * i for i in range(7)]

battle_ok_x = screen_width//2
battle_ok_y =  screen_height//2 + int(300 * scale_h)
battle_ok_y = [screen_width//2, screen_height//2 + int(300 * scale_h)]

device = get_device()

def tap(x, y):
    device.shell(f'input tap {x} {y}')

def fight(skip=False):
    tap(menu_row[1], bot_menu)
    sleep(0.5)
    if skip:
        tap(screen_width // 2 , screen_height//2)
    else:
        tap(menu_row[1], soul_row_2)
    sleep(0.5)
    tap(menu_row[3], soul_y)
    sleep(0.5)
    # last step
    for i in range(10):
        tap(screen_width//2, screen_height//2 + int(i*50 * scale_h))

def find_range(pixel,end):
    for i in range(1,end):
        rows = pixel * i
        for j in menu_row:
            print(f"Tap at {j}, {rows}")
            tap(j, rows)
            sleep(1)

def retrain():
    # print("Retrain army")
    tap(menu_row[0], bot_menu)
    tap(menu_row[2], retrain_y)
    sleep(1)

def soul_collect(fight_flag, minutes, skip=False):
    sleep_time = 6 - 1.4
    tap(menu_row[2], bot_menu)
    if fight_flag:
        sleep_time -= 3
    start_time = time.time()
    while time.time() - start_time < (60 * minutes):
        if (time.time() - start_time) % 60 == 0:
            print(f"Collecting souls for {int((time.time() - start_time)/60)} minutes")
        if fight_flag:
            tap(menu_row[2], bot_menu)
        sleep(0.5)
        tap(menu_row[3], soul_y)
        sleep(0.5)

        for i in range(7):
            tap(soul_col[i], soul_row_1)
            sleep(0.1)
            tap(soul_col[i], soul_row_2)
            sleep(0.1)

        tap(menu_row[0], soul_y)
        if fight_flag:
            retrain()
            fight(skip)
        sleep(sleep_time)

# retrain()
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Soul collection automation script.")
    parser.add_argument('--fight', action='store_true', default=False, help='Enable fight mode after soul collection')
    parser.add_argument('--skip', action='store_true', default=False, help='Enable skip mode during fight')
    parser.add_argument('--minutes', type=int, default=10, help='Number of minutes to run the script (default: 10)')
    parser.add_argument('--poweroff', action='store_true', default=False, help='Press power button at the end (default: False)')
    args = parser.parse_args()
    try:
        soul_collect(args.fight, args.minutes, args.skip)
    except KeyboardInterrupt:
        print(f"\nSoul collection completed for {args.minutes} minutes (interrupted by user).")
        sys.exit(0)
    if args.poweroff:
        device.shell('input keyevent 26')  # Power button
        print(f"Soul collection completed for {args.minutes} minutes. Device will now turn off.")
    else:
        print(f"Soul collection completed for {args.minutes} minutes.")

