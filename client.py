import os.path
import socket
import threading
import sys
from PySide2.QtWidgets import QApplication, QTextEdit, QVBoxLayout, QHBoxLayout
from PySide2.QtWidgets import QWidget, QLineEdit
from PySide2.QtWidgets import QPushButton, QLabel
nicknames = []
from PIL import Image


def user():
    if(fieldEdit.text() != ""):
        nicknames.append(fieldEdit.text())
        app.exit()
        app.quit()

class ChatWindow(QWidget):
    def __init__(self, nick, host, port):
        super().__init__()
        self.name = nick
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))
        self.init_ui()
        self.setGeometry(100, 100, 600, 500)
        self.setWindowTitle("Communicator")

    def init_ui(self):
        # Widgets
        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        self.chat_input = QLineEdit()
        self.button = QPushButton("Send")
        self.label = QLabel("Type sendim to send image, senddoc to send file .docx")
        # Layout
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        vbox.addWidget(self.label)
        hbox.addWidget(self.chat_input)
        hbox.addWidget(self.button)
        vbox.addWidget(self.chat_history)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        # Events
        self.button.clicked.connect(self.send_message)
        self.chat_input.returnPressed.connect(self.button.click)
        self.chat_input.returnPressed.connect(self.chat_input.clear)

        # Start threads
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

    def send_message(self):
        message = self.chat_input.text()
        if message:
            if(message[0:6].lower() == "sendim"):
                image_path = message[7:]
                if(os.path.exists(image_path)):
                    img = Image.open(image_path)
                    width, height = img.size
                    aspect_ratio = height / width
                    new_width = 80
                    new_height = aspect_ratio * new_width * 0.55
                    img = img.resize((new_width, int(new_height)))
                    img = img.convert('L')
                    pixels = img.getdata()
                    chars = ["B", "S", "#", "&", "@", "$", "%", "*", "!", ":", "."]
                    new_pixels = [chars[pixel // 25] for pixel in pixels]
                    new_pixels = ''.join(new_pixels)
                    new_pixels_count = len(new_pixels)
                    ascii = [new_pixels[index:index + new_width] for index in
                                   range(0, new_pixels_count, new_width)]
                    ascii = "\n".join(ascii)
                    self.chat_history.append("You: " + ascii)
                    ascii = self.name + ": " + ascii
                    self.client_socket.send(ascii.encode())
                    self.chat_input.clear()
                else:
                    self.chat_input.clear()
            elif (message[0:7] == "senddoc"):
                file_path = message[8:]
                if(os.path.exists(file_path)):
                    self.client_socket.send("file".encode())
                    self.client_socket.send(file_path.encode())
                    filesize = os.path.getsize(file_path)
                    self.client_socket.send(str(filesize).encode())
                    with open(file_path, "rb") as f:
                        while True:
                            file_data = f.read(1024)
                            if not file_data:
                                break
                            self.client_socket.send(file_data)


            else:
                self.chat_history.append("You: " + message)
                message = "Message received from " + self.name + ": " + message
                self.client_socket.send(message.encode())
                self.chat_input.clear()

    def receive_messages(self):
        while True:
            message = self.client_socket.recv(4096).decode()
            self.chat_history.append(message)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QWidget()
    fieldEdit = QLineEdit(widget)
    fieldEdit.move(50, 20)
    fieldEdit.resize(200, 32)
    pybutton = QPushButton('Accept', widget)
    pybutton.resize(200, 32)
    pybutton.move(50, 80)
    pybutton.clicked.connect(user)
    widget.setGeometry(100, 100, 300, 150)
    widget.setWindowTitle("Type your username")
    widget.show()
    app.exec_()
    widget.hide()
    app1 = QApplication.instance()
    if(app1 is None):
        app1= QApplication(sys.argv)
    host = 'localhost'
    port = 5001
    window = ChatWindow(nicknames[0], host, port)
    window.show()
    sys.exit(app1.exec_())