import mysql.connector

def connectDB():
    return mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "kenthlangnamankasitoe27321",
        database = "inquipay"
    )