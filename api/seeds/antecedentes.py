from core.models import Background
from .utils import get_json_data, parse_requirements, strip_html_tags


def run():
    print("Seeding Backgrounds...")

    data = get_json_data("antecedentes.json")

    if not data or "antecedente" not in data:
        print("No background data found.")
        return

    count_created = 0
    count_updated = 0

    for item in data["antecedente"]:
        name = item.get("n")
        if not name:
            continue

        defaults = {
            "description": strip_html_tags(item.get("d", "")),
            "benefit_text": item.get("b", ""),
            "requirements_text": parse_requirements(item.get("r", [])),
            "starting_equipment": item.get("eq", ""),
        }

        obj, created = Background.objects.update_or_create(name=name, defaults=defaults)

        if created:
            count_created += 1
        else:
            count_updated += 1

    print(f"Backgrounds: {count_created} created, {count_updated} updated.")
