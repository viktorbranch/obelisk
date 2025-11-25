import pyautogui
import sys
import time

if len(sys.argv) < 3:
    print('Usage: python automator.py <action> <params>')
    sys.exit(1)

action = sys.argv[1]
params = sys.argv[2:]

if action == 'click':
    x, y = int(params[0]), int(params[1])
    pyautogui.click(x, y)
    print(f'Clicked at ({x}, {y})')
elif action == 'write':
    text = ' '.join(params)
    pyautogui.write(text)
    print(f'Wrote: {text}')
elif action == 'move':
    x, y = int(params[0]), int(params[1])
    pyautogui.moveTo(x, y)
    print(f'Moved to ({x}, {y})')
elif action == 'screenshot':
    filename = params[0] if params else f'screenshot_{int(time.time())}.png'
    pyautogui.screenshot(filename)
    print(f'Screenshot saved as {filename}')
else:
    print('Unknown action')
    sys.exit(2)
