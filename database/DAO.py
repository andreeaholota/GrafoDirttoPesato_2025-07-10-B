from database.DB_connect import DBConnect

from model.product import Product
from model.category import Category


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getDateRange():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct (order_date) from orders o order by order_date"

        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last


    @staticmethod
    def getAllCat():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * from categories"

        cursor.execute(query)

        for row in cursor:
            results.append(Category(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllProductsbyCategory(cat):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select * from products p 
                    where p.category_id = %s"""

        cursor.execute(query, (cat.category_id,))

        for row in cursor:
            results.append(Product(**row))

        cursor.close()
        conn.close()
        return results


    @staticmethod
    def getEdges(cat, d1, d2, idMap):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select t1.product_id as n1, t2.product_id as n2, t1.num+t2.num as peso
                    from (SELECT p.product_id , sum(oi.quantity) as num
                    FROM products p, order_items oi, orders o 
                    WHERE p.product_id = oi.product_id and oi.order_id = o.order_id 
                    and o.order_date BETWEEN %s and %s
                    and p.category_id = %s
                    group by (p.product_id)
                    order by p.product_id ) t1, 
                    (SELECT p.product_id , sum(oi.quantity) as num
                    FROM products p, order_items oi, orders o 
                    WHERE p.product_id = oi.product_id and oi.order_id = o.order_id 
                    and o.order_date BETWEEN %s and %s
                    and p.category_id = %s
                    group by (p.product_id)
                    order by p.product_id ) t2
                    where t1.num <= t2.num
                    and t1.product_id <> t2.product_id
                    order by peso desc, n1 asc, n2 asc"""

        cursor.execute(query, (d1,d2,cat.category_id,d1,d2,cat.category_id))

        for row in cursor:
            results.append((idMap[row["n1"]],idMap[row["n2"]], row["peso"]))

        cursor.close()
        conn.close()
        return results