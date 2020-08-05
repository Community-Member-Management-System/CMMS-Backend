from django.core.management.base import BaseCommand, CommandError
from account.models import User
from account.utils import is_new_user


class Command(BaseCommand):
    help = 'Set user nickname and realname (make it valid)'

    def add_arguments(self, parser):
        parser.add_argument('student_id', type=str)
        parser.add_argument('nickname', type=str)
        parser.add_argument('realname', type=str)

    def handle(self, *args, **options):
        student_id = options['student_id']
        nickname = options['nickname']
        realname = options['realname']

        try:
            user = User.objects.get(student_id=student_id)
        except User.DoesNotExist:
            raise CommandError(f'User with student id {student_id} does not exist.')

        user.nick_name = nickname
        user.real_name = realname
        user.save()

        assert not is_new_user(user)

        self.stdout.write(
            f'User {student_id} now has nick name {nickname} and real name {realname}, it shall be valid.'
        )
