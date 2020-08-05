CREATE DATABASE CMMS CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'cmms'@'localhost' IDENTIFIED BY 'cmms';
GRANT ALL PRIVILEGES ON CMMS.* to 'cmms'@'localhost';
GRANT ALL PRIVILEGES ON CMMS_test.* to 'cmms'@'localhost';
