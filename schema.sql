-- 1. Drop existing tables if you are resetting the database
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS menu;
DROP TABLE IF EXISTS orders;

-- 2. Create the Users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
);

-- 3. Create the Menu table
CREATE TABLE menu (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    category TEXT,
    price REAL
);

-- 4. Create the Orders table (THIS WAS MISSING!)
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    items TEXT,
    total REAL,
    status TEXT DEFAULT 'Pending'
);

-- 5. Insert the default student login
INSERT INTO users (username, password) VALUES ('student', 'campus123');

-- 6. Insert the 38 Campus Canteen Menu Items
INSERT INTO menu (name, category, price) VALUES 
('Idli (2 pcs)', 'Breakfast', 30), 
('Vada', 'Breakfast', 15), 
('Masala Dosa', 'Breakfast', 50),
('Set Dosa', 'Breakfast', 45), 
('Chow Chow Bath', 'Breakfast', 40), 
('Bisi Bele Bath', 'Breakfast', 45),
('Filter Coffee', 'Beverages', 15), 
('Tea', 'Beverages', 12), 
('Lemon Tea', 'Beverages', 15),
('Samosa', 'Snacks', 15), 
('Veg Puff', 'Snacks', 20), 
('Egg Puff', 'Snacks', 25),
('Chicken Puff', 'Snacks', 35), 
('Veg Fried Rice', 'Main Course', 70), 
('Egg Fried Rice', 'Main Course', 80),
('Chicken Fried Rice', 'Main Course', 100), 
('Gobi Manchurian', 'Snacks', 60), 
('Paneer Manchurian', 'Snacks', 80),
('Tandoori Roti', 'Main Course', 20), 
('Butter Naan', 'Main Course', 35), 
('Paneer Butter Masala', 'Main Course', 120),
('Chicken Curry', 'Main Course', 140), 
('South Indian Meals', 'Main Course', 80), 
('North Indian Thali', 'Main Course', 100),
('Maggi Noodles', 'Snacks', 30), 
('Cheese Maggi', 'Snacks', 45), 
('Bread Omelette', 'Snacks', 40),
('Cold Coffee', 'Beverages', 50), 
('Fresh Lime Soda', 'Beverages', 30), 
('Mango Milkshake', 'Beverages', 60),
('Oreo Shake', 'Beverages', 70), 
('Vanilla Ice Cream', 'Desserts', 30), 
('Chocolate Ice Cream', 'Desserts', 40),
('Gulab Jamun (2 pcs)', 'Desserts', 30), 
('Masala Puri', 'Chaat', 40), 
('Pani Puri', 'Chaat', 35),
('Bhel Puri', 'Chaat', 40), 
('Veg Grilled Sandwich', 'Snacks', 50);