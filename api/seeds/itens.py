from core.models import Item, Weapon, Armor, Consumable
from .utils import get_json_data, strip_html_tags


def run():
    print("Seeding Items...")

    count_created = 0
    count_updated = 0

    # 1. Weapons (arma.json)
    arma_data = get_json_data("arma.json")
    if arma_data and "arma" in arma_data:
        for item in arma_data["arma"]:
            name = item.get("n")
            if not name:
                continue

            defaults = {
                "description": strip_html_tags(item.get("de", "")),
                "weight": item.get("p", 0),
                "price": item.get("c", 0),
                "item_type": "weapon",
                "damage": item.get("d", 0),
                "damage_type": str(
                    item.get("t", "")
                ),  # 't' is damage type index/id in some cases?
                "grip": item.get(
                    "a", ""
                ),  # 'a' is Alcance/Grip? (e.g. "Corpo-a-corpo")
                "min_strength": (
                    max(item.get("fn", 0), item.get("fn2m", 0))
                    if (item.get("fn", 0) > 0 or item.get("fn2m", 0) > 0)
                    else 0
                ),
                "defense_bonus": item.get(
                    "dm", False
                ),  # 'dm' seems to be defense bonus flag
                "is_throwable": item.get("ar", False),  # 'ar' flag for Arremesso?
                "is_stackable": item.get(
                    "ar", False
                ),  # Throwable weapons like daggers are stackable
            }

            obj, created = Weapon.objects.update_or_create(name=name, defaults=defaults)
            if created:
                count_created += 1
            else:
                count_updated += 1

    # 2. Armor (defesa.json)
    def_data = get_json_data("defesa.json")
    if def_data and "defesa" in def_data:
        for item in def_data["defesa"]:
            name = item.get("n")
            if not name:
                continue

            defaults = {
                "description": strip_html_tags(item.get("de", "")),
                "weight": item.get("p", 0),
                "price": item.get("c", 0),
                "item_type": "armor",
                "defense_bonus": item.get("d", 0),
                "penalty": item.get(
                    "fn", 0
                ),  # 'fn' here is often penalty or min strength. Usually for armor its "carga" or penalty.
                "is_heavy": item.get(
                    "pe", False
                ),  # 'pe' Peso? In defesa.json, 'pe' is boolean.
                "is_stackable": False,
            }

            obj, created = Armor.objects.update_or_create(name=name, defaults=defaults)
            if created:
                count_created += 1
            else:
                count_updated += 1

    # 3. Consumables (pocao.json)
    pocao_data = get_json_data("pocao.json")
    if pocao_data and "pocao" in pocao_data:
        for item in pocao_data["pocao"]:
            name = item.get("n")
            if not name:
                continue

            obj, created = Consumable.objects.update_or_create(
                name=name,
                defaults={
                    "description": strip_html_tags(item.get("d", "")),
                    "weight": item.get("p", 0.1),
                    "price": item.get("c", 0),
                    "item_type": "consumable",
                    "rarity": item.get("r", "comum"),
                    "is_stackable": True,
                },
            )
            if created:
                count_created += 1
            else:
                count_updated += 1

    # 4. General Gear (mundano.json)
    mundano_data = get_json_data("mundano.json")
    if mundano_data and "mundano" in mundano_data:
        for item in mundano_data["mundano"]:
            name = item.get("n")
            if not name:
                continue

            obj, created = Item.objects.update_or_create(
                name=name,
                item_type="gear",  # Mundane are gear
                defaults={
                    "description": strip_html_tags(item.get("de", "")),
                    "weight": item.get("p", 0),
                    "price": item.get("c", 0),
                    "is_stackable": item.get("q", True),  # 'q' stackable?
                },
            )
            if created:
                count_created += 1
            else:
                count_updated += 1

    print(f"Items/Gear: {count_created} created, {count_updated} updated.")
