# notice

## idea

- [ ] ~~用户登陆/刷新/操作 NoticeBox 时懒更新与其有关的 NoticeBox 表项。~~
- [x] Notice 发生时对 Notice 更新，Notice 更新时更新 NoticeBox，用户读 Notice 时从 NoticeBox 取数据。
- [ ] C_AN 和 S_CA 的 `description` 域的使用方法还有待开发。它们应当至少包含活动页面链接和处理申请的页面的链接。
- [ ] `NoticeBox` 的预期使用方法是这样的：通过 `fetch` 来确定需要给用户展示哪些条目，通过 `read` 来渲染其是否表现为已读，通过 `delete` 来决定它是否被展示给用户。如果需要分类展示条目，可以通过查相关 `Notice` 的属性解决；如果这个需求存在且频繁，应考虑抽象到 `NoticeManager` 里。

## API

### notice.utils.NoticeManager

#### create_notice_PC(related_user, related_community, subtype, date)

创建一个用户 `related_user` 被社团 `related_community` 邀请加入 `subtype = 0` /取消管理员 `subtype = 1` /踢出 `subtype=2` 的通知。

日期默认为创建通知时的时间。

#### create_notice_AR(related_user, related_comment, subtype, date)

创建一个用户 `related_user` 的评论被回复 `subtype = 0` 或用户 `related_user` 被 AT `subtype = 1` 的通知。相关评论域 `related_comment` 为回复者的评论或包含此 AT 的评论。

日期默认为创建通知时的时间。

#### create_notice_CA(related_user, related_community, subtype, description, date)

创建一个用户 `related_user` 创建 `subtype = 0` /加入 `subtype = 1` 社团 `related_community` 结果 `description` 的通知。若创建失败，社团可以为空 `None` 。

日期默认为创建通知时的时间。

#### create_notice_B(related_user, description, date)

创建一个用户 `related_user` 以给定理由 `description` 被封禁的通知。

日期默认为创建通知时的时间。

#### create_notice_C_AN(related_community, description, date)

创建一个社团 `related_community` 活动通知。描述域 `description` 应为此活动的提要。

日期默认为创建通知时的时间。

#### create_notice_C_AP(related_user, related_community, subtype, description, date)

创建一个仅社团 `related_community` 管理员可见的、向用户 `related_user` 发送的邀请被拒绝 `subtype = 0` /与用户 `related_user` 相关的权限变更 `description`  `subtype = 1` /与用户 `related_user` 相关的成员增减 `description`  `subtype = 2` 的通知。

日期默认为创建通知时的时间。

#### create_notice_C_AA(related_user, related_community, description, date)

创建一个仅社团 `related_community` 管理员可见的、用户 `related_user` 申请加入社团的通知。描述域 `description` 为申请理由。

日期默认为创建通知时的时间。

#### create_notice_C_D(related_community, description, date)

创建一个社团 `related_community` 成员可见的、社团被解散的通知。描述域 `description` 为解散理由。

日期默认为创建通知时的时间。

#### create_notice_S_CA(related_user, description, date)

创建一个仅系统管理员可见的，用户 `related_user` 申请创建社团的通知。描述域 `description` 为申请提要。

日期默认为创建通知时的时间。

#### fetch(user)

返回一个 `QuerySet`，包含了属于用户 `user` 的所有 `NoticeBox` 项目。

#### read(notice_box)

将 `NoticeBox` 条目 `notice_box` 置为已读 `read = True`。

#### unread(notice_box)

将 `NoticeBox` 条目 `notice_box` 置为未读 `read = False`。

#### delete(notice_box)

将 `NoticeBox` 条目 `notice_box` 置为已删除 `delete = True`。

## model

### Notice

+ date
+ type

| 值               | 含义                                               |
| ---------------- | -------------------------------------------------- |
| NoticeType.pc   | 被邀请加入社团/取消管理员/被踢出社团          |
| NoticeType.ar   | 评论被 at/回复                                     |
| NoticeType.ca   | 创建/加入社团审核结果                              |
| NoticeType.b    | 用户被封禁                                         |
| NoticeType.c_an   | 社团活动通知                               |
| NoticeType.c_ap | 社团管理员个人邀请被拒绝/社团成员权限变更/成员增减 |
| NoticeType.c_aa | 社团管理员审核用户加入请求                         |
| NoticeType.c_d  | 社团被解散                                         |
| NoticeType.s_ca | 系统管理员审核社团创建请求                         |

+ related_user
+ related_community
+ related_comment
+ subtype
+ description

| 类型 | related_user | related_community | related_comment | subtype | description |
| ---- | ------------ | ----------------- | --------------- | ------- | ----------- |
| pc   | Y            | Y                 | -               | Y       | -           |
| ar   | Y            | -                 | Y               | Y       | -           |
| ca   | Y            | Y/N               | -               | Y       | Y           |
| b    | Y            | -                 | -               | -       | Y           |
| c_an | -            | Y                 | -               | -       | Y           |
| c_ap | Y            | Y                 | -               | Y       | -           |
| c_aa | Y            | Y                 | -               | -       | Y           |
| c_d  | -            | Y                 | -               | -       | Y           |
| s_ca | Y            | -                 | -               | -       | Y           |

| subtype | 0                        | 1                | 2          |
| ------- | ------------------------ | ---------------- | ---------- |
| pc      | 被邀请加入社团           | 取消管理员       | 被踢出社团 |
| ar      | 评论被 at                | 评论被回复       |            |
| ca      | 创建社团审核结果         | 加入社团审核结果 |            |
| c_ap    | 社团管理员个人邀请被拒绝 | 社团成员权限变更 | 成员增减   |

### NoticeBox

+ user
+ notice
+ read
+ deleted

