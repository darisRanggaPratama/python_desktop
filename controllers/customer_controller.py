import csv
from datetime import datetime
from models.customer import Customer
from PySide6.QtWidgets import QMessageBox, QFileDialog

class CustomerController:
    def __init__(self):
        self.customer_model = Customer()
    
    def get_customers(self, limit=10, offset=0, search_term=""):
        return self.customer_model.get_all_customers(limit, offset, search_term)
    
    def get_customer(self, customer_id):
        return self.customer_model.get_customer_by_id(customer_id)
    
    def create_customer(self, nik, name, born, active, salary):
        try:
            # Validate data
            if not nik or not name:
                return False, "NIK dan Nama harus diisi"
            
            # Convert born to date format
            if isinstance(born, str):
                born = datetime.strptime(born, "%Y-%m-%d").date()
            
            success = self.customer_model.create_customer(nik, name, born, active, salary)
            if success:
                return True, "Data berhasil disimpan"
            else:
                return False, "Gagal menyimpan data"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def update_customer(self, customer_id, nik, name, born, active, salary):
        try:
            if not nik or not name:
                return False, "NIK dan Nama harus diisi"
            
            if isinstance(born, str):
                born = datetime.strptime(born, "%Y-%m-%d").date()
            
            success = self.customer_model.update_customer(customer_id, nik, name, born, active, salary)
            if success:
                return True, "Data berhasil diupdate"
            else:
                return False, "Gagal mengupdate data"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def delete_customer(self, customer_id):
        try:
            success = self.customer_model.delete_customer(customer_id)
            if success:
                return True, "Data berhasil dihapus"
            else:
                return False, "Gagal menghapus data"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def export_to_csv(self, file_path):
        try:
            customers, _ = self.customer_model.get_all_customers(limit=999999)
            
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                
                # Write header
                writer.writerow(['idx', 'nik', 'name', 'born', 'active', 'salary'])
                
                # Write data
                for customer in customers:
                    writer.writerow([
                        customer['idx'],
                        customer['nik'],
                        customer['name'],
                        customer['born'],
                        customer['active'],
                        customer['salary']
                    ])
            
            return True, f"Berhasil mengekspor {len(customers)} data"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def import_from_csv(self, file_path):
        try:
            success_count = 0
            error_count = 0
            error_messages = [] # List to store error messages
            
            with open(file_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile, delimiter=';')
                
                # Skip header
                next(reader)
                
                for row_number, row in enumerate(reader, start=2): # Start from row 2 to account for header
                    try:
                        if len(row) >= 5:
                            nik = row[0]
                            name = row[1]
                            born = datetime.strptime(row[2], "%Y-%m-%d").date() if row[3] else None
                            active = int(row[3]) if row[3] else 0
                            salary = int(row[4]) if row[4] else 0
                            
                            if self.customer_model.create_customer(nik, name, born, active, salary):
                                success_count += 1
                            else:
                                error_messages.append(f"Row {row_number}: Gagal menyimpan data untuk NIK {nik}")
                                error_count += 1
                        else:
                            error_messages.append(f"Row {row_number}: invalid row length")
                            error_count += 1
                    except ValueError as ve:
                        error_messages.append(f"Row {row_number}: Value error - {str(ve)}")
                        error_count += 1
                    except Exception as e:
                        error_messages.append(f"Row {row_number}: Unexpected error - {e}")
                        error_count += 1

            # print error messages if any
            for message in error_messages:
                print(message)
            
            return True, f"Berhasil import {success_count} data, gagal {error_count} data"
        except Exception as e:
            return False, f"Error: {str(e)}"