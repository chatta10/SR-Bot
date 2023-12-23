import pyautogui
import time

try:
    while True:
        # Get the current mouse coordinates
        x, y = pyautogui.position()

        # Print the coordinates
        print(f"Mouse coordinates are: X={x}, Y={y}")

        # Update every second
        time.sleep(1)

except KeyboardInterrupt:
    print("\nExecution interrupted.")

