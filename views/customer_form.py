from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
                               QLineEdit, QDateEdit, QComboBox, QSpinBox,
                               QPushButton, QMessageBox)
from PySide6.QtCore import QDate, Qt
from PySide6.QtGui import QFont
from controllers.customer_controller import CustomerController

class CustomerForm(QDialog):
    def __init__(self, parent=None, customer_id=None):
        super().__init__(parent)
        self.customer_id = customer_id
        self.controller = CustomerController()
        self.init_ui()
        
        if customer_id:
            self.load_customer_data()
    
    def init_ui(self):
        self.setWindowTitle("Form Customer")
        self.setFixedSize(400, 300)
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
            }
            QLineEdit, QDateEdit, QComboBox, QSpinBox {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 5px;
                font-size: 12px;
            }
            QLineEdit:focus, QDateEdit:focus, QComboBox:focus, QSpinBox:focus {
                border-color: #4CAF50;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QPushButton#deleteBtn {
                background-color: #f44336;
            }
            QPushButton#deleteBtn:hover {
                background-color: #da190b;
            }
        """)
        
        layout = QVBoxLayout()
        
        # Form layout
        form_layout = QFormLayout()
        
        self.nik_edit = QLineEdit()
        self.nik_edit.setMaxLength(6)
        form_layout.addRow("NIK:", self.nik_edit)
        
        self.name_edit = QLineEdit()
        self.name_edit.setMaxLength(50)
        form_layout.addRow("Nama:", self.name_edit)
        
        self.born_edit = QDateEdit()
        self.born_edit.setDate(QDate.currentDate())
        self.born_edit.setCalendarPopup(True)
        form_layout.addRow("Tanggal Lahir:", self.born_edit)
        
        self.active_combo = QComboBox()
        self.active_combo.addItems(["Tidak Aktif", "Aktif"])
        form_layout.addRow("Status:", self.active_combo)
        
        self.salary_spin = QSpinBox()
        self.salary_spin.setRange(0, 999999999)
        self.salary_spin.setSuffix(" IDR")
        form_layout.addRow("Gaji:", self.salary_spin)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.save_btn = QPushButton("Simpan")
        self.save_btn.clicked.connect(self.save_customer)
        
        self.cancel_btn = QPushButton("Batal")
        self.cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.cancel_btn)
        
        if self.customer_id:
            self.delete_btn = QPushButton("Hapus")
            self.delete_btn.setObjectName("deleteBtn")
            self.delete_btn.clicked.connect(self.delete_customer)
            button_layout.addWidget(self.delete_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def load_customer_data(self):
        customer = self.controller.get_customer(self.customer_id)
        if customer:
            self.nik_edit.setText(customer['nik'])
            self.name_edit.setText(customer['name'])
            if customer['born']:
                self.born_edit.setDate(QDate.fromString(str(customer['born']), "yyyy-MM-dd"))
            self.active_combo.setCurrentIndex(customer['active'])
            self.salary_spin.setValue(customer['salary'] or 0)
    
    def save_customer(self):
        nik = self.nik_edit.text().strip()
        name = self.name_edit.text().strip()
        born = self.born_edit.date().toString("yyyy-MM-dd")
        active = self.active_combo.currentIndex()
        salary = self.salary_spin.value()
        
        if self.customer_id:
            success, message = self.controller.update_customer(
                self.customer_id, nik, name, born, active, salary
            )
        else:
            success, message = self.controller.create_customer(
                nik, name, born, active, salary
            )
        
        if success:
            QMessageBox.information(self, "Sukses", message)
            self.accept()
        else:
            QMessageBox.warning(self, "Error", message)
    
    def delete_customer(self):
        reply = QMessageBox.question(
            self, "Konfirmasi", 
            "Apakah Anda yakin ingin menghapus data ini?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            success, message = self.controller.delete_customer(self.customer_id)
            if success:
                QMessageBox.information(self, "Sukses", message)
                self.accept()
            else:
                QMessageBox.warning(self, "Error", message)