create database CMMS character set utf8mb4;
create user 'cmms'@'localhost' identified by 'cmms';
GRANT ALL ON CMMS.* to 'cmms'@'localhost';
GRANT ALL ON CMMS_test.* to 'cmms'@'localhost';
