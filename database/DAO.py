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
    def getConnectionsOfColor(color):
        result = []
        try:
            conn = DBConnect.get_connection()
            cursor = conn.cursor(dictionary=True)
            query = """ 
                        select distinct (gp.Product_number), gds.Retailer_code , day(gds.`Date`) as day, month (gds.`Date`) as mounth 
                        from go_products gp, go_daily_sales gds 
                        where gp.Product_color = COALESCE(%s, gp.Product_color) and gp.Product_number = gds.Product_number and year (gds.`Date`) = COALESCE(%s, year (gds.`Date`))
                    """
            cursor.execute(query, (color,))

            for row in cursor:
                result.append((row["Product_number"], row["Retailer_code"], row["day"], row["mounth"]))

        except Exception as e:
            print(f"Error fetching colors: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        return result