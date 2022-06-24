from rest_framework import serializers
from django.contrib.auth import get_user_model
from .utils import normalize_phone
from .task import send_activation_sms


User = get_user_model()
#
# class RegistrationSerializer(serializers.Serializer):
#     nickname =


class RegistrationSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(max_length=100, required=True)
    class Meta:
        model = User
        fields = ('nickname', "phone", "password", "password_confirm")


    def validate_nickname(self, nickname):
        if User.objects.filter(nickname=nickname).exists():
            raise serializers.ValidationError('This is already taken. Please choose another one')
        return nickname

    def validate_phone(self, phone):
        phone = normalize_phone(phone)
        print(phone, 'asdfjlkasgdkflgkasdlf')
        if len(phone) != 13:
            raise serializers.ValidationError('Invalid phone format')
        if User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError('Phone alredy exists')
        return phone


    def validate(self, attrs: dict):
        print(attrs)
        password1 = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')
        if not any(i for i in password1 if i.isdigit()):
            raise serializers.ValidationError('Password. nust contain at least one degit!')
        if password1 != password_confirm:
            raise serializers.ValidationError('Passwords do not match')
        return attrs

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(**validated_data)
        user.create_activation_code()
        send_activation_sms.delay(user.phone, user.activation_code)
        return user