from django.core.management.base import BaseCommand, CommandError
from communities.models import Community


class Command(BaseCommand):
    help = 'Make a community valid'

    def add_arguments(self, parser):
        parser.add_argument('community_id', type=str)

    def handle(self, *args, **options):
        community_id = options['community_id']

        try:
            community = Community.objects.get(id=community_id)
        except Community.DoesNotExist:
            raise CommandError(f'Community with id {community_id} does not exist.')

        community.valid = True
        community.save()

        self.stdout.write(
            f'Community {community_id} is valid now.'
        )
