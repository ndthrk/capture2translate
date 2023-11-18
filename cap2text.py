import tkinter as tk
import numpy as np
import cv2
from threading import Thread
# from googletrans import Translator
import pytesseract
from PIL import ImageGrab, Image, ImageTk
import pyautogui
import openai

# build: py -m PyInstaller --onefile --icon=icon.ico --name=Cap2Trans --noconsole cap2text.py

path = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
pytesseract.pytesseract.tesseract_cmd = path
openai.api_key = "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"
start_position, end_position = None, None

# translator = Translator()
# def trans_google_API(text):
#     txt = ""
#     try:
#         txt = translator.translate(text, src='en', dest='vi').text
#     except:
#         pass
#     return txt

def on_key_start(event):
    global start_position, end_position
    start_mouse_listener()

def on_key_end(event):
    global start_position, end_position
    print("Stop")
    exit()

def set_start_position(event):
    global start_position
    start_position = pyautogui.position()
    label.config(text=f"{start_position}")
def set_end_position(event):
    global end_position
    end_position = pyautogui.position()
    
    solve()

def start_mouse_listener():
    # Bắt đầu lắng nghe sự kiện chuột trong một luồng riêng biệt
    mouse_thread = Thread(target=mouse_listener_thread)
    mouse_thread.start()

def mouse_listener_thread():
    global start_position, end_position
    root.bind("<z>", set_start_position)
    root.bind("<x>", set_end_position)


def trans_openAI(text):
    prompt = f'''Clean and Translate:
                    Given an English text possibly containing extraneous or meaningless characters, please thoroughly understand the semantics of the text ("/","l","|" may be translate with mean "I" fisrtly), clean it, and provide a coherent Vietnamese translation.
                    Input English Text: "{text}"
                    Cleaned and Translated Text to Vietnamese in 1 line'''
    response = openai.Completion.create(
        engine="text-davinci-003", 
        prompt=prompt,
        temperature=0.4, 
        max_tokens=800,
        n=1)
    translation = response.choices[0].text.strip()
    return translation

def detect_text(image):
    img = np.array(image)
    try:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    except:
        pass
    _, thresh = cv2.threshold(img, 90, 255, cv2.THRESH_BINARY)
    lang = 'eng' 
    config = r'--oem 1 --psm 12'
    # d = pytesseract.image_to_data(img,config=config, output_type=pytesseract.Output.DICT)
    text = pytesseract.image_to_string(thresh, lang = lang, config = config)
    return " ".join(text.split())

def solve():
    global start_position, end_position
    label.config(text="z,x: vị trí bắt đầu, kết thúc")
    try:
        pos = [start_position[0],end_position[0],start_position[1],end_position[1]]
        if len(np.unique(pos)) == 4:
            print(pos)
            img = ImageGrab.grab(bbox=(min(start_position[0], end_position[0]),
                                       min(start_position[1], end_position[1]),
                                       max(start_position[0], end_position[0]),
                                       max(start_position[1], end_position[1])))
            text = detect_text(img)
            t2 = trans_openAI(text)
            label1.config(text=text)
            label2.config(text=t2)

        start_position, end_position = None, None
    except:
        return
def on_close():
    # Hàm xử lý khi cửa sổ Tkinter đóng
    print("Tkinter window closed")
    root.destroy()


root = tk.Tk()

root.title("Vớ vẩn 7")
root.iconbitmap("D:\\ss\\myCap2Text\\icon.ico")
root.bind('<Control-s>', on_key_start)
root.bind('<Control-e>', on_key_end)

max_ratio = 0.8
max_width = int(max_ratio * root.winfo_screenwidth())
max_height = int(max_ratio * root.winfo_screenheight())

label = tk.Label(root, font=("Arial", 11), wraplength=int(max_width*0.9), fg="#FF0000",bg="#2b2c41")
label1 = tk.Label(root, text="Ctrl+S để bắt đầu", fg = "#edcc6f",bg="#2b2c41",
                    font=("Arial", 14), wraplength=int(max_width*0.9))
label2 = tk.Label(root, text="z,x: vị trí bắt đầu, kết thúc", fg = "#88cafc",bg="#2b2c41",
                font=("Arial", 14), wraplength=int(max_width*0.9))

label.pack()
label1.pack()
label2.pack()

root.configure(bg="#2b2c41") #Đen xanh đậm
root.maxsize(width=max_width, height=max_height)
root.geometry(f"+0+0")
root.attributes('-topmost', True)
root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()