from django.db import models
from django.contrib.auth.models import User

DISTRICT_CHOICES = [
    # Марказ ва шаҳрҳои асосӣ
    ('dushanbe', 'ш. Душанбе'),
    ('khujand', 'ш. Хуҷанд'),
    ('bokhtar', 'ш. Бохтар'),
    ('kulob', 'ш. Кӯлоб'),
    ('vahdat', 'ш. Ваҳдат'),
    ('hissor', 'ш. Ҳисор'),
    ('tursunzoda', 'ш. Турсунзода'),
    ('roghun', 'ш. Роғун'),
    ('nurek', 'ш. Норак'),
    ('levakant', 'ш. Левакант'),
    ('khorugh', 'ш. Хоруғ'),

    # Ноҳияҳои Хатлон ва дигар бахшҳо
    ('temurmalik', 'н. Темурмалик'),
    ('dangara', 'н. Данғара'),
    ('vose', 'н. Восеъ'),
    ('yavon', 'н. Ёвон'),
    ('vakhsh', 'н. Вахш'),
    ('dusti', 'н. Дӯстӣ'),
    ('kushoniyon', 'н. Кӯшониён'),
    ('baljuvon', 'н. Балҷувон'),
    ('muminobod', 'н. Муъминобод'),
    ('panj', 'н. Панҷ'),
    ('farkhor', 'н. Фархор'),
    ('khovaling', 'н. Ховалинг'),
    ('sh_shohin', 'н. Шамсиддин Шоҳин'),
    ('jayhun', 'н. Ҷайҳун'),
    ('j_balkhi', 'н. Ҷалолиддини Балхӣ'),
    ('jomi', 'н. А.Ҷомӣ'),
    ('bahoriyon', 'н. Баҳориён'),
    ('nosiri_khusrav', 'н. Носири Хусрав'),

    # Ноҳияҳои тобеи ҷумҳурӣ (ШНТҶ)
    ('rudaki', 'н. Рӯдакӣ'),
    ('varzob', 'н. Варзоб'),
    ('shahrinav', 'н. Шаҳринав'),
    ('fayzobod', 'н. Файзобод'),
    ('lakhsh', 'н. Лахш'),
    ('rasht', 'н. Рашт'),
    ('tojikobod', 'н. Тоҷикобод'),
    ('nurobod', 'н. Нуробод'),
    ('sangvor', 'н. Сангвор'),

    # Шаҳру ноҳияҳои Суғд
    ('ayni', 'н. Айнӣ'),
    ('asht', 'н. Ашт'),
    ('b_gafurov', 'н. Бобоҷон Ғафуров'),
    ('devashtich', 'н. Деваштич'),
    ('zafarobod', 'н. Зафаробод'),
    ('k_mastchoh', 'н. Кӯҳистони Мастчоҳ'),
    ('mastchoh', 'н. Мастчоҳ'),
    ('spitamen', 'н. Спитамен'),
    ('j_rasulov', 'н. Ҷаббор Расулов'),
    ('istravshan', 'ш. Истаравшан'),
    ('isfara', 'ш. Исфара'),
    ('konibodom', 'ш. Конибодом'),
    ('panjakent', 'ш. Панҷакент'),
    ('guliston', 'ш. Гулистон'),
    ('bostan', 'ш. Бӯстон'),
    ('istiqlol', 'ш. Истиқлол'),

    # Ноҳияҳои ВМКБ
    ('darvoz', 'н. Дарвоз'),
    ('vanj', 'н. Ванҷ'),
    ('rushon', 'н. Рӯшон'),
    ('shughnon', 'н. Шугнон'),
    ('roshtqala', 'н. Роштқалъа'),
    ('ishkoshim', 'н. Ишкошим'),
    ('murghob', 'н. Мурғоб'),
]

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Номи категория")
    icon = models.CharField(max_length=50, blank=True, null=True, verbose_name="Иконка (FontAwesome)")
    
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True, 
        related_name='subcategories', 
        verbose_name="Категорияи асосӣ (Агар зербанд бошад)"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категорияҳо"

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} ➡️ {self.name}"
        return self.name


class Product(models.Model):
    
    STATUS_CHOICES = [
        ('new', 'Нав'),
        ('used', 'Истифодашуда'),
    ]
    
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='new', 
        verbose_name="Ҳолат"
    )
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Соҳиби эълон")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    
    title = models.CharField(max_length=200, verbose_name="Номи маҳсулот")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Нарх (сомонӣ)")
    description = models.TextField(verbose_name="Тавсифи маҳсулот")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Сурат")
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new', verbose_name="Ҳолат")
    location = models.CharField(max_length=50, choices=DISTRICT_CHOICES, default='dushanbe', verbose_name="Шаҳр/Ноҳия")
    phone = models.CharField(max_length=20, verbose_name="Телефон барои алоқа")
    
    has_delivery = models.BooleanField(default=False, verbose_name="Имконияти расонидан")
    delivery = models.BooleanField(default=False, verbose_name="Хизматрасонии расонидан (Доставка)")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Вакти дақиқи эълон")
    
    def __str__(self):
        return self.title
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wallet = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) # Баланси корбар

    def __str__(self):
        return f"Профили {self.user.username}"