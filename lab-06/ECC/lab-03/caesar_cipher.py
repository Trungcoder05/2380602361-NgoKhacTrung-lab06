import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.caesar import Ui_MainWindow
import requests

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.call_api_encrypt)
        self.ui.pushButton_2.clicked.connect(self.call_api_decrypt)

    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/caesar/encrypt"
        payload = {
            "plain_text": self.ui.textEdit.toPlainText(),
            "key": int(self.ui.textEdit_2.toPlainText())
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                encrypted = data.get("encrypted_message")
                if encrypted is not None:
                    self.ui.textEdit_3.setPlainText(encrypted)
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Encryption successful!")
                    msg.exec_()
                else:
                    print("Unexpected response format", data)
            else:
                print("Error while calling API", response.status_code)
        except requests.exceptions.RequestException as e:
            print("Error: %s" % e)

    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/caesar/decrypt"
        payload = {
            "cipher_text": self.ui.textEdit_3.toPlainText(),
            "key": int(self.ui.textEdit_2.toPlainText())
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                decrypted = data.get("decrypted_message")
                if decrypted is not None:
                    self.ui.textEdit.setPlainText(decrypted)
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Decryption successful!")
                    msg.exec_()
                else:
                    print("Unexpected response format", data)
            else:
                print("Error while calling API", response.status_code)
        except requests.exceptions.RequestException as e:
            print("Error: %s" % e)            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
