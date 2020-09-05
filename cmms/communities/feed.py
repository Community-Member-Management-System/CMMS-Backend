from django.conf import settings
from django.shortcuts import get_object_or_404
from django_ical.views import ICalFeed
from activity.models import Activity
from django.db.models.query import QuerySet
from django.contrib.syndication.views import Feed

from communities.models import Community


class FeedConfig:
    def get_object(self, request, *args, **kwargs):
        return get_object_or_404(Community, pk=int(kwargs['pk']))

    def items(self, community_id: int) -> 'QuerySet[Activity]':
        return Activity.objects.filter(related_community=community_id).order_by('-start_time')

    def item_title(self, item: Activity):
        return item.title

    def item_description(self, item: Activity):
        return item.description

    def item_start_datetime(self, item: Activity):
        return item.start_time

    def item_end_datetime(self, item: Activity):
        return item.end_time

    def item_created(self, item: Activity):
        return item.created_date

    def item_link(self, item: Activity):
        # fixme: after frontend finishes, the actual link shall be updated here
        return f'#/tourist/activity/{item.id}'

    def item_location(self, item: Activity):
        return item.location


class CommunityEventCalendarFeed(FeedConfig, ICalFeed):
    product_id = '-//CMMS/Activity/CN'
    timezone = 'Asia/Shanghai'
    file_name = 'feed.ics'


class CommunityEventRSSFeed(FeedConfig, Feed):  # type: ignore
    # mypy is somewhat stupid here...
    language = 'zh-cn'

    def title(self, item: Community):
        return f"社团 {item.name} 的活动 RSS"

    def link(self, item: Community):
        return f'#/tourist/activity/{item.id}'  # fixme
