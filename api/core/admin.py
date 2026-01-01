from django.contrib import admin
from .models import (
    Race,
    RaceLore,
    CharacterClass,
    Background,
    Ability,
    Item,
    Weapon,
    Armor,
    Consumable,
    Material,
    ItemQuality,
    Character,
    CharacterItem,
    Creature,
)

# --- INLINES (Para ver itens dentro da ficha) ---


class CharacterItemInline(admin.TabularInline):
    model = CharacterItem
    extra = 0
    raw_id_fields = ("item",)  # Para não carregar mil itens no dropdown


class RaceLoreInline(admin.StackedInline):
    model = RaceLore
    can_delete = False


# --- CONFIGURAÇÃO DOS MODELS ---


@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ("name", "initial_str", "initial_agi", "initial_int", "initial_wil")
    search_fields = ("name",)
    inlines = [RaceLoreInline]


@admin.register(CharacterClass)
class CharacterClassAdmin(admin.ModelAdmin):
    list_display = ("name", "bonus_str", "bonus_agi", "bonus_int", "bonus_wil")
    search_fields = ("name",)


@admin.register(Ability)
class AbilityAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "mana_cost", "difficulty")
    list_filter = ("category",)
    search_fields = ("name", "description")


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "user",
        "race",
        "character_class",
        "level",
        "current_load_display",
    )
    list_filter = ("race", "character_class", "level")
    search_fields = ("name", "user__username")
    inlines = [CharacterItemInline]

    def current_load_display(self, obj):
        return f"{obj.current_load} / {obj.max_load} kg"

    current_load_display.short_description = "Carga"


# --- INVENTÁRIO ---


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("name", "item_type", "price", "weight")
    list_filter = ("item_type",)
    search_fields = ("name",)


@admin.register(Weapon)
class WeaponAdmin(admin.ModelAdmin):
    list_display = ("name", "damage", "damage_type", "grip", "price")
    list_filter = ("damage_type", "grip")


@admin.register(Armor)
class ArmorAdmin(admin.ModelAdmin):
    list_display = ("name", "defense_bonus", "penalty", "is_heavy")


@admin.register(Consumable)
class ConsumableAdmin(admin.ModelAdmin):
    list_display = ("name", "rarity", "charges")


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price_multiplier", "damage_bonus")


@admin.register(Creature)
class CreatureAdmin(admin.ModelAdmin):
    list_display = ("name", "creature_type", "hp", "defense")
    search_fields = ("name",)


# Registros simples
admin.site.register(Background)
admin.site.register(ItemQuality)
