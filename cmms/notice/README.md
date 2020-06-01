# notice

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
| ca   | Y            | Y/N               | -               | Y       | -           |
| b    | Y            | -                 | -               | -       | Y           |
| c_an | -            | Y                 | -               | -       | Y           |
| c_ap | Y            | Y                 | -               | Y       | -           |
| c_aa | Y            | Y                 | -               | -       | Y           |
| c_d  | -            | Y                 | -               | -       | Y           |
| s_ca | Y            | -                 | -               | -       | -           |

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

