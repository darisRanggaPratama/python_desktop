from datetime import datetime
from config.database import DatabaseConfig

class Customer:
    def __init__(self):
        self.db_config = DatabaseConfig()
    
    def get_all_customers(self, limit=10, offset=0, search_term=""):
        connection = self.db_config.get_connection()
        if not connection:
            return [], 0
        
        try:
            cursor = connection.cursor(dictionary=True)
            
            # Build search query
            search_condition = ""
            params = []
            
            if search_term:
                search_condition = """
                WHERE nik LIKE %s OR name LIKE %s OR 
                born LIKE %s OR active LIKE %s OR salary LIKE %s
                """
                search_param = f"%{search_term}%"
                params = [search_param] * 5
            
            # Get total count
            count_query = f"SELECT COUNT(*) as total FROM customer {search_condition}"
            cursor.execute(count_query, params)
            total_count = cursor.fetchone()['total']
            
            # Get paginated data
            query = f"""
            SELECT idx, nik, name, born, active, salary 
            FROM customer {search_condition}
            ORDER BY idx DESC 
            LIMIT %s OFFSET %s
            """
            cursor.execute(query, params + [limit, offset])
            customers = cursor.fetchall()
            
            return customers, total_count
            
        except Exception as e:
            print(f"Error fetching customers: {e}")
            return [], 0
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    
    def get_customer_by_id(self, customer_id):
        connection = self.db_config.get_connection()
        if not connection:
            return None
        
        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM customer WHERE idx = %s"
            cursor.execute(query, (customer_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error fetching customer: {e}")
            return None
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    
    def create_customer(self, nik, name, born, active, salary):
        connection = self.db_config.get_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            query = """
            INSERT INTO customer (nik, name, born, active, salary) 
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (nik, name, born, active, salary))
            connection.commit()
            return True
        except Exception as e:
            print(f"Error creating customer: {e}")
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    
    def update_customer(self, customer_id, nik, name, born, active, salary):
        connection = self.db_config.get_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            query = """
            UPDATE customer 
            SET nik = %s, name = %s, born = %s, active = %s, salary = %s 
            WHERE idx = %s
            """
            cursor.execute(query, (nik, name, born, active, salary, customer_id))
            connection.commit()
            return True
        except Exception as e:
            print(f"Error updating customer: {e}")
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    
    def delete_customer(self, customer_id):
        connection = self.db_config.get_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            query = "DELETE FROM customer WHERE idx = %s"
            cursor.execute(query, (customer_id,))
            connection.commit()
            return True
        except Exception as e:
            print(f"Error deleting customer: {e}")
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()