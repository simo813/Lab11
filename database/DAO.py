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

    @staticmethod
    def getConnections(data, prodotto1, prodotto2):
        result = None
        try:
            conn = DBConnect.get_connection()
            cursor = conn.cursor(dictionary=True)
            query = """ 
                SELECT COUNT(f.date) as weight
                FROM (
                    SELECT DISTINCT(t1.`Date`) AS date
                    FROM go_daily_sales t1, go_daily_sales t2
                    WHERE YEAR(t1.`Date`) = %s
                      AND t1.Retailer_code = t2.Retailer_code 
                      AND t1.`Date` = t2.`Date` 
                      AND t1.Product_number = %s 
                      AND t2.Product_number = %s
                    GROUP BY t1.`Date`
                ) AS f;


            """
            cursor.execute(query, (data, prodotto1.Product_number, prodotto2.Product_number))
            row = cursor.fetchone()
            result = row["weight"] if row else 0

        except Exception as e:
            print(f"Error fetching connections: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        return result
