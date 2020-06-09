# activity

## idea

## API

### activity.utils.ActivityManager

#### create_activity

receive `related_community`, `location`, `title`, `description`, `start_time`, `end_time`, `created_date` (which default timezone.now), return a newly created activity.

#### get_activity_by_community

receive `community`, return a queryset of activities whose `related_commnunity` == `community`.

#### create_comment

receive `related_activity`, `related_user`, `title`, `content`, `date` (which default timezone.now), return a newly created comment.

#### get_comment_by_activity

receive `activity`, return a queryset of comments whose `related_activity` == `activity`.

#### get_comment_by_user

receive `user`, return a queryset of comments whose `related_user` == `user`.

## model

### Activity

+ related_community
+ created_date
+ location
+ title
+ description
+ start_time
+ end_time
+ signed_in_users

### Comment

+ related_activity
+ related_user
+ date
+ title
+ content
