from rest_framework.serializers import ModelSerializer, BooleanField, Serializer, SerializerMethodField
from rest_framework.exceptions import ValidationError

from django.db.models.query import QuerySet

from account.models import User
from .models import Community, Invitation


class CommunitySerializer(ModelSerializer):
    members = SerializerMethodField()

    def get_members(self, community):
        valid_members = community.members.filter(membership__valid=True)
        serializer = MemberSerializer(instance=valid_members,
                                      context={
                                          'community': community,
                                          'admin': community.is_admin(self.context.get('user'))
                                      }, many=True)
        return serializer.data

    class Meta:
        model = Community
        fields = '__all__'
        read_only_fields = ['creator', 'owner', 'date_created', 'members', 'admins', 'valid']


class OwnershipTransferSerializer(ModelSerializer):
    def validate_owner(self, value):
        if value not in self.instance.membership_set.all():
            raise ValidationError('Specified user is not a member of the community')

    class Meta:
        model = Community
        fields = ['owner']


class CommunitySimpleSerializer(ModelSerializer):
    class Meta:
        model = Community
        fields = ('id', 'name', 'profile', 'avatar')


class CommunityJoinSerializer(Serializer):
    join = BooleanField(label='加入', required=True, read_only=False)


class MemberSerializer(ModelSerializer):
    role = SerializerMethodField()
    real_name = SerializerMethodField()

    def get_role(self, user):
        community = self.context['community']
        owner = community.owner
        if user == owner:
            return 'owner'
        if community.is_admin(user):
            return 'admin'

        return None

    def get_real_name(self, user):
        # for user's privacy
        if self.context.get('admin') is True:
            return user.real_name
        else:
            return None

    class Meta:
        model = User
        fields = ('id', 'real_name', 'nick_name', 'avatar', 'profile', 'role')


class CommunityNewMemberAuditSerializer(ModelSerializer):
    invalid_members = SerializerMethodField()

    def get_invalid_members(self, community):
        # fixme: dup code
        invalid_list = community.members.filter(membership__valid=False)
        serializer = MemberSerializer(instance=invalid_list, context={'community': community, 'admin': True}, many=True)
        return serializer.data

    class Meta:
        model = Community
        fields = ('invalid_members',)


class CommunitySysAdminAuditSerializer(ModelSerializer):
    class Meta:
        model = Community
        fields = ('valid', 'name', 'profile', 'owner', 'avatar', 'pk')
        read_only_fields = ('name', 'profile', 'owner', 'avatar')


def get_community_non_members_list(community) -> 'QuerySet[User]':
    users = User.objects.all()
    members = community.members.all()
    return users.difference(members)


class CommunityInviteSerializer(ModelSerializer):
    non_members = SerializerMethodField()

    def get_non_members(self, community):
        non_members_list = get_community_non_members_list(community)
        serializer = MemberSerializer(instance=non_members_list, context={'community': community}, many=True)
        return serializer.data

    class Meta:
        model = Community
        fields = ('non_members',)


class CommunityInvitationSerializer(ModelSerializer):
    class Meta:
        model = Invitation
        fields = '__all__'
        read_only_fields = ('user', 'community')
