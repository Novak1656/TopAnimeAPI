from django.db import models
from django_unique_slugify import slugify
from unidecode import unidecode


class Anime(models.Model):
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=255
    )
    title = models.CharField(
        verbose_name='Название',
        max_length=255
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True
    )
    score = models.DecimalField(
        verbose_name='Рейтинг',
        max_digits=4, decimal_places=2
    )
    type = models.CharField(
        verbose_name='Тип',
        max_length=255,
        blank=True,
        null=True
    )
    season = models.ForeignKey(
        verbose_name='Аниме сезон',
        to='Season',
        on_delete=models.PROTECT,
        related_name='anime',
        blank=True,
        null=True
    )
    studio = models.ForeignKey(
        verbose_name='Студия',
        to='Studio',
        on_delete=models.PROTECT,
        related_name='anime',
        blank=True,
        null=True
    )
    genres = models.ManyToManyField(
        verbose_name='Жанры',
        to='Genre',
        related_name='anime',
        blank=True,
    )
    image = models.CharField(
        verbose_name='Постер',
        max_length=255,
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Аниме'
        verbose_name_plural = 'Аниме'
        ordering = ['-score']

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(unidecode(self.title))
        super(Anime, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.title}: {self.score}'


class Genre(models.Model):
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=255
    )
    title = models.CharField(
        verbose_name='Название',
        max_length=255,
        unique=True
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['title']

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(unidecode(self.title))
        super(Genre, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Studio(models.Model):
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=255
    )
    title = models.CharField(
        verbose_name='Название',
        max_length=255,
        unique=True
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Студия'
        verbose_name_plural = 'Студии'
        ordering = ['title']

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(unidecode(self.title))
        super(Studio, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Season(models.Model):
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=255
    )
    title = models.CharField(
        verbose_name='Название',
        max_length=255,
        unique=True
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Аниме сезон'
        verbose_name_plural = 'Аниме сезоны'
        ordering = ['title']

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(unidecode(self.title))
        super(Season, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
