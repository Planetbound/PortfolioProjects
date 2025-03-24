### Q2A3 ###

import sqlite3
import time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

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


def create_indexes():
    global connection, cursor
    cursor.execute('CREATE INDEX customer_postal_codeIdx ON Customers (customer_postal_code);')
    cursor.execute('CREATE INDEX c_customer_idIdx ON Customers (customer_id);')
    cursor.execute('CREATE INDEX o_customer_idIdx ON Orders (customer_id);')
    cursor.execute('CREATE INDEX o_order_idIdx ON Orders (order_id);')


def drop_indexes():
    global connection, cursor
    cursor.execute('DROP INDEX IF EXISTS customer_postal_codeIdx;')
    cursor.execute('DROP INDEX IF EXISTS c_customer_idIdx;')
    cursor.execute('DROP INDEX IF EXISTS o_customer_idIdx;')
    cursor.execute('DROP INDEX IF EXISTS o_order_idIdx;')


def create_view():
    global connection, cursor
    cursor.execute('''
                    CREATE VIEW OrderSize AS
	                SELECT order_id AS oid, COUNT(*) AS size
	                FROM Order_items
	                GROUP BY oid;
                    ''')


def drop_view():
    global connection, cursor
    cursor.execute('DROP VIEW OrderSize')


def run_query():
    global connection, cursor
    cursor.execute('SELECT customer_postal_code FROM Customers ORDER BY RANDOM() LIMIT 1;')
    rand_postal_code = cursor.fetchone()
    cursor.execute('''
                    SELECT COUNT(*)
                    FROM Customers c, Orders o, OrderSize s
                    WHERE customer_postal_code = ?
                    AND c.customer_id = o.customer_id
                    AND o.order_id = s.oid
                    AND size > 
	                    (SELECT AVG(size)
	                    FROM OrderSize);
                    ''', rand_postal_code)



def main():
    global connection, cursor

    ###Small db###

    ## Uninformed
    path = "./A3Small.db"
    connect(path)
    create_view()
    cursor.execute('PRAGMA automatic_index = FALSE;')
    uninform()
    start_time = time.time()
    for i in range(50):
        run_query()
    end_time = time.time() - start_time
    small_unin_time = round((end_time / 50) * 1000, 0) #in ms
    reinform()
    connection.commit()
    connection.close()


    ## Self-optimized
    path = "./A3Small.db"
    connect(path)
    cursor.execute('PRAGMA automatic_index = TRUE;')
    start_time = time.time()
    for i in range(50):
        run_query()
    end_time = time.time() - start_time
    small_self_time = round((end_time / 50) * 1000, 0)
    connection.commit()
    connection.close()


    ## User-optimized
    path = "./A3Small.db"
    connect(path)
    cursor.execute('PRAGMA automatic_index = FALSE;')
    create_indexes()
    start_time = time.time()
    for i in range(50):
        run_query()
    end_time = time.time() - start_time
    small_user_time = round((end_time / 50) * 1000, 0)
    drop_indexes()
    drop_view()
    connection.commit()
    connection.close()



    ###Medium db###

    ## Uninformed
    path = "./A3Medium.db"
    connect(path)
    create_view()
    cursor.execute('PRAGMA automatic_index = FALSE;')
    uninform()
    start_time = time.time()
    for i in range(50):
        run_query()
    end_time = time.time() - start_time
    med_unin_time = round((end_time / 50) * 1000, 0)
    reinform()
    connection.commit()
    connection.close()


    ## Self-optimized
    path = "./A3Medium.db"
    connect(path)
    cursor.execute('PRAGMA automatic_index = TRUE;')
    start_time = time.time()
    for i in range(50):
        run_query()
    end_time = time.time() - start_time
    med_self_time = round((end_time / 50) * 1000, 0)
    connection.commit()
    connection.close()


    ## User-optimized
    path = "./A3Medium.db"
    connect(path)
    cursor.execute('PRAGMA automatic_index = FALSE;')
    create_indexes()
    start_time = time.time()
    for i in range(50):
        run_query()
    end_time = time.time() - start_time
    med_user_time = round((end_time / 50) * 1000, 0)
    drop_indexes()
    drop_view()
    connection.commit()
    connection.close()



    ###Large db###

    ## Uninformed
    path = "./A3Large.db"
    connect(path)
    create_view()
    cursor.execute('PRAGMA automatic_index = FALSE;')
    uninform()
    start_time = time.time()
    for i in range(50):
        run_query()
    end_time = time.time() - start_time
    large_unin_time = round((end_time / 50) * 1000, 0)
    reinform()
    connection.commit()
    connection.close()


    ## Self-optimized
    path = "./A3Large.db"
    connect(path)
    cursor.execute('PRAGMA automatic_index = TRUE;')
    start_time = time.time()
    for i in range(50):
        run_query()
    end_time = time.time() - start_time
    large_self_time = round((end_time / 50) * 1000, 0)
    connection.commit()
    connection.close()


    ## User-optimized
    path = "./A3Large.db"
    connect(path)
    cursor.execute('PRAGMA automatic_index = FALSE;')
    create_indexes()
    start_time = time.time()
    for i in range(50):
        run_query()
    end_time = time.time() - start_time
    large_user_time = round((end_time / 50) * 1000, 0)
    drop_indexes()
    drop_view()
    connection.commit()
    connection.close()



    # Make graphs #
    databases = ("SmallDB", "MediumDB", "LargeDB")
    avg_times = {
        'User-Optimized': (small_user_time, med_user_time, large_user_time),
        'Self-Optimized': (small_self_time, med_self_time, large_self_time),
        'Uninformed': (small_unin_time, med_unin_time, large_unin_time),
    }

    x = np.arange(len(databases))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0.1

    fig, ax = plt.subplots()

    for attribute, measurement in avg_times.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, padding=3)
        multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Avg Time (ms)')
    ax.set_title('Query Runtime')
    ax.set_xticks(x + width, databases)
    ax.legend(loc='upper left', ncols=3)
    ax.set_ylim(0, 250)

    plt.savefig('Q2A3chart.png')

    return


if __name__ == "__main__":
    main()