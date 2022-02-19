# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 22:28:13 2022

@author: shouk
"""
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QMessageBox

def on_button_clicked():
    alert = QMessageBox()
    alert.setText('You clicked the button!')
    alert.exec()

app = QApplication([])
app.setStyleSheet("QPushButton { margin: 10ex; padding: 10ex; }")
app.setStyle('Fusion')
window = QWidget()
layout = QVBoxLayout()
clickButton = QPushButton('Click')
layout.addWidget(QPushButton('Top'))
layout.addWidget(clickButton)
layout.addWidget(QPushButton('Bottom'))

clickButton.clicked.connect(on_button_clicked)
window.setLayout(layout)
window.show()
app.exec()