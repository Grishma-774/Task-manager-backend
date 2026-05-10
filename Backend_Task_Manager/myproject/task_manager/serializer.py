
from rest_framework import serializers
from django.contrib.auth.models import User
from task_manager.models import Task,Notification


class RegisterSerializer(serializers.ModelSerializer):

    confirm_pass = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "confirm_pass"]

        extra_kwargs = {
            "password": {"write_only": True}
        }

    def validate(self, data):
        password = data.get("password")
        confirm_password = data.get("confirm_pass")

        if not password:
            raise serializers.ValidationError("Password is required")

        if len(password) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters")

        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match")

        return data

    def create(self, validated_data):
        validated_data.pop("confirm_pass")

        user = User(
            username=validated_data["username"],  # ✅ correct
            email=validated_data["email"]
        )

        user.set_password(validated_data["password"])
        user.save()

        return user



class Task_Serializer(serializers.ModelSerializer):

    class Meta:

        model= Task

        fields= ["id","title","description","priority","status","due_date","created_at","updated_at"]

    def validate(self, data):
        
        errors = {}

        if not data.get("title"):
            errors["title"] = "title is required"

        if not data.get("description"):
            errors["description"] = "description is required"

        if not data.get("due_date"):
            errors["due_date"] = "due_date is required"

        if errors:
            raise serializers.ValidationError(errors)

        return data


class Notification_Serializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields="__all__"




