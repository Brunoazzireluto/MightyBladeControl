from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Race,
    RaceLore,
    CharacterClass,
    Ability,
    Background,
    Language,
    Creature,
    SpiritAnimal,
    Material,
    ItemQuality,
    Item,
    Weapon,
    Armor,
)


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "password", "email", "first_name", "last_name")

    def create(self, validated_data):
        # create_user garante o hash da senha
        return User.objects.create_user(**validated_data)


class AbilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ability
        fields = "__all__"


class RaceLoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = RaceLore
        fields = ["naming_rules_html", "male_names", "female_names"]


class RaceSerializer(serializers.ModelSerializer):
    lore = RaceLoreSerializer(read_only=True)

    class Meta:
        model = Race
        fields = "__all__"


class CharacterClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterClass
        fields = "__all__"


class BackgroundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Background
        fields = "__all__"


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = "__all__"


class CreatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creature
        fields = "__all__"


class SpiritAnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpiritAnimal
        fields = "__all__"


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = "__all__"


class ItemQualitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemQuality
        fields = "__all__"


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"


class WeaponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weapon
        fields = "__all__"


class ArmorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Armor
        fields = "__all__"
