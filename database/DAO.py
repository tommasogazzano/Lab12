from database.DB_connect import DBConnect
from model.retailer import Retailer


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getCountries():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        result = []

        query = '''SELECT distinct gr.Country as nation from go_retailers gr '''
        cursor.execute(query)
        for row in cursor:
            result.append(row["nation"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getYears():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        result = []

        query = '''SELECT DISTINCT year(gds.`Date`) as y
                    from go_daily_sales gds 
                    where year(gds.`Date` ) <= 2018 and year(gds.`Date`) >= 2015'''
        cursor.execute(query)
        for row in cursor:
            result.append(row["y"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getRetailers(nazione):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        result = []

        query = '''SELECT gr.*
                    from go_retailers gr 
                    where gr.Country = %s'''
        cursor.execute(query, (nazione,))
        for row in cursor:
            result.append(Retailer(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdges(anno, country, idMap):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        result = []

        query = '''SELECT 
                        gr1.Retailer_code AS R1,
                        gr2.Retailer_code AS R2,
                        COUNT(DISTINCT gds1.Product_number) AS peso
                    FROM 
                        go_retailers gr1, 
                        go_retailers gr2, 
                        go_daily_sales gds1, 
                        go_daily_sales gds2
                    WHERE 
                        gr1.Retailer_code = gds1.Retailer_code
                        AND gr2.Retailer_code = gds2.Retailer_code
                        AND gr1.Country = %s
                        AND gr2.Country = %s
                        AND YEAR(gds1.Date) = %s
                        AND YEAR(gds2.Date) = %s
                        AND gds1.Product_number = gds2.Product_number
                        AND gr1.Retailer_code < gr2.Retailer_code
                    GROUP BY 
                        gr1.Retailer_code, gr2.Retailer_code
                    HAVING 
                        peso > 0'''
        cursor.execute(query, (country, country, anno, anno))
        for row in cursor:
            if row["R1"] in idMap and row["R2"] in idMap:
                result.append((idMap[row["R1"]], idMap[row["R2"]], row["peso"]))

        cursor.close()
        conn.close()
        return result


