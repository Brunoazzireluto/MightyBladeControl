from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserRegisterView,
    AbilityViewSet,
    RaceViewSet,
    CharacterClassViewSet,
    BackgroundViewSet,
    LanguageViewSet,
    CreatureViewSet,
    SpiritAnimalViewSet,
    MaterialViewSet,
    ItemQualityViewSet,
    ItemViewSet,
    WeaponViewSet,
    ArmorViewSet,
)

router = DefaultRouter()
router.register(r"abilities", AbilityViewSet)
router.register(r"races", RaceViewSet)
router.register(r"classes", CharacterClassViewSet)
router.register(r"backgrounds", BackgroundViewSet)
router.register(r"languages", LanguageViewSet)
router.register(r"creatures", CreatureViewSet)
router.register(r"spirit-animals", SpiritAnimalViewSet)
router.register(r"materials", MaterialViewSet)
router.register(r"qualities", ItemQualityViewSet)
router.register(r"items", ItemViewSet)
router.register(r"weapons", WeaponViewSet)
router.register(r"armors", ArmorViewSet)

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register-user"),
    path("", include(router.urls)),
]


# precisa verificar as armas, acho que todas estão como is_stackable sendo que a maioria deve ser falsa, apenas facas de arremeso e coisas assim
# preciso verificar as armaduras
# precisa atualizar o md para ter como rodar as seeds
