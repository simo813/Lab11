from database.DB_connect import DBConnect
from model.product import Product


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getColors():
        result = []
        try:
            conn = DBConnect.get_connection()
            cursor = conn.cursor(dictionary=True)
            query = """ 
                SELECT DISTINCT gp.Product_color
                FROM go_products gp
            """
            cursor.execute(query)

            for row in cursor:
                result.append(row["Product_color"])

        except Exception as e:
            print(f"Error fetching colors: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        return result

    @staticmethod
    def getProductsOfColor(color):
        result = []
        try:
            conn = DBConnect.get_connection()
            cursor = conn.cursor(dictionary=True)
            query = """ 
                    select *
                    from go_products gp
                    where gp.Product_color = COALESCE(%s, gp.Product_color)
                """
            cursor.execute(query, (color,))

            for row in cursor:
                result.append(Product(row["Product_number"], row["Product_line"], row["Product_type"], row["Product"], row["Product_brand"], row["Product_color"], row["Unit_cost"], row["Unit_price"]))

        except Exception as e:
            print(f"Error fetching colors: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        return result