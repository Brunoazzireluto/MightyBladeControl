from core.models import SpiritAnimal
from .utils import get_json_data, strip_html_tags


def run():
    print("Seeding Spirit Animals...")

    data = get_json_data("espiritosAnimais.json")

    if not data or "espirito_animal" not in data:
        print("No spirit animal data found.")
        return

    count_created = 0
    count_updated = 0

    for item in data["espirito_animal"]:
        name = item.get("Espírito Animal")
        description = item.get("Descrição", "")

        if not name:
            continue

        obj, created = SpiritAnimal.objects.update_or_create(
            name=name, defaults={"description": strip_html_tags(description)}
        )

        if created:
            count_created += 1
        else:
            count_updated += 1

    print(f"Spirit Animals: {count_created} created, {count_updated} updated.")
