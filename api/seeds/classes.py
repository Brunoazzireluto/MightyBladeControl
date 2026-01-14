from core.models import CharacterClass, ClassAvailableAbility, Ability
from .utils import get_json_data, parse_attributes, strip_html_tags


def run():
    print("Seeding Classes...")

    data = get_json_data("classes.json")

    if not data or "classe" not in data:
        print("No class data found.")
        return

    for item in data["classe"]:
        name = item.get("n")
        if not name:
            continue

        print(f"Processing Class: {name}")

        attrs = parse_attributes(item.get("a"))

        defaults = {
            "description": strip_html_tags(item.get("d", "")),
            "bonus_str": attrs["strength"],
            "bonus_agi": attrs["agility"],
            "bonus_int": attrs["intelligence"],
            "bonus_wil": attrs["will"],
        }

        class_obj, created = CharacterClass.objects.update_or_create(
            name=name, defaults=defaults
        )

        # Available Abilities
        # We combine 'h' (list) and 'ha' (single string) into the available pool
        abilities_to_link = set(item.get("h", []))

        if item.get("ha"):
            abilities_to_link.add(item.get("ha"))

        # Clear existing? Or just add?
        # Ideally, we should sync. But `update_or_create` on Class doesn't clear M2M.
        # Since this is a seeder, maybe we shouldn't wipe everything to avoid data loss if manually edited.
        # But usually seeders ensure state.
        # Let's just add missing ones for now to be safe.

        for ability_name in abilities_to_link:
            try:
                ab = Ability.objects.filter(name__iexact=ability_name).first()
                if ab:
                    ClassAvailableAbility.objects.get_or_create(
                        character_class=class_obj, ability=ab
                    )
                else:
                    print(
                        f"Warning: Class Ability '{ability_name}' not found for {name}"
                    )
            except Exception as e:
                print(f"Error linking class ability: {e}")
