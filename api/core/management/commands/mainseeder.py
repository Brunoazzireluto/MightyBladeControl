from django.core.management.base import BaseCommand
from seeds import (
    habilidades,
    racas,
    classes,
    antecedentes,
    idiomas,
    espiritos,
    criaturas,
    itens,
    materiais,
)


class Command(BaseCommand):
    help = "Seeds the database with data from JSON files in api/docs/"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting Database Seeding..."))

        seeders = [
            ("Languages", idiomas),
            ("Materials & Qualities", materiais),
            ("Abilities & Magic", habilidades),
            ("Races", racas),
            ("Classes", classes),
            ("Backgrounds", antecedentes),
            ("Spirit Animals", espiritos),
            ("Creatures", criaturas),
            ("Items & Equipment", itens),
        ]

        for name, seeder in seeders:
            try:
                self.stdout.write(f"--- Seeding {name} ---")
                seeder.run()
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Error seeding {name}: {e}"))
                import traceback

                traceback.print_exc()

        self.stdout.write(self.style.SUCCESS("\nSuccessfully seeded database!"))
