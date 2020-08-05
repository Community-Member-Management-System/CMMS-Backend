# CMMS-Backend

![Django CI](https://github.com/Community-Member-Management-System/CMMS-Backend/workflows/Django%20CI/badge.svg)

2019-2020 春季学期科大软件工程项目「社团成员管理系统」后端部分。

## Configuring Database

```mysql
create database CMMS character set utf8mb4;
create user 'cmms'@'localhost' identified by 'cmms';
GRANT ALL ON CMMS.* to 'cmms'@'localhost';
GRANT ALL ON CMMS_test.* to 'cmms'@'localhost';
```

```shell script
python manage.py migrate
python manage.py createsuperuser
python manage.py set_user <superusername> <nickname> <realname>
```

## Other Management Commands

```shell script
python manage.py set_community <community_id>  # make a community valid
python manage.py create_user <from> <to> <valid>  # create users from 'test{from}' to 'test{to}', set valid to 0 if invalid
python manage.py create_community <from> <to> <user_id> <valid>  # create communities from 'test{from}' to 'test{to}' with owner as user_id, set valid to 0 if invalid
```
