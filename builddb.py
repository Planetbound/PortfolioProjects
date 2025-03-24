## Builds the databases ##

import pandas as pd
import random
import sqlite3

connection = None
cursor = None

def connect(path):
    global connection, cursor
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute('PRAGMA foreign_keys=ON;')
    connection.commit()
    return


def drop_tables():
    global connection, cursor
    drop_customers = "DROP TABLE IF EXISTS Customers;"
    drop_sellers = "DROP TABLE IF EXISTS Sellers;"
    drop_orders = "DROP TABLE IF EXISTS Orders;"
    drop_items = "DROP TABLE IF EXISTS Order_items;"
    cursor.execute(drop_customers)
    cursor.execute(drop_sellers)
    cursor.execute(drop_orders)
    cursor.execute(drop_items)


def define_tables():
    global connection, cursor
    customer_query = '''
                    CREATE TABLE Customers (
                                customer_id TEXT,
                                customer_postal_code INTEGER,
                                PRIMARY KEY(customer_id)
                                );
                    '''

    seller_query = '''
                    CREATE TABLE Sellers (
                                seller_id TEXT,
                                seller_postal_code INTEGER,
                                PRIMARY KEY(seller_id)
                                );
                    '''

    order_query = '''
                    CREATE TABLE Orders (
                                order_id TEXT,
                                customer_id TEXT,
                                PRIMARY KEY(order_id),
                                FOREIGN KEY(customer_id) REFERENCES Customers(customer_id)
                                );
                    '''
    
    item_query = '''
                    CREATE TABLE Order_items (
                                order_id TEXT,
                                order_item_id INTEGER,
                                product_id TEXT,
                                seller_id TEXT,
                                PRIMARY KEY(order_id,order_item_id,product_id,seller_id),
                                FOREIGN KEY(seller_id) REFERENCES Sellers(seller_id)
                                FOREIGN KEY(order_id) REFERENCES Orders(order_id)
                                );
                    '''

    cursor.execute(customer_query)
    cursor.execute(seller_query)
    cursor.execute(order_query)
    cursor.execute(item_query)
    connection.commit()

    return


def insert_data(cust, sell, ord, orditem):
    global connection, cursor

    for row in cust.itertuples():
        cursor.execute('INSERT INTO Customers (customer_id, customer_postal_code) VALUES (?,?);',
                       (row.customer_id, row.customer_zip_code_prefix))
    
    for row in sell.itertuples():
        cursor.execute('INSERT INTO Sellers (seller_id, seller_postal_code) VALUES (?,?);',
                       (row.seller_id, row.seller_zip_code_prefix))
    
    for row in ord.itertuples():
        cursor.execute('INSERT INTO Orders (order_id, customer_id) VALUES (?,?);',
                       (row.order_id, row.customer_id))
    
    for row in orditem.itertuples():
        cursor.execute('INSERT INTO Order_items (order_id, order_item_id, product_id, seller_id) VALUES (?,?,?,?);',
                       (row.order_id, row.order_item_id, row.product_id, row.seller_id))

    connection.commit()
    return


def main():
    random.seed(72)

    #Get set of customer ids and seller ids for small db

    small_customers = pd.read_csv("olist_customers_dataset.csv", skiprows=lambda x: x>0 and random.random() >= 0.1)
    small_customers_data = pd.DataFrame(small_customers)

    small_sellers = pd.read_csv("olist_sellers_dataset.csv", skiprows=lambda x: x>0 and random.random() >= 0.16)
    small_sellers_data = pd.DataFrame(small_sellers)

    s_c = set()
    for row in small_customers_data.itertuples():
        s_c.add(row.customer_id)

    s_s = set()
    for row in small_sellers_data.itertuples():
        s_s.add(row.seller_id)


    #Get set of customer ids and seller ids for med db

    med_customers = pd.read_csv("olist_customers_dataset.csv", skiprows=lambda x: x>0 and random.random() >= 0.2)
    med_customers_data = pd.DataFrame(med_customers)

    med_sellers = pd.read_csv("olist_sellers_dataset.csv", skiprows=lambda x: x>0 and random.random() >= 0.24)
    med_sellers_data = pd.DataFrame(med_sellers)

    m_c = set()
    for row in med_customers_data.itertuples():
        m_c.add(row.customer_id)

    m_s = set()
    for row in med_sellers_data.itertuples():
        m_s.add(row.seller_id)


    #Get set of customer ids and seller ids for large db

    large_customers = pd.read_csv("olist_customers_dataset.csv", skiprows=lambda x: x>0 and random.random() >= 0.33)
    large_customers_data = pd.DataFrame(large_customers)

    large_sellers = pd.read_csv("olist_sellers_dataset.csv", skiprows=lambda x: x>0 and random.random() >= 0.32)
    large_sellers_data = pd.DataFrame(large_sellers)

    l_c = set()
    for row in large_customers_data.itertuples():
        l_c.add(row.customer_id)

    l_s = set()
    for row in large_sellers_data.itertuples():
        l_s.add(row.seller_id)


    #Get the orders data for each db

    orders = pd.read_csv("olist_orders_dataset.csv")
    orders_data = pd.DataFrame(orders)

    small_orders_data = orders_data.loc[orders_data['customer_id'].isin(s_c)]
    med_orders_data = orders_data.loc[orders_data['customer_id'].isin(m_c)]
    large_orders_data = orders_data.loc[orders_data['customer_id'].isin(l_c)]


    #Get set of order ids for each db

    s_o = set()
    for row in small_orders_data.itertuples():
        s_o.add(row.order_id)

    m_o = set()
    for row in med_orders_data.itertuples():
        m_o.add(row.order_id)

    l_o = set()
    for row in large_orders_data.itertuples():
        l_o.add(row.order_id)


    #Get the items data for each db

    items = pd.read_csv("olist_order_items_dataset.csv")
    items_data = pd.DataFrame(items)

    small_items_data = items_data.loc[(items_data['order_id'].isin(s_o)) & (items_data['seller_id'].isin(s_s))]
    med_items_data = items_data.loc[(items_data['order_id'].isin(m_o)) & (items_data['seller_id'].isin(m_s))]
    large_items_data = items_data.loc[(items_data['order_id'].isin(l_o)) & (items_data['seller_id'].isin(l_s))]


    global connection, cursor

    #small db
    path = "./A3Small.db"
    connect(path)
    drop_tables()
    define_tables()
    insert_data(small_customers_data, small_sellers_data, small_orders_data, small_items_data)
    connection.commit()
    connection.close()

    #med db
    path = "./A3Medium.db"
    connect(path)
    drop_tables()
    define_tables()
    insert_data(med_customers_data, med_sellers_data, med_orders_data, med_items_data)
    connection.commit()
    connection.close()

    #large db
    path = "./A3Large.db"
    connect(path)
    drop_tables()
    define_tables()
    insert_data(large_customers_data, large_sellers_data, large_orders_data, large_items_data)
    connection.commit()
    connection.close()

    return


if __name__ == "__main__":
    main()
