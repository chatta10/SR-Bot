import time
import pyautogui
import pygetwindow as gw
import math
from mss import mss
from PIL import Image

def press_key_a():
    pyautogui.press('A')
    time.sleep(0.5)  # Add a small delay between key presses

def press_key_sequence(sequence):
    for key in sequence:
        pyautogui.press(key)
        time.sleep(1.5)  # Add a delay between keys to avoid pressing them too quickly

def detect_color_similarity(pixel, target_color, threshold):
    # Calculate the Euclidean difference between the detected color and the target color
    difference = math.sqrt(sum((c1 - c2) ** 2 for c1, c2 in zip(pixel, target_color)))

    # Check if the difference is below the specified threshold
    return difference <= threshold

def execute_command():
    # Execute the "Reset" command
    pyautogui.hotkey('command', 'e')

def main():
    windows = gw.getAllTitles()
    target_window = '[ App 0/2478685 pid=3808 ] Pokemon - Versione Rosso Fuoco (Italy) - VisualBoyAdvance-M 2.1.7'

    if target_window in windows:

        x_pixel_blue = 1252  # Replace with the x coordinates of the blue pixel
        y_pixel_blue = 261   # Replace with the y coordinates of the blue pixel

        x_pixel_check = 1059  # Replace with the x coordinates of the pixel to check
        y_pixel_check = 190   # Replace with the y coordinates of the pixel to check

        desired_blue_color = (120, 168, 192)  # Desired blue color (RGB)
        desired_check_color = (128, 163, 56)     # Desired check color (RGB)

        similarity_threshold = 50  # Replace with the desired threshold

        active_key_sequence = False  # Control variable for the key sequence

        with mss() as sct:
            blue_region = {"left": x_pixel_blue, "top": y_pixel_blue, "width": 1, "height": 1}

            while True:
                press_key_a()  # Press the 'A' key

                img = sct.grab(blue_region)
                blue_pixel = img.pixel(0, 0)

                # Debug print
                print(f"Detected color: {blue_pixel}")

                # Check if the pixel is similar to the desired blue color
                if detect_color_similarity(blue_pixel, desired_blue_color, similarity_threshold):
                    active_key_sequence = True
                    print("Blue color detected. Activating key sequence.")
                else:
                    print("Blue color not detected. Deactivating key sequence.")

                if active_key_sequence:
                    # Execute the key sequence
                    key_sequence = ['D', 'A', 'A', 'A', 'D', 'A', 'A', 'A']
                    press_key_sequence(key_sequence)

                    # Perform additional color check
                    img_check = sct.grab({"left": x_pixel_check, "top": y_pixel_check, "width": 1, "height": 1})
                    check_pixel = img_check.pixel(0, 0)

                    # Debug print
                    print(f"Check color detected: {check_pixel}")

                    if detect_color_similarity(check_pixel, desired_check_color, similarity_threshold):
                        print("Similar color detected. Script stops.")
                        return
                    else:
                        print("Non-similar color detected. Executing 'Command + E' command.")
                        execute_command()
                        time.sleep(2)  # Wait for 2 seconds
                        print("Restarting the script.")
                        active_key_sequence = False
    else:
        print(windows)

if __name__ == "__main__":
    main()
