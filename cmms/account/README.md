# account 模块

## 简介

有两个 Model: 继承自 AbstractBaseUser 的自定义用户类型（**其他所有需要使用 User 的地方都必须使用这个 Model，而非 Django 自带的**），以及和它对应的 UserManager。

Views: 实现了

- 传统登录（用户名 & 密码）
- CAS 登录
- 注销
- 查看用户公开信息
- 查看当前用户信息、修改当前用户信息。

TODO:

- 不允许从 CAS 使用 GID 登录。
- 用户信息可见性相关设置（比较复杂）

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
| new | 是否为（未补全信息的）新用户。仅在登录成功时有此字段。 |

登录成功时，返回 HTTP 200，否则为 HTTP 401。

## CAS 登录

`GET /api/auth/cas_login`

302 至 CAS 服务，进行下一步操作。

验证成功：302 到 `/login=true&new=<是否为新用户>`，前端据此进一步操作。

验证失败：返回 401，提示用户返回主页。（前端不需要处理这种情况。）

## 注销

`POST /api/auth/logout`

无输入。

输出：

| 字段 | 备注 |
| -- | -- |
| msg | 输出的信息。 |

总是成功（即使没有登录）。

## 查看用户公开信息

`GET /api/users/public/`

详见 Browsable API 页面。

## 查看、修改自己的信息

`GET/PUT/PATCH /api/users/current`

详见 Browsable API 页面。
