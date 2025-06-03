from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QTableWidget, QTableWidgetItem, QPushButton,
                               QComboBox, QLabel, QLineEdit, QMessageBox,
                               QFileDialog, QHeaderView, QDialog)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from controllers.customer_controller import CustomerController
from views.customer_form import CustomerForm


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.controller = CustomerController()
        self.current_page = 1
        self.rows_per_page = 10
        self.total_records = 0
        self.search_term = ""
        self.init_ui()
        self.load_data()

    def init_ui(self):
        self.setWindowTitle("Customer Management System")
        self.setGeometry(100, 100, 1000, 700)

        # Apply modern styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QTableWidget {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 5px;
                gridline-color: #e0e0e0;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #e0e0e0;
                color: #000;
            }
            QTableWidget::item:selected {
                background-color: #e3f2fd;
            }
            QHeaderView::section {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 15px;
                border-radius: 5px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
            QLineEdit {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 5px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border-color: #4CAF50;
            }
            QComboBox {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 5px;
                font-size: 12px;
                min-width: 80px;
            }
            QLabel {
                font-size: 12px;
                color: #333;
            }
            QMessageBox {
                background-color: #f5f5f5;
                color: #4CAF50;
                font-weight: bold;
            }
            QMessageBox QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 60px;
            }
            QMessageBox QPushButton:hover {
                background-color: #45a049;
            }

        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        # Search and controls
        controls_layout = QHBoxLayout()

        # Search
        search_label = QLabel("Pencarian:")
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Cari berdasarkan NIK, Nama, Tanggal Lahir, Status, atau Gaji...")
        self.search_edit.textChanged.connect(self.on_search_changed)

        controls_layout.addWidget(search_label)
        controls_layout.addWidget(self.search_edit)
        controls_layout.addStretch()

        # Rows per page
        rows_label = QLabel("Baris per halaman:")
        self.rows_combo = QComboBox()
        self.rows_combo.addItems(["1", "5", "10", "25", "50", "100"])
        self.rows_combo.setCurrentText("10")
        self.rows_combo.currentTextChanged.connect(self.on_rows_per_page_changed)

        controls_layout.addWidget(rows_label)
        controls_layout.addWidget(self.rows_combo)

        layout.addLayout(controls_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "NIK", "Nama", "Tanggal Lahir", "Status", "Gaji"])

        # Set column widths
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)

        self.table.cellDoubleClicked.connect(self.on_row_double_clicked)

        layout.addWidget(self.table)

        # Pagination and action buttons
        bottom_layout = QHBoxLayout()

        # Pagination info
        self.info_label = QLabel()
        bottom_layout.addWidget(self.info_label)

        bottom_layout.addStretch()

        # Pagination buttons
        self.prev_btn = QPushButton("← Sebelumnya")
        self.prev_btn.clicked.connect(self.prev_page)

        self.next_btn = QPushButton("Selanjutnya →")
        self.next_btn.clicked.connect(self.next_page)

        bottom_layout.addWidget(self.prev_btn)
        bottom_layout.addWidget(self.next_btn)

        # Action buttons
        self.add_btn = QPushButton("Tambah Data")
        self.add_btn.clicked.connect(self.add_customer)

        self.upload_btn = QPushButton("Upload CSV")
        self.upload_btn.clicked.connect(self.upload_csv)

        self.download_btn = QPushButton("Download CSV")
        self.download_btn.clicked.connect(self.download_csv)

        bottom_layout.addWidget(self.add_btn)
        bottom_layout.addWidget(self.upload_btn)
        bottom_layout.addWidget(self.download_btn)

        layout.addLayout(bottom_layout)
        central_widget.setLayout(layout)

        # Search timer
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.perform_search)

    def load_data(self):
        offset = (self.current_page - 1) * self.rows_per_page
        customers, total = self.controller.get_customers(
            limit=self.rows_per_page,
            offset=offset,
            search_term=self.search_term
        )

        self.total_records = total
        self.table.setRowCount(len(customers))

        for row, customer in enumerate(customers):
            self.table.setItem(row, 0, QTableWidgetItem(str(customer['idx'])))
            self.table.setItem(row, 1, QTableWidgetItem(customer['nik']))
            self.table.setItem(row, 2, QTableWidgetItem(customer['name']))
            self.table.setItem(row, 3, QTableWidgetItem(str(customer['born']) if customer['born'] else ""))
            self.table.setItem(row, 4, QTableWidgetItem("Aktif" if customer['active'] else "Tidak Aktif"))
            self.table.setItem(row, 5, QTableWidgetItem(f"Rp {customer['salary']:,}" if customer['salary'] else "Rp 0"))

        self.update_pagination_info()

    def update_pagination_info(self):
        total_pages = (self.total_records + self.rows_per_page - 1) // self.rows_per_page
        if total_pages == 0:
            total_pages = 1

        start_record = (self.current_page - 1) * self.rows_per_page + 1
        end_record = min(self.current_page * self.rows_per_page, self.total_records)

        self.info_label.setText(
            f"Halaman {self.current_page} dari {total_pages} | "
            f"Menampilkan {start_record}-{end_record} dari {self.total_records} record"
        )

        self.prev_btn.setEnabled(self.current_page > 1)
        self.next_btn.setEnabled(self.current_page < total_pages)

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.load_data()

    def next_page(self):
        total_pages = (self.total_records + self.rows_per_page - 1) // self.rows_per_page
        if self.current_page < total_pages:
            self.current_page += 1
            self.load_data()

    def on_rows_per_page_changed(self, value):
        self.rows_per_page = int(value)
        self.current_page = 1
        self.load_data()

    def on_search_changed(self):
        self.search_timer.stop()
        self.search_timer.start(500)  # Delay 500ms

    def perform_search(self):
        self.search_term = self.search_edit.text().strip()
        self.current_page = 1
        self.load_data()

    def on_row_double_clicked(self, row, column):
        customer_id = int(self.table.item(row, 0).text())
        self.edit_customer(customer_id)

    def add_customer(self):
        dialog = CustomerForm(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_data()

    def edit_customer(self, customer_id):
        dialog = CustomerForm(self, customer_id)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_data()

    def upload_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Pilih File CSV", "", "CSV Files (*.csv)"
        )

        if file_path:
            reply = QMessageBox.question(
                self, "Konfirmasi Upload",
                "Apakah Anda yakin ingin mengupload file CSV ini?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                success, message = self.controller.import_from_csv(file_path)
                if success:
                    QMessageBox.information(self, "Sukses", message)
                    self.load_data()
                else:
                    QMessageBox.warning(self, "Error", message)

    def download_csv(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Simpan File CSV", "customers.csv", "CSV Files (*.csv)"
        )

        if file_path:
            reply = QMessageBox.question(
                self, "Konfirmasi Download",
                "Apakah Anda yakin ingin mendownload data ke file CSV?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                success, message = self.controller.export_to_csv(file_path)
                if success:
                    QMessageBox.information(self, "Sukses", message)
                else:
                    QMessageBox.warning(self, "Error", message)
