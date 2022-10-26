import psycopg2

def drop_db(cur):
    cur.execute("""
    DROP TABLE client, telephone;
            """)

def create_db(cur):
    cur.execute("""
    CREATE TABLE client (
    client_id SERIAL PRIMARY KEY,
    last_name VARCHAR(60) NOT NULL,
    first_name VARCHAR(60) NOT NULL,
    email VARCHAR(60) NOT NULL UNIQUE,
    last_update TIMESTAMP NOT NULL DEFAULT NOW(),
    deleted BOOLEAN DEFAULT FALSE NOT NULL
    );

    CREATE TABLE telephone (
    telephone_id SERIAL PRIMARY KEY,
    telephone INTEGER UNIQUE,
    client_id INTEGER REFERENCES client(client_id),
    last_update TIMESTAMP NOT NULL DEFAULT NOW(),
    deleted BOOLEAN DEFAULT FALSE NOT NULL
    );
            """)

def add_client(cur, first_name, last_name, email):
    cur.execute("""
    INSERT INTO client(last_name, first_name, email) VALUES(%s, %s, %s);
    """, (last_name, first_name, email))


def add_phone(cur, client_id, phone):
    cur.execute("""
    INSERT INTO telephone(client_id, telephone) VALUES(%s, %s);
    """, (client_id, phone))


def change_client(cur, client_id, first_name=None, last_name=None, email=None, phone=None):
   
    if phone != None:
        cur.execute("""
            UPDATE telephone SET telephone=%s WHERE client_id=%s;
            """, (phone, client_id))
    else: pass
    
    if first_name != None:
        cur.execute("""
            UPDATE client SET first_name=%s WHERE client_id=%s;
            """, (first_name, client_id))
    else: pass
    
    if last_name != None:
        cur.execute("""
            UPDATE client SET last_name=%s WHERE client_id=%s;
            """, (last_name, client_id))
    else: pass
    
    if email != None:
        cur.execute("""
            UPDATE client SET email=%s WHERE client_id=%s;
            """, (email, client_id))
    else: pass
    
def delete_phone(cur, client_id, phone):
    cur.execute("""
        DELETE FROM telephone WHERE client_id=%s AND telephone=%s;
        """, (client_id, phone))

def delete_client(cur, client_id):
    cur.execute("""
        DELETE FROM telephone WHERE client_id=%s;
        DELETE FROM client WHERE client_id=%s;
        """, (client_id, client_id))


def find_client(cur, first_name=None, last_name=None, email=None, phone=None):
    cur.execute("""
        SELECT c.last_name, c.first_name, c.email, t.telephone 
        FROM client c
        JOIN telephone t ON t.client_id = c.client_id  
        WHERE last_name=%s OR first_name=%s OR email=%s OR telephone=%s
        """, (last_name, first_name, email, phone))
    print(cur.fetchall())

if __name__ == '__main__':
    with psycopg2.connect(database="", user="", password="") as conn:
        with conn.cursor() as cur:
            drop_db(cur)
            create_db(cur)
            add_client(cur, 'first_name5', 'last_name5', 'email5')
            add_client(cur, 'first_name6', 'last_name6', 'email6')
            add_client(cur, 'first_name7', 'last_name7', 'email7')
            add_phone(cur, '1', '11117211')
            add_phone(cur, '1', '131313131')
            add_phone(cur, '1', '8888888')
            add_phone(cur, '2', '11142811')
            add_phone(cur, '2', '44444444')
            add_phone(cur, '3', '11133191')
            change_client(cur, client_id='3', email='супермен', phone='96969696')
            change_client(cur, client_id='1', email='супермен3')
            delete_phone(cur, client_id='1', phone='11117211')
            delete_client(cur, client_id='2')
            find_client(cur, last_name='last_name5', email='email6', phone='96969696')
            find_client(cur, phone='11117211')
    cur.close()