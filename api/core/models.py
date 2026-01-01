from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()

# ==========================================
# 1. CLASSES ABSTRATAS & UTILITÁRIOS
# ==========================================


class MightyBaseModel(models.Model):
    """Base para entidades que possuem Nome, Descrição e Slug."""

    name = models.CharField(max_length=100, unique=True, verbose_name="Nome")
    slug = models.SlugField(max_length=120, unique=True, blank=True, null=True)
    description = models.TextField(blank=True, verbose_name="Descrição")

    class Meta:
        abstract = True
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# ==========================================
# 2. CORE: HABILIDADES E MAGIAS
# ==========================================


class Ability(MightyBaseModel):
    CATEGORY_CHOICES = [
        ("racial", "Racial"),
        ("class", "De Classe"),
        ("magic", "Magia Arcana"),
        ("general", "Geral"),
        ("path", "Caminho"),
        ("support", "Suporte"),  # Para habilidades de monstros
    ]

    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default="general"
    )

    # Detalhes técnicos (usados principalmente em Magias)
    mana_cost = models.IntegerField(
        default=0, null=True, blank=True, verbose_name="Custo de Mana"
    )
    difficulty = models.IntegerField(null=True, blank=True, verbose_name="Dificuldade")
    casting_time = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Tempo de Execução"
    )
    range_info = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Alcance/Área"
    )

    # Texto descritivo dos requisitos para exibição simples
    requirements_text = models.TextField(
        blank=True, help_text="Texto descritivo dos requisitos (ex: 'Força 3')"
    )

    class Meta:
        verbose_name = "Habilidade/Magia"
        verbose_name_plural = "Habilidades e Magias"


# ==========================================
# 3. DADOS ESTÁTICOS: RAÇA, CLASSE, ANTECEDENTE
# ==========================================


class Race(MightyBaseModel):
    # Atributos Base (De 'a' no JSON)
    initial_str = models.IntegerField(default=0, verbose_name="Força Inicial")
    initial_agi = models.IntegerField(default=0, verbose_name="Agilidade Inicial")
    initial_int = models.IntegerField(default=0, verbose_name="Inteligência Inicial")
    initial_wil = models.IntegerField(default=0, verbose_name="Vontade Inicial")

    class Meta:
        verbose_name = "Raça"
        verbose_name_plural = "Raças"


class RaceLore(models.Model):
    """Regras de nomes e cultura (Vertical Partitioning)"""

    race = models.OneToOneField(Race, on_delete=models.CASCADE, related_name="lore")
    naming_rules_html = models.TextField(verbose_name="Regras de Nomes (HTML)")
    male_names = models.TextField(
        blank=True, help_text="Lista separada por vírgulas ou quebras"
    )
    female_names = models.TextField(blank=True)

    def __str__(self):
        return f"Lore: {self.race.name}"


class RaceInnateAbility(models.Model):
    """Habilidades que a raça ganha automaticamente (ex: Anão -> Visão no Escuro)"""

    race = models.ForeignKey(
        Race, on_delete=models.CASCADE, related_name="innate_abilities"
    )
    ability = models.ForeignKey(Ability, on_delete=models.CASCADE)


class CharacterClass(MightyBaseModel):
    # Bônus de Atributo ao escolher a classe
    bonus_str = models.IntegerField(default=0)
    bonus_agi = models.IntegerField(default=0)
    bonus_int = models.IntegerField(default=0)
    bonus_wil = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Classe"
        verbose_name_plural = "Classes"


class ClassAvailableAbility(models.Model):
    """Lista de habilidades que a classe PODE comprar"""

    character_class = models.ForeignKey(
        CharacterClass, on_delete=models.CASCADE, related_name="available_skills"
    )
    ability = models.ForeignKey(Ability, on_delete=models.CASCADE)


class Background(MightyBaseModel):
    """Antecedentes (Regras) - De 'antecedentes.json'"""

    benefit_text = models.TextField(verbose_name="Benefício Mecânico")
    requirements_text = models.TextField(blank=True)
    starting_equipment = models.TextField(blank=True)

    class Meta:
        verbose_name = "Antecedente"
        verbose_name_plural = "Antecedentes"


# ==========================================
# 4. LINGUISTICA & BESTIÁRIO
# ==========================================


class Language(MightyBaseModel):
    speakers = models.CharField(
        max_length=255, blank=True, verbose_name="Falantes Típicos"
    )
    is_exotic = models.BooleanField(default=False)
    script = models.CharField(max_length=50, blank=True, verbose_name="Alfabeto")

    class Meta:
        verbose_name = "Idioma"
        verbose_name_plural = "Idiomas"


class Creature(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    creature_type = models.CharField(max_length=50, blank=True)  # Besta, Morto-Vivo
    size = models.CharField(max_length=50, blank=True)

    # Atributos
    strength = models.IntegerField(default=0)
    agility = models.IntegerField(default=0)
    intelligence = models.IntegerField(default=0)
    will = models.IntegerField(default=0)

    # Vitals
    hp = models.IntegerField(default=10, verbose_name="Vida")
    mana = models.IntegerField(default=0)
    defense = models.IntegerField(default=0)

    # Dados complexos (JSONB no Postgres)
    attacks_data = models.JSONField(default=list, blank=True)
    abilities_data = models.JSONField(default=list, blank=True)
    description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class SpiritAnimal(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nome")
    description = models.TextField(
        blank=True,
        verbose_name="Descrição",
        help_text="Informações sobre rolagens e mecânicas do espírito animal",
    )

    class Meta:
        verbose_name = "Espírito Animal"
        verbose_name_plural = "Espíritos Animais"

    def __str__(self):
        return self.name


# ==========================================
# 5. PERSONAGEM (A FICHA)
# ==========================================


class Character(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="characters")
    name = models.CharField(max_length=100)

    # --- Lore do Jogador ---
    biography = models.TextField(blank=True, verbose_name="Biografia")
    appearance = models.TextField(blank=True, verbose_name="Aparência")
    personality = models.TextField(blank=True, verbose_name="Personalidade")

    # --- Progresso ---
    level = models.IntegerField(default=1)
    xp = models.IntegerField(default=0)

    # --- Vínculos de Regra ---
    race = models.ForeignKey(Race, on_delete=models.PROTECT)
    character_class = models.ForeignKey(CharacterClass, on_delete=models.PROTECT)
    background = models.ForeignKey(
        Background, on_delete=models.PROTECT, null=True, blank=True
    )

    # Espírito Animal (opcional, apenas um)
    spirit_animal = models.ForeignKey(
        SpiritAnimal,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="characters",
        verbose_name="Espírito Animal",
        help_text="Espírito animal vinculado ao personagem (apenas um)",
    )

    # --- Atributos (Base + Bônus + Evolução) ---
    strength = models.IntegerField(default=0)
    agility = models.IntegerField(default=0)
    intelligence = models.IntegerField(default=0)
    will = models.IntegerField(default=0)

    # --- Status Atuais ---
    hp_max = models.IntegerField(default=10)
    hp_current = models.IntegerField(default=10)
    mana_max = models.IntegerField(default=0)
    mana_current = models.IntegerField(default=0)

    # --- Economia (A Carteira) ---
    coin_copper = models.IntegerField(default=0, verbose_name="Cobre")
    coin_silver = models.IntegerField(default=0, verbose_name="Prata")
    coin_gold = models.IntegerField(default=0, verbose_name="Ouro")

    # --- Carga ---
    extra_carry_capacity = models.DecimalField(
        default=0.0, max_digits=6, decimal_places=2, verbose_name="Carga Extra (Kg)"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (Lv {self.level} {self.character_class.name})"

    @property
    def max_load(self):
        # Regra base: Força * 7 (Mighty Blade 3ª Ed)
        return (self.strength * 7) + float(self.extra_carry_capacity)

    @property
    def current_load(self):
        # Calcula peso total via Python
        # (O ideal é usar annotations no QuerySet para performance, mas isso funciona para MVP)
        return sum(item.final_weight for item in self.inventory.all())


# --- Tabelas Relacionais do Personagem ---


class CharacterAbility(models.Model):
    character = models.ForeignKey(
        Character, on_delete=models.CASCADE, related_name="abilities"
    )
    ability = models.ForeignKey(Ability, on_delete=models.PROTECT)
    notes = models.CharField(max_length=255, blank=True)


class CharacterLanguage(models.Model):
    character = models.ForeignKey(
        Character, on_delete=models.CASCADE, related_name="languages"
    )
    language = models.ForeignKey(Language, on_delete=models.PROTECT)


class CharacterCompanion(models.Model):
    character = models.ForeignKey(
        Character, on_delete=models.CASCADE, related_name="companions"
    )
    creature = models.ForeignKey(Creature, on_delete=models.PROTECT)
    custom_name = models.CharField(max_length=100)
    current_hp = models.IntegerField()
    notes = models.TextField(blank=True)


# ==========================================
# 6. SISTEMA DE INVENTÁRIO (ITEM, MATERIAL, MOCHILA)
# ==========================================


class Material(models.Model):
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=30)  # metal, madeira
    price_multiplier = models.DecimalField(max_digits=5, decimal_places=2, default=1.0)
    weight_multiplier = models.DecimalField(max_digits=5, decimal_places=2, default=1.0)
    damage_bonus = models.IntegerField(default=0)
    defense_bonus = models.IntegerField(default=0)
    special_rules = models.TextField(blank=True)

    def __str__(self):
        return self.name


class ItemQuality(models.Model):
    name = models.CharField(max_length=50)  # Baixa, Alta, Obra-Prima
    symbol = models.CharField(max_length=5)  # Q+, Q-
    cost_multiplier = models.DecimalField(max_digits=5, decimal_places=2, default=1.0)
    attack_bonus = models.IntegerField(default=0)
    defense_bonus = models.IntegerField(default=0)
    skill_bonus = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Item(models.Model):
    """Classe Pai para todos os itens"""

    ITEM_TYPES = [
        ("weapon", "Arma"),
        ("armor", "Armadura/Escudo"),
        ("consumable", "Consumível"),
        ("gear", "Equipamento Geral"),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    weight = models.DecimalField(
        max_digits=6, decimal_places=3, verbose_name="Peso Base (kg)"
    )
    price = models.IntegerField(default=0, verbose_name="Preço Base (Cobre)")
    is_stackable = models.BooleanField(default=True)
    item_type = models.CharField(max_length=20, choices=ITEM_TYPES, default="gear")

    def __str__(self):
        return self.name


# --- Herança de Itens (Multi-Table Inheritance) ---


class Weapon(Item):
    damage = models.IntegerField(default=0)
    damage_type = models.CharField(max_length=50, blank=True)  # Corte, Perfuração
    grip = models.CharField(max_length=50, blank=True)  # Haste, Leve
    min_strength = models.IntegerField(default=0)
    defense_bonus = models.BooleanField(default=False)  # Se dá defesa passiva
    is_throwable = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Arma"
        verbose_name_plural = "Armas"


class Armor(Item):
    defense_bonus = models.IntegerField(default=0)
    penalty = models.IntegerField(default=0)
    is_heavy = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Armadura ou Escudo"
        verbose_name_plural = "Armaduras e Escudos"


class Consumable(Item):
    rarity = models.CharField(max_length=50, blank=True)
    charges = models.IntegerField(default=1)

    class Meta:
        verbose_name = "Consumível"
        verbose_name_plural = "Consumíveis"


# --- A Mochila (Pivot Table) ---


class CharacterItem(models.Model):
    character = models.ForeignKey(
        Character, on_delete=models.CASCADE, related_name="inventory"
    )
    item = models.ForeignKey(Item, on_delete=models.PROTECT)

    # Customizações
    material = models.ForeignKey(
        Material, on_delete=models.SET_NULL, null=True, blank=True
    )
    quality = models.ForeignKey(
        ItemQuality, on_delete=models.SET_NULL, null=True, blank=True
    )

    quantity = models.IntegerField(default=1)
    is_equipped = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity}x {self.item.name} ({self.character.name})"

    @property
    def final_weight(self):
        w = float(self.item.weight)
        if self.material:
            w *= float(self.material.weight_multiplier)
        return w * self.quantity

    @property
    def final_price(self):
        p = float(self.item.price)
        if self.material:
            p *= float(self.material.price_multiplier)
        if self.quality:
            p *= float(self.quality.cost_multiplier)
        return int(p * self.quantity)
