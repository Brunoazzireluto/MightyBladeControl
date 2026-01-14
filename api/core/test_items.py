from django.test import TestCase
from core.models import Item, Weapon, Armor, Consumable
from seeds import itens
import unittest.mock as mock


class ItemStackabilityTests(TestCase):
    def test_item_default_stackability(self):
        """Standard items (gear) should be non-stackable by default now."""
        item = Item.objects.create(name="Corda", weight=1.0, price=10)
        self.assertFalse(item.is_stackable)

    def test_weapon_stackability_logic(self):
        """Weapon stackability depends on whether it's throwable."""
        # Non-throwable
        sword = Weapon.objects.create(
            name="Espada", weight=2.0, price=100, is_throwable=False
        )
        self.assertFalse(sword.is_stackable)

        # Throwable
        dagger = Weapon.objects.create(
            name="Adaga", weight=0.25, price=50, is_throwable=True, is_stackable=True
        )
        self.assertTrue(dagger.is_stackable)

    def test_armor_is_never_stackable(self):
        """Armors should never be stackable."""
        armor = Armor.objects.create(
            name="Couro", weight=10.0, price=100, is_stackable=False
        )
        self.assertFalse(armor.is_stackable)

    def test_consumable_is_stackable(self):
        """Consumables should be stackable."""
        potion = Consumable.objects.create(
            name="Poção", weight=0.1, price=50, is_stackable=True
        )
        self.assertTrue(potion.is_stackable)


class ItemSeederTests(TestCase):
    @mock.patch("seeds.itens.get_json_data")
    def test_seeder_correctly_sets_stackability(self, mock_json):
        # Mock data for one weapon (throwable), one weapon (non-throwable), one armor
        mock_json.side_effect = lambda filename: {
            "arma.json": {
                "arma": [
                    {"n": "Adaga Teste", "ar": True, "p": 0.5, "c": 10},
                    {"n": "Espada Teste", "ar": False, "p": 2.0, "c": 100},
                ]
            },
            "defesa.json": {"defesa": [{"n": "Couro Teste", "p": 10, "c": 100}]},
            "pocao.json": {"pocao": []},
            "mundano.json": {"mundano": []},
        }.get(filename)

        itens.run()

        dagger = Weapon.objects.get(name="Adaga Teste")
        self.assertTrue(dagger.is_stackable)
        self.assertTrue(dagger.is_throwable)

        sword = Weapon.objects.get(name="Espada Teste")
        self.assertFalse(sword.is_stackable)
        self.assertFalse(sword.is_throwable)

        armor = Armor.objects.get(name="Couro Teste")
        self.assertFalse(armor.is_stackable)
