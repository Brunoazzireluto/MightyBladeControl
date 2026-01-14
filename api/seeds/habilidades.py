from core.models import Ability
from .utils import (
    get_json_data,
    get_files_by_pattern,
    parse_requirements,
    strip_html_tags,
)
import os


def run():
    print("Seeding Abilities...")

    # Encontra todos arquivos de habilidades
    files = get_files_by_pattern("habilidades*.json")
    files += get_files_by_pattern("magias*.json")  # Inclui magias também

    count_created = 0
    count_updated = 0

    for file_path in files:
        filename = os.path.basename(file_path)
        data = get_json_data(filename)

        if not data:
            continue

        # Determina a chave correta (pode ser 'habilidade' ou 'magia' dependendo do arquivo)
        items = []
        if "habilidade" in data:
            items = data["habilidade"]
        elif "magia" in data:
            items = data["magia"]

        for item in items:
            name = item.get("n")
            if not name:
                continue

            # Mapeamento de Categoria
            json_cat = item.get("c", "").lower()
            category = "general"

            if "mística" in json_cat or "mistica" in json_cat:
                category = "magic"
            elif "arcana" in json_cat:
                category = "magic"
            elif "técnica" in json_cat or "tecnica" in json_cat:
                category = "general"  # Poderia ser class, mas habilidades gerais tb sao tecnicas
            elif "característica" in json_cat or "caracteristica" in json_cat:
                category = "racial"  # Muitas caracteristicas sao raciais, mas nem todas. Defaulting.

            # Se a habilidade já existe, não sobrescrevemos a categoria se ela foi ajustada manualmente
            # Mas aqui é seed, então assumimos autoridade do JSON ou mantemos default.

            defaults = {
                "description": strip_html_tags(item.get("d", "")),
                "mana_cost": int(item.get("m", 0)) if int(item.get("m", 0)) >= 0 else 0,
                "difficulty": (
                    int(item.get("df", 0)) if int(item.get("df", 0)) >= 0 else None
                ),
                "casting_time": str(item.get("ct", "")),  # Convert to string
                "range_info": str(
                    item.get("r", "")
                ),  # Raw requirements data saved here strictly if needed, or mapping logic
                # Na verdade range_info deveria ser Alcance. O JSON não parece ter campo explícito de Alcance para Habilidades, exceto no texto ou 're'.
                # Vamos usar 're' (Resumo) em requirements_text por enquanto, ou parse_requirements(r)
                "requirements_text": parse_requirements(item.get("r", [])),
                "category": category,
            }

            obj, created = Ability.objects.update_or_create(
                name=name, defaults=defaults
            )

            if created:
                count_created += 1
            else:
                count_updated += 1

    print(f"Abilities/Magic: {count_created} created, {count_updated} updated.")
