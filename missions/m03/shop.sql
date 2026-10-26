CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT NOT NULL, region TEXT NOT NULL);
CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER REFERENCES customers(id), amount REAL NOT NULL, status TEXT NOT NULL);
INSERT INTO customers VALUES (1, 'Ada Park', 'North'), (2, 'Ben Osei', 'South'), (3, 'Cleo Ruiz', 'North'), (4, 'Dev Larsen', 'East'), (5, 'Eva Lind', 'South');
INSERT INTO orders VALUES (10, 1, 250.0, 'paid'), (11, 1, 100.0, 'refunded'), (12, 2, 80.0, 'paid'), (13, 3, 40.0, 'paid'), (14, 2, 120.0, 'paid'), (15, 4, 300.0, 'cancelled');
