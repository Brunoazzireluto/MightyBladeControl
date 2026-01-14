from core.models import Language
from .utils import get_json_data, strip_html_tags


def run():
    print("Seeding Languages...")

    count_created = 0
    count_updated = 0

    # Common Languages
    comum_data = get_json_data("idiomasComuns.json")
    if comum_data and "comum" in comum_data:
        for item in comum_data["comum"]:
            if len(item) < 3:
                continue

            name = item[0]
            speakers = item[1]
            description = item[2]

            obj, created = Language.objects.update_or_create(
                name=name,
                defaults={
                    "speakers": speakers,
                    "description": strip_html_tags(description),
                    "is_exotic": False,
                },
            )
            if created:
                count_created += 1
            else:
                count_updated += 1

    # Exotic Languages
    exotico_data = get_json_data("idiomasExoticos.json")
    if exotico_data and "exotico" in exotico_data:
        for item in exotico_data["exotico"]:
            if len(item) < 3:
                continue

            name = item[0]
            speakers = item[1]
            description = item[2]

            obj, created = Language.objects.update_or_create(
                name=name,
                defaults={
                    "speakers": speakers,
                    "description": strip_html_tags(description),
                    "is_exotic": True,
                },
            )
            if created:
                count_created += 1
            else:
                count_updated += 1

    print(f"Languages: {count_created} created, {count_updated} updated.")
