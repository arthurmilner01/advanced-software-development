import sqlite3

def CreateDatabase():
    con = sqlite3.connect("HorizonCinemasDB.db")
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS bookingstaff(
        bookingstaff_id INTEGER NOT NULL PRIMARY KEY,
        email VARCHAR(120) NOT NULL UNIQUE,
        password VARCHAR(120) NOT NULL,
        cinema_name VARCHAR(120) NOT NULL
    );
    """)
    cur.execute("""
    INSERT INTO bookingstaff
        (email,
        password,
        cinema_name)
    VALUES
        ('arthur@gmail.com', 'arthur', 'Cabot Circus')
    """)
    con.commit()
    return con, cur