import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QTextEdit, QMessageBox
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Simple Calculator')
        self.setStyleSheet("background-color: black;")

        vbox = QVBoxLayout()
        grid = QGridLayout()

        self.display = QTextEdit()
        self.display.setReadOnly(True)
        self.display.setFixedHeight(50)
        self.display.setStyleSheet("font-size: 24px; background-color: black; color: white;")
        vbox.addWidget(self.display)

    
        button_texts = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', 'C', '=', '+'
        ]

        row_val = 0
        col_val = 0

        for text in button_texts:
            button_color = 'orange' if text in '+-*/=' else 'white'
            button = QPushButton(text)
            button.setStyleSheet(f"font-size: 16px; background-color: gray; color: {button_color};")
            button.clicked.connect(lambda _, t=text: self.on_button_click(t))
            grid.addWidget(button, row_val, col_val)
            col_val += 1
            if col_val > 3:
                col_val = 0
                row_val += 1

        vbox.addLayout(grid)
        self.setLayout(vbox)

        
        self.setFocusPolicy(Qt.StrongFocus)

    def on_button_click(self, char):
        if char == '=':
            self.calculate()
        elif char == 'C':
            self.display.clear()
        else:
            current_text = self.display.toPlainText()
            self.display.setText(current_text + char)

    def keyPressEvent(self, event):
        key = event.text()
        if key in '0123456789+-*/':
            self.on_button_click(key)
        elif event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.calculate()
        elif key.lower() == 'c':
            self.on_button_click('C')

    def calculate(self):
        try:
            expression = self.display.toPlainText().strip()
            result = str(eval(expression))
            self.display.setText(result)
        except Exception as e:
            self.display.setText("Error")
            self.display.setStyleSheet("color: red;")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calculator_app = Calculator()
    calculator_app.resize(400, 400)
    calculator_app.show()
    sys.exit(app.exec_())
