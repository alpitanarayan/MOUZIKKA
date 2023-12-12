import cx_Oracle
import traceback
conn=None
# username = "mouzikaa"
# password = "music"
# dsn = "127.0.0.1"  # Oracle Database System Name (TNS entry)

# Create a connection


# try:
#     # conn=cx_Oracle.connect("mouzikka/music@localhost")
#     # # conn = cx_Oracle.connect(username, password, dsn)
#     # print("Connected successfully to Oracle")
#
try:
    conn = cx_Oracle.connect("c##mouzikka/music@127.0.0.1/orcl")
    print("Connected successfully to Oracle")

except cx_Oracle.DatabaseError:
    print("Error in connecting to Oracle")
    print(traceback.format_exc())
finally:
    if conn is not None:
        conn.close()
        print("Disconnected with Oracle successfully")

