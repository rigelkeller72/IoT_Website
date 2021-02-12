import sqlite3


def main():
    conn = sqlite3.connect("site_data.db")
    # Adding new data with the INSERT statement
    cursor = conn.execute("INSERT INTO temperature VALUES ('00:30', '001','30','DHT-11')")
    cursor.close()
    conn.commit()


    # Querying the database with SELECT statement
    cursor = conn.execute("SELECT * from temperature")
    records = cursor.fetchall()
    for record in records:
        print('Time: %s, Sensor ID: %s, Reading: %s, Sensor Type: %s' % (record[0], record[1], record[2], record[3]))
    cursor.close()
    conn.close()


if __name__=="__main__":
    main()
