CREATE TABLE IF NOT EXISTS Products(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    description VARCHAR(8000) NOT NULL,
    price FLOAT NOT NULL
);

CREATE TABLE IF NOT EXISTS Product_flavours(
    flavour_id INT AUTO_INCREMENT PRIMARY KEY,
    flavour VARCHAR(30) NOT NULL,
    description VARCHAR(500) NOT NULL
);

CREATE TABLE IF NOT EXISTS Product_variations(
    variation_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    flavour_id INT NOT NULL,
    in_stock INT NOT NULL,
    FOREIGN KEY (product_id) REFERENCES Products(id),
    FOREIGN KEY (flavour_id) REFERENCES Product_flavours(flavour_id)
);

CREATE TABLE IF NOT EXISTS Sales(
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    variation_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (variation_id) REFERENCES Product_variations(variation_id),
    FOREIGN KEY (product_id) REFERENCES Products(id)
);