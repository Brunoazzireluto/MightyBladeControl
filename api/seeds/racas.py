from core.models import Race, RaceLore, RaceInnateAbility, Ability
from .utils import get_json_data, parse_attributes, strip_html_tags
import re


def parse_names_from_context(race_name, nomes_data):
    """
    Encontra os dados de nomes para a raça específica no JSON de nomes.
    """
    if not nomes_data or "nome" not in nomes_data:
        return None

    # Tenta encontrar a entrada correta
    # nomes_data['nome'] é uma lista de listas [ "NomeRaça", "HTML" ]

    target_lore = None

    for entry in nomes_data["nome"]:
        category_name = entry[0]
        # Match impreciso: 'Humanos e Metadílios' deve casar com 'Humano'
        if race_name in category_name or (
            race_name.endswith("s") and race_name[:-1] in category_name
        ):
            target_lore = entry[1]
            break

            # Casos especificos
        if race_name == "Humano" and "Humanos" in category_name:
            target_lore = entry[1]
            break
        if race_name == "Anão" and "Anões" in category_name:
            target_lore = entry[1]
            break

    if not target_lore:
        return None

    # Extract names using regex
    male_names = ""
    female_names = ""

    # Regex pattern: <b> Masculinos </b> <br/> (content) <br/>
    # Note: The HTML in JSON might vary slightly in spacing

    male_match = re.search(
        r"<b>\s*Masculinos\s*</b>\s*<br/>(.*?)(?:<br/>|$)",
        target_lore,
        re.IGNORECASE | re.DOTALL,
    )
    if male_match:
        male_names = male_match.group(1).strip().replace("\n", "")

    female_match = re.search(
        r"<b>\s*Femininos\s*</b>\s*<br/>(.*?)(?:<br/>|$)",
        target_lore,
        re.IGNORECASE | re.DOTALL,
    )
    if female_match:
        female_names = female_match.group(1).strip().replace("\n", "")

    return {"html": target_lore, "male": male_names, "female": female_names}


def run():
    print("Seeding Races...")

    data = get_json_data("racas.json")
    nomes_data = get_json_data("nomes.json")

    if not data or "raca" not in data:
        print("No race data found.")
        return

    for item in data["raca"]:
        name = item.get("n")
        if not name:
            continue

        print(f"Processing Race: {name}")

        attrs = parse_attributes(item.get("a"))

        defaults = {
            "description": strip_html_tags(item.get("d", "")),
            "initial_str": attrs["strength"],
            "initial_agi": attrs["agility"],
            "initial_int": attrs["intelligence"],
            "initial_wil": attrs["will"],
        }

        race_obj, created = Race.objects.update_or_create(name=name, defaults=defaults)

        # Lore
        lore_info = parse_names_from_context(name, nomes_data)
        if lore_info:
            RaceLore.objects.update_or_create(
                race=race_obj,
                defaults={
                    "naming_rules_html": strip_html_tags(lore_info["html"]),
                    "male_names": strip_html_tags(lore_info["male"]),
                    "female_names": strip_html_tags(lore_info["female"]),
                },
            )

        # Innate Abilities
        abilities_list = item.get("h", [])
        # 'ha' field seems to be "Habilidade Automatica" or "Habilidade de Ancestralidade"?
        # In racas.json: "ha": "Vigor Nórdico".
        # 'h' is list of OPTIONAL/CHOICE abilities? Or list of ALL abilities?
        # JSON structure:
        # "ha": "Vigor Nórdico"
        # "h": ["Berserkir", "Bravura...", ...]
        # Usually races have 1 automatic ability and a list of purchasable ones.
        # But `RaceInnateAbility` model implies automatic ones.
        # Let's assume 'ha' is the Innate one.

        innate_name = item.get("ha")
        if innate_name:
            # Try to find ability
            try:
                ab = Ability.objects.filter(name__iexact=innate_name).first()
                if ab:
                    RaceInnateAbility.objects.get_or_create(race=race_obj, ability=ab)
                else:
                    print(
                        f"Warning: Innate Ability '{innate_name}' not found for {name}"
                    )
            except Exception as e:
                print(f"Error linking innate ability: {e}")
