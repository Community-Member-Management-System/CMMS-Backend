from django.core.management.base import BaseCommand
from account.models import User


class Command(BaseCommand):
    help = 'Create test users'

    def add_arguments(self, parser):
        parser.add_argument('from', type=int)
        parser.add_argument('to', type=int)
        parser.add_argument('valid', type=int)

    def handle(self, *args, **options):
        int_from = options['from']
        int_to = options['to']
        valid = options['valid']

        for i in range(int_from, int_to + 1):
            sid = f'test{i}'
            if valid > 0:
                nickname = sid
                realname = sid
            else:
                nickname = None
                realname = None
            User.objects.create_user(
                gid=f'{i}',
                student_id=sid,
                password=sid,
                nick_name=nickname,
                real_name=realname,
            )
            self.stdout.write(
                f'User {i} (username {sid}, password {sid}) created.'
            )
