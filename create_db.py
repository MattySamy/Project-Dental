from pickle import TRUE
from database import get_db
def create_tables(db):
    conn = db
    with open("tables.sql",'r') as table:
        conn.execute(table.read())
    conn.close()
    return TRUE

create_tables(get_db())