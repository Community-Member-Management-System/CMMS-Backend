from django.core.management.base import BaseCommand, CommandError
from communities.models import Community
from account.models import User


class Command(BaseCommand):
    help = 'Create test communities'

    def add_arguments(self, parser):
        parser.add_argument('from', type=int)
        parser.add_argument('to', type=int)
        parser.add_argument('user_id', type=int)
        parser.add_argument('valid', type=int)

    def handle(self, *args, **options):
        int_from = options['from']
        int_to = options['to']
        user_id = options['user_id']
        valid = bool(options['valid'])

        for i in range(int_from, int_to + 1):
            sid = f'club{i}'
            Community.objects.create(
                creator=User.objects.get(id=user_id),
                owner=User.objects.get(id=user_id),
                name=sid,
                profile=sid + 'profile',
                valid=valid
            )
            self.stdout.write(
                f'Community (name {sid}) created.'
            )
