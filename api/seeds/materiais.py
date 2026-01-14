from core.models import Material, ItemQuality
from .utils import get_json_data


def run():
    print("Seeding Materials and Qualities...")

    count_created = 0
    count_updated = 0

    # 1. Materials (material.json)
    mat_data = get_json_data("material.json")
    if mat_data and "material" in mat_data:
        for item in mat_data["material"]:
            name = item.get("n")
            if not name:
                continue

            # Mapping:
            # c: category, pm: price_multiplier, wm: weight_multiplier,
            # db: damage_bonus, df: defense_bonus, sr: special_rules

            defaults = {
                "category": item.get("c", "metal"),
                "price_multiplier": item.get("pm", 1.0),
                "weight_multiplier": item.get("wm", 1.0),
                "damage_bonus": item.get("db", 0),
                "defense_bonus": item.get("df", 0),
                "special_rules": item.get("sr", ""),
            }

            obj, created = Material.objects.update_or_create(
                name=name, defaults=defaults
            )
            if created:
                count_created += 1
            else:
                count_updated += 1

    # 2. Qualities (qualidade.json)
    qual_data = get_json_data("qualidade.json")
    if qual_data and "qualidade" in qual_data:
        for item in qual_data["qualidade"]:
            name = item.get("n")
            if not name:
                continue

            # Mapping:
            # s: symbol, cm: cost_multiplier, ab: attack_bonus,
            # db: defense_bonus, sb: skill_bonus

            defaults = {
                "symbol": item.get("s", ""),
                "cost_multiplier": item.get("cm", 1.0),
                "attack_bonus": item.get("ab", 0),
                "defense_bonus": item.get("db", 0),
                "skill_bonus": item.get("sb", 0),
            }

            obj, created = ItemQuality.objects.update_or_create(
                name=name, defaults=defaults
            )
            if created:
                count_created += 1
            else:
                count_updated += 1

    print(f"Materials/Qualities: {count_created} created, {count_updated} updated.")
