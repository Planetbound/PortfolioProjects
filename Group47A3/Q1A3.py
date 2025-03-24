### A3Q1 ###

import sqlite3
import time

connection = None
cursor = None

def connect(path):
    global connection, cursor
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute('PRAGMA foreign_keys=ON;')
    connection.commit()
    return


def uninform():
    global connection, cursor
    cursor.execute('PRAGMA foreign_keys=OFF;')

    #Create new tables without pk and fk
    cursor.execute('ALTER TABLE Customers RENAME TO pk_Customers;')
    customer_query = '''
                    CREATE TABLE Customers(
                                customer_id TEXT,
                                customer_postal_code INTEGER
                                );
                    '''
    cursor.execute('ALTER TABLE Sellers RENAME TO pk_Sellers;')
    seller_query = '''
                    CREATE TABLE Sellers(
                                seller_id TEXT,
                                seller_postal_code INTEGER
                                );
                    '''
    cursor.execute('ALTER TABLE Orders RENAME TO pk_Orders;')
    order_query = '''
                    CREATE TABLE Orders(
                                order_id TEXT,
                                customer_id TEXT
                                );
                    '''
    cursor.execute('ALTER TABLE Order_items RENAME TO pk_Order_items;')
    item_query = '''
                    CREATE TABLE Order_items(
                                order_id TEXT,
                                order_item_id INTEGER,
                                product_id TEXT,
                                seller_id TEXT
                                );
                    '''
    cursor.execute(customer_query)
    cursor.execute(seller_query)
    cursor.execute(order_query)
    cursor.execute(item_query)

    #Insert the values into these new tables
    cursor.execute('INSERT INTO Customers SELECT * FROM pk_Customers;')
    cursor.execute('INSERT INTO Sellers SELECT * FROM pk_Sellers;')
    cursor.execute('INSERT INTO Orders SELECT * FROM pk_Orders;')
    cursor.execute('INSERT INTO Order_items SELECT * FROM pk_Order_items;')
    
    connection.commit()
    return


def reinform():
    global connection, cursor
    cursor.execute('PRAGMA foreign_keys=ON;')

    cursor.execute('ALTER TABLE Customers RENAME TO nopk_Customers;')
    cursor.execute('ALTER TABLE pk_Customers RENAME TO Customers;')
    cursor.execute('ALTER TABLE Sellers RENAME TO nopk_Sellers;')
    cursor.execute('ALTER TABLE pk_Sellers RENAME TO Sellers;')
    cursor.execute('ALTER TABLE Orders RENAME TO nopk_Orders;')
    cursor.execute('ALTER TABLE pk_Orders RENAME TO Orders;')
    cursor.execute('ALTER TABLE Order_items RENAME TO nopk_Order_items;')
    cursor.execute('ALTER TABLE pk_Order_items RENAME TO Order_items;')
    cursor.execute('DROP TABLE nopk_Customers;')
    cursor.execute('DROP TABLE nopk_Sellers;')
    cursor.execute('DROP TABLE nopk_Orders;')
    cursor.execute('DROP TABLE nopk_Order_items;')

    connection.commit()
    return




def run_query():
    global connection, cursor
    cursor.execute('SELECT customer_postal_code FROM Customers ORDER BY RANDOM() LIMIT 1;')
    rand_postal_code = cursor.fetchone()
    cursor.execute('''
                    SELECT COUNT(*)
                    FROM Orders o, Customers c
                    WHERE customer_postal_code = ?
                    AND c.customer_id = o.customer_id
                    AND o.order_id IN
                        (SELECT order_id
                        FROM Order_items
                        GROUP BY order_id
                        HAVING COUNT(*) > 1);
    ''', rand_postal_code)
    #cursor.fetchall()




def main():
    global connection, cursor
    times_taken = []

    ###Small db###

    ## Uninformed
    path = "./A3Small.db"
    connect(path)
    cursor.execute('PRAGMA automatic_index = FALSE;')
    uninform()
    start_time = time.time()
    for i in range(50):
        run_query()
    end_time = time.time() - start_time
    small_unin_time = end_time / 50
    reinform()
    connection.commit()
    connection.close()

    times_taken.append(small_unin_time)
    print(small_unin_time)


    ## Self-optimized
    path = "./A3Small.db"
    connect(path)
    cursor.execute('PRAGMA automatic_index = TRUE;')
    start_time = time.time()
    for i in range(50):
        run_query()
    end_time = time.time() - start_time
    small_self_time = end_time / 50
    connection.commit()
    connection.close()

    times_taken.append(small_self_time)
    print(small_self_time)


    ## User-optimized
    path = "./A3Small.db"
    connect(path)
    cursor.execute('PRAGMA automatic_index = FALSE;')
    #Make indexes
    #cursor.execute('CREATE INDEX customer_idIdx ON Customers (customer_id);')
    #cursor.execute('CREATE INDEX customer_postal_codeIdx ON Customers (customer_postal_code);')
    #cursor.execute('CREATE INDEX order_idIdx ON Orders (order_id);')
    start_time = time.time()
    for i in range(50):
        run_query()
    end_time = time.time() - start_time
    small_user_time = end_time / 50
    cursor.execute('DROP INDEX IF EXISTS customer_idIdx;')
    cursor.execute('DROP INDEX IF EXISTS customer_postal_codeIdx;')
    cursor.execute('DROP INDEX IF EXISTS order_idIdx;')
    connection.commit()
    connection.close()

    times_taken.append(small_user_time)
    print(small_user_time)

    return


if __name__ == "__main__":
    main()