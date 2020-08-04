# account 模块

## 简介

有两个 Model: 继承自 AbstractBaseUser 的自定义用户类型（**其他所有需要使用 User 的地方都必须使用这个 Model，而非 Django 自带的**），以及和它对应的 UserManager。

## Views

详情见 Swagger `auth`, `users` 和 `token`。

实现了：

- 传统登录（用户名 & 密码），返回 JWT 且设置 session 为登录态
- CAS 登录（需要作为可点击的链接跳转），跳转到 next 参数对应的 URL（如果没有则为 /），将 JWT 放置于 cookie 中且设置 `login=true`，session 设置为登录态
- 注销
- 查看用户公开信息
- 查看当前用户信息、修改当前用户信息
- 更新 JWT，以及验证 JWT 有效性
- 验证当前用户状态

### 关于 Session 和 JWT

目前后端配置支持 Session 和 JWT 验证（两者满足其一即可）。

### TODO

- 不允许从 CAS 使用 GID 登录。（CAS 测试服务器上的测试用户似乎 GID 和正式的服务器规则不一样，可能需要到最后再改）
- ~~用户信息可见性相关设置（比较复杂）~~

## Permissions

实现了 `ValidUserPermission`（所有接口默认的权限要求），`ValidUserOrReadOnlyPermission` 和 `IsSuperUser`。

如果某个接口是所有人可使用的，设置：

```python
permission_classes: Sequence[Type[BasePermission]] = []
```
