-- Create table for 'cart'
CREATE TABLE IF NOT EXISTS cart (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    pdt_id INT NOT NULL,
    stock_quantity INT,
    FOREIGN KEY (pdt_id) REFERENCES products(id)
);

-- Create table for 'currentuser'
CREATE TABLE IF NOT EXISTS currentuser (
    currentid INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    id INT,
    username VARCHAR(255),
    FOREIGN KEY (id) REFERENCES login(id)
);

-- Create table for 'login'
CREATE TABLE IF NOT EXISTS login (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Create table for 'orders'
CREATE TABLE IF NOT EXISTS orders (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    pdt_id INT NOT NULL,
    stock_quantity INT,
    user_id INT,
    order_date DATE,
    order_time TIME,
    FOREIGN KEY (pdt_id) REFERENCES products(id),
    FOREIGN KEY (user_id) REFERENCES currentuser(id)
);

-- Create table for 'products'
CREATE TABLE IF NOT EXISTS products (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255),
    price DECIMAL(10,2),
    image BLOB,
    stock_quantity INT,
    rating INT
);

-- Create table for 'ratings'
CREATE TABLE IF NOT EXISTS ratings (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    pdt_id INT NOT NULL,
    rating INT NOT NULL,
    user_id INT,
    username VARCHAR(255),
    FOREIGN KEY (pdt_id) REFERENCES products(id),
    FOREIGN KEY (user_id) REFERENCES currentuser(id)
);
