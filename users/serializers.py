from rest_framework import serializers, viewsets
from rest_auth.serializers import LoginSerializer as RestAuthLoginSerializer
from .models import User, UserProfile


class LoginSerializer(RestAuthLoginSerializer):
    username = None


class UserSerializer(serializers.HyperlinkedModelSerializer):
    # profile_url = serializers.HyperlinkedIdentityField(view_name='profile-detail', source='profile')
    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'email')


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    id = serializers.IntegerField(source='pk', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    admin = serializers.CharField(source='user.is_superuser')

    class Meta:
        model = UserProfile
        fields = '__all__'

    def get_full_name(self, obj):
        request = self.context['request']
        return request.user.get_full_name()

    def update(self, instance, validated_data):
        # retrieve the User
        user_data = validated_data.pop('user', None)
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)

        # retrieve Profile
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.user.save()
        instance.save()
        return instance

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()