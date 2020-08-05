from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

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

        user = User.objects.get(id=user_id)

        for i in range(int_from, int_to + 1):
            sid = f'club{i}'
            with transaction.atomic():
                c = Community.objects.create(
                    creator=user,
                    owner=user,
                    name=sid,
                    profile=sid + 'profile',
                    valid=valid
                )
                c.admins.add(user)
                c.members.add(user, through_defaults={'valid': True})
            self.stdout.write(
                f'Community (name {sid}) created.'
            )
