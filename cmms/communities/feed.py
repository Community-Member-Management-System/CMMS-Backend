from django_ical.views import ICalFeed
from activity.models import Activity
from django.db.models.query import QuerySet


class CommunityEventCalendarFeed(ICalFeed):
    product_id = '-//cmms/Activity/CN'
    timezone = 'Asia/Shanghai'
    file_name = 'feed.ics'

    def get_object(self, request, *args, **kwargs):
        return int(kwargs['pk'])

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
        return f'/community/{item.id}/activities'

    def item_location(self, item: Activity):
        return item.location
