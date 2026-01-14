from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from .models import (
    Race,
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
from .serializers import (
    UserSerializer,
    RaceSerializer,
    CharacterClassSerializer,
    AbilitySerializer,
    BackgroundSerializer,
    LanguageSerializer,
    CreatureSerializer,
    SpiritAnimalSerializer,
    MaterialSerializer,
    ItemQualitySerializer,
    ItemSerializer,
    WeaponSerializer,
    ArmorSerializer,
)


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class AbilityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ability.objects.all()
    serializer_class = AbilitySerializer
    permission_classes = [AllowAny]


class RaceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Race.objects.all()
    serializer_class = RaceSerializer
    permission_classes = [AllowAny]


class CharacterClassViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CharacterClass.objects.all()
    serializer_class = CharacterClassSerializer
    permission_classes = [AllowAny]


class BackgroundViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Background.objects.all()
    serializer_class = BackgroundSerializer
    permission_classes = [AllowAny]


class LanguageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = [AllowAny]


class CreatureViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Creature.objects.all()
    serializer_class = CreatureSerializer
    permission_classes = [AllowAny]


class SpiritAnimalViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SpiritAnimal.objects.all()
    serializer_class = SpiritAnimalSerializer
    permission_classes = [AllowAny]


class MaterialViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    permission_classes = [AllowAny]


class ItemQualityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ItemQuality.objects.all()
    serializer_class = ItemQualitySerializer
    permission_classes = [AllowAny]


class ItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [AllowAny]


class WeaponViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Weapon.objects.all()
    serializer_class = WeaponSerializer
    permission_classes = [AllowAny]


class ArmorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Armor.objects.all()
    serializer_class = ArmorSerializer
    permission_classes = [AllowAny]
