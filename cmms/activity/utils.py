from .models import Activity, Comment
from django.conf import settings
from django.utils import timezone


class ActivityManager:
    __user_manager = settings.AUTH_USER_MODEL.objects
    __community_manager = settings.COMMUNITY_MODEL.objects
    __notice_manager = settings.NOTICE_MODEL.objects
    __notice_box_manager = settings.NOTICE_BOX_MODEL.objects
    __activity_manager = Activity.objects
    __comment_manager = Comment.objects

    # Activity API
    def create_activity(self,
                        related_community,
                        location,
                        title,
                        description,
                        start_time,
                        end_time,
                        created_date=timezone.now):
        new_activity = self.__activity_manager.create(related_community,
                                                      created_date, location,
                                                      title, description,
                                                      start_time, end_time)
        return new_activity

    def get_activity_by_community(self, community):
        return self.__activity_manager.filter(related_community=community)

    # Comment API
    def create_comment(self, related_activity, related_user, title, content, date=timezone.now):
        return self.__comment_manager.create(related_activity, related_user, date, title, content)

    def get_comment_by_activity(self, activity):
        return self.__comment_manager.filter(related_activity=activity)

    def get_comment_by_user(self, user):
        return self.__comment_manager.filter(related_user=user)
