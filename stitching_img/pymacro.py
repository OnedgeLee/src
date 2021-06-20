#%%
import pyautogui, pyperclip

Y = 550 # 507
X = 800 # 740
pyperclip.copy("직")
pyautogui.moveTo(x=X, y=Y, duration=0.001)
pyautogui.click(clicks=1)
pyautogui.hotkey("ctrl", "v")

pyperclip.copy("업")
pyautogui.moveTo(x=X, y=Y, duration=1)
pyautogui.click(clicks=1)
pyautogui.hotkey("ctrl", "v")

pyperclip.copy("상")
pyautogui.moveTo(x=X, y=Y, duration=1)
pyautogui.click(clicks=1)
pyautogui.hotkey("ctrl", "v")

pyperclip.copy("담")
pyautogui.moveTo(x=X, y=Y, duration=1)
pyautogui.click(clicks=1)
pyautogui.hotkey("ctrl", "v")

pyperclip.copy("사")
pyautogui.moveTo(x=X, y=Y, duration=1)
pyautogui.click(clicks=1)
pyautogui.hotkey("ctrl", "v")

print(pyautogui.position())
 
print(pyautogui.size())
 
print(pyautogui.onScreen(1000,2000))
 
print(pyautogui.onScreen(1000,1000))

# x 740 / y 507

#%%
# OCR
import pytesseract, pyautogui
from PIL import ImageGrab
from textblob import TextBlob
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract'

screen = ImageGrab.grab(bbox=(600, 300, 1200, 800))
w = screen.convert('L')
w.save('/Users/shetshield/Desktop/python_ws/grabbed.png')

text = pytesseract.image_to_string(w)
arr = text.split('\n')[0:-1]
res = '\n'.join(arr)
# correctedText = TextBlob(text).correct().string
# print(correctedText)
print(res)
