from core.models import Creature
from .utils import get_json_data, parse_attributes, strip_html_tags
from django.utils.text import slugify


def run():
    print("Seeding Creatures (Animals)...")

    data = get_json_data("animais.json")

    if not data or "animais" not in data:
        print("No creature data found.")
        return

    count_created = 0
    count_updated = 0

    for item in data["animais"]:
        name = item.get("n")
        if not name:
            continue

        attrs = parse_attributes(item.get("a"))

        # Build description with extra info
        extra_info = []
        if item.get("hb"):
            extra_info.append(f"Habitat: {item.get('hb')}")
        if item.get("di"):
            extra_info.append(f"Dieta: {item.get('di')}")
        if item.get("o"):
            extra_info.append(f"Organização: {item.get('o')}")
        if item.get("tm"):
            extra_info.append(f"Tamanho Físico: {item.get('tm')}")

        description = strip_html_tags("\n".join(extra_info))

        defaults = {
            "creature_type": item.get("c", ""),
            "size": item.get("md", ""),
            "strength": attrs["strength"],
            "agility": attrs["agility"],
            "intelligence": attrs["intelligence"],
            "will": attrs["will"],
            "hp": item.get("v", 10),
            "mana": item.get("m", 0),
            "defense": item.get("d", 0),
            "attacks_data": item.get("at", []),
            "abilities_data": item.get("ha", []),
            "description": description,
        }

        # We manually handle slug if needed, but model save does it.
        # However, update_or_create by name is safer for seeds.
        obj, created = Creature.objects.update_or_create(name=name, defaults=defaults)

        if created:
            count_created += 1
        else:
            count_updated += 1

    print(f"Creatures: {count_created} created, {count_updated} updated.")
