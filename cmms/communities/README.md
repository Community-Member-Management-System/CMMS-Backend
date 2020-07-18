# communities 模块

## 简介

Model:

- Community: 定义了社团在数据库中的相关信息。
- Membership: 记录社团-成员多对多关系的中间表。

Views: 实现了

- 列出所有社团的信息。
- 创建社团。
- 转移社团所有者。
- 修改社团名与社团简介。
- 删除社团。
- 加入与退出社团。
- 管理员审核加入社团的列表。

TODO:

- 创建社团审核
- 文档中明确每个操作要求的权限


## 列出所有社团

`GET /api/community/`

详见 Browsable API 页面。

## 创建新社团

`POST /api/community/`

详见 Browsable API 页面。

## 转移社团所有者

`PUT /api/community/<int:pk>/transfer`

`<int:pk>` 为社团 ID。详见 Browsable API 页面。

## 修改社团名和社团简介

`GET /api/community/<int:pk>`

查看社团名和社团简介。

`PUT /api/community/<int:pk>`

修改社团名和社团简介。详见 Browsable API 页面。

## 删除社团

`DELETE /api/community/<int:pk>/delete`

删除社团。

## 加入与退出社团

`POST /api/community/<int:pk>/join`

发送内容中如果 `join=true`，加入社团；否则如果 `join=false`，退出社团。

## 待审核加入社团列表查询

`GET /api/community/<int:pk>/audit`

返回结果类似于：

```
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "invalid_members": [
        {
            "id": 1,
            "real_name": "11",
            "nick_name": "11"
        }
    ]
}
```

## 审核通过/不通过操作

`POST /api/community/<int:pk>/audit/<int:user_id>/<str:action>`

user_id 为待审核列表中某个用户的 ID，action 为 allow 或者 deny。
