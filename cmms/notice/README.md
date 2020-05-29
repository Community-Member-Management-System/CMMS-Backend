# notice

## model

### Notice

+ date
+ type

| 值               | 含义                                               | 内容      |
| ---------------- | -------------------------------------------------- | --------- |
| notice_type_pc   | 被邀请加入社团/取消管理员/kick/解散                | NoticePC  |
| notice_type_ar   | 评论被 at/回复                                     | NoticeAR  |
| notice_type_ca   | 创建/加入社团审核结果                              | NoticeCA  |
| notice_type_b    | 用户被封禁                                         | NoticeB   |
| notice_type_c_an   | 社团活动通知                               | NoticeCAN  |
| notice_type_c_ap | 社团管理员个人邀请被拒绝/社团成员权限变更/成员增减 | NoticeCAP |
| notice_type_c_aa | 社团管理员审核用户加入请求                         | NoticeCAA |
| notice_type_c_d  | 社团被解散                                         | NoticeCD  |
| notice_type_s_ca | 系统管理员审核社团创建请求                         | NoticeSCA |

+ content

### NoticePC

+ notice
+ receiver
+ community

### NoticeAR

+ notice
+ receiver
+ comment

### NoticeCA

+ notice
+ receiver
+ access

### NoticeB

+ notice
+ receiver
+ reason

### NoticeCAN

+ notice
+ related_community
+ description

### NoticeCAP

+ notice
+ related_community
+ related_user

### NoticeCAA

+ notice
+ related_community
+ related_user

### NoticeCD

+ notice
+ related_community

### NoticeSCA

+ notice
+ related_community