/**
 Author: UMD Marketplace team
 Model : UMD Marketplace
**/

DROP SCHEMA IF EXISTS umd_marketplace;

CREATE SCHEMA umd_marketplace;
USE umd_marketplace;

DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Product;
DROP TABLE IF EXISTS ShopCart;

/* Table: User */
CREATE TABLE User (
  userId INT PRIMARY KEY auto_increment,
  name VARCHAR(20) NOT NULL,
  userName VARCHAR(20) UNIQUE NOT NULL,
  email VARCHAR(20) UNIQUE NOT NULL,
  password VARCHAR(500) NOT NULL
);

/* Table: Product */
CREATE TABLE Product (
    productId INT PRIMARY KEY auto_increment,
    productName VARCHAR(20) NOT NULL,
    prodDescription VARCHAR(50) NOT NULL,
    category VARCHAR(20) NOT NULL,
    productImage BLOB,
    price DECIMAL(10,2)
);

/* Table: ShopCart */
CREATE TABLE ShopCart (
    cartId INT PRIMARY KEY auto_increment,
    userId INTEGER NOT NULL,
    productId INTEGER NOT NULL
);

/* Foreign Key: ShopCart */
ALTER TABLE ShopCart ADD CONSTRAINT fk_ShopCart__User FOREIGN KEY (userId) REFERENCES User(userId);
ALTER TABLE ShopCart ADD CONSTRAINT fk_Shop__User FOREIGN KEY (productId) REFERENCES Product(productId);