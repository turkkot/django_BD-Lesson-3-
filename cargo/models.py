from django.db import models
from datetime import date
from django.db.models import Model
from django.db.models.functions import Floor


# Таблица "Водители"
class Drivers(models.Model):

    GENDER_CHOICES = [
        ('М', 'Мужской'),
        ('Ж', 'Женский'),
    ]

    surname = models.CharField(verbose_name='Фамилия', max_length=30)
    name = models.CharField(verbose_name='Имя', max_length=30)
    employment_date = models.DateField(verbose_name='Дата приема на работу')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='Пол')
    photo = models.ImageField(upload_to='drivers_photos/', verbose_name='Фото', blank=True, null=True)

    def get_work_experience(self):
        current_date = date.today()
        experience_years = current_date.year - self.employment_date.year
        if (current_date.month, current_date.day) < (self.employment_date.month, self.employment_date.day):
            experience_years -= 1
        return experience_years

    def __str__(self):
        return self.surname

    class Meta:
        verbose_name = 'Водитель'
        verbose_name_plural = 'Водители'
        ordering = ['surname']

# Таблица "Маршруты"
class Routes(models.Model):
    name = models.CharField(verbose_name='Название', max_length=30, default='Неизвестный маршрут', blank=True)
    distance = models.IntegerField(verbose_name='Расстояние')
    travel_days = models.IntegerField(verbose_name='Дней в пути')
    payment = models.IntegerField(verbose_name='Оплата')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'
        ordering = ['name']  # Сортировка по названию маршрута

# Таблица "Перевозки"
class Transportations(models.Model):
    departure_date = models.DateField(verbose_name='Дата отправления')
    return_date = models.DateField(verbose_name='Дата возвращения')
    is_bonus = models.BooleanField(verbose_name='Премия', default=False)
    route = models.ForeignKey(Routes, on_delete=models.CASCADE, verbose_name='Маршрут')  # Связь с моделью Routes

    def get_travel_time(self):
        return self.return_date - self.departure_date

    def __str__(self):
        return f"{self.departure_date.strftime('%Y-%m-%d')} - {self.route.name}"

    class Meta:
        verbose_name = 'Перевозка'
        verbose_name_plural = 'Перевозки'
        ordering = ['departure_date']

# Промежуточная модель для связи таблиц "Водители" и "Перевозки"
class DriversTransportations(models.Model):
    driver = models.ForeignKey(Drivers, on_delete=models.CASCADE)
    transportation = models.ForeignKey(Transportations, on_delete=models.CASCADE)
    transport = models.ForeignKey('Transport', on_delete=models.CASCADE)
    driving_hours = models.IntegerField(verbose_name='Часы в пути')

    def __str__(self):
        return f'{self.driver.surname} - {self.transportation.departure_date}'

    class Meta:
        verbose_name = 'Связь Водителя и Перевозки'
        verbose_name_plural = 'Связи Водителей и Перевозок'

# Связь между таблицами "Водители" и "Перевозки" через промежуточную таблицу-связку
Drivers.transportations = models.ManyToManyField(Transportations, through=DriversTransportations)

# Таблица "Транспорт"
class Transport(models.Model):
    vehicle_number = models.CharField(verbose_name='Номер транспортного средства', max_length=20, unique=True)
    model = models.CharField(verbose_name='Модель', max_length=50)
    capacity = models.IntegerField(verbose_name='Грузоподъемность (кг)')


    def __str__(self):
        return f'{self.model} ({self.vehicle_number})'

    class Meta:
        verbose_name = 'Транспорт'
        verbose_name_plural = 'Транспорт'
        ordering = ['model']


# Таблица "Детали перевозки"
class TransportationDetails(models.Model):
    transportation = models.OneToOneField(Transportations, on_delete=models.CASCADE, verbose_name='Перевозка')
    description = models.TextField(verbose_name='Описание перевозки', blank=True, null=True)
    document_number = models.CharField(verbose_name='Номер документа', max_length=30)
    insurance = models.BooleanField(verbose_name='Наличие страховки', default=False)

    def __str__(self):
        return f'Детали перевозки {self.transportation}'

    class Meta:
        verbose_name = 'Детали перевозки'
        verbose_name_plural = 'Детали перевозок'