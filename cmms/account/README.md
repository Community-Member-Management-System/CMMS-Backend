# account 模块

## 简介

有两个 Model: 继承自 AbstractBaseUser 的自定义用户类型（**其他所有需要使用 User 的地方都必须使用这个 Model，而非 Django 自带的**），以及和它对应的 UserManager。

Views: 实现了

- 传统登录（用户名 & 密码）
- CAS 登录
- 注销

## 传统登录

`POST /api/auth/traditional_login`

输入:

| 字段 | 备注 |
| -- | -- |
| username | 用户名。不能为空。 |
| password | 密码。不能为空。 |

输出：

| 字段 | 备注 |
| -- | -- |
| msg | 输出的信息。 |

登录成功时，返回 HTTP 200，否则为 HTTP 401。

## CAS 登录

`GET /api/auth/cas_login`

302 至 CAS 服务，进行下一步操作。

// TODO: 需要确认验证成功/失败后的操作。

## 注销

`POST /api/auth/logout`

无输入。

输出：

| 字段 | 备注 |
| -- | -- |
| msg | 输出的信息。 |

总是成功（即使没有登录）。
