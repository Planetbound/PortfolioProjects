Group #: 47
CCID: spaine
Name: Seth Paine
Resources Used:
	https://www.geeksforgeeks.org/sql-select-random/
	https://github.com/BVLC/caffe/issues/861
	https://matplotlib.org/stable/gallery/lines_bars_and_markers/barchart.html

I declare that I did not collaborate with anyone outside of my own group in this assignment.

For Q1, i created indexes for columns that are accessed and compared in the WHERE clause through the process of the query (customer_postal_code, customer_id for both Orders and Customers, order_id for both Orders and Order_items, and order_item_id) to reduce the amount of linear scans with the data to be done.
For similar reasons, I added indexes for customer_postal_code, customer_id for both Orders and Customers, and order_id for Q2; customer_postal_code, customer_id for both Orders and Customers, and order_id for both Orders and Order_items for Q3; customer_id for Orders, order_id for both Orders and Order_items, seller_id for both Order_items and Sellers, and order_item_id for Q4.