from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import default_token_generator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.dispatch.dispatcher import receiver

from .validators import validate_username, validate_year


class User(AbstractUser):
    """Модель пользователя."""
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLE = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    )
    username = models.CharField(
        'Никнейм',
        max_length=150,
        validators=(validate_username,),
        unique=True,
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль',
        max_length=30,
        choices=ROLE,
        default='user',
    )
    email = models.EmailField(
        'Почта',
        max_length=128,
        unique=True
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=128,
        blank=True,
    )

    @property
    def get_admin(self):
        return self.role == self.ADMIN

    @property
    def get_moderator(self):
        return self.role == self.MODERATOR


@receiver(models.signals.post_save, sender=User)
def post_save(sender, instance, created, **kwargs):
    if created:
        confirmation_code = default_token_generator.make_token(
            instance
        )
        instance.confirmation_code = confirmation_code
        instance.save()


class CreatedModel(models.Model):
    """Абстрактная модель. Добавляет дату создания."""
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        abstract = True


class Category(CreatedModel):
    """Модель категорий для произведений"""
    name = models.CharField(
        verbose_name='Имя',
        max_length=256
    )
    slug = models.SlugField(
        unique=True,
        max_length=50
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name[:20]


class Genre(CreatedModel):
    """Модель жанров произведений"""
    name = models.CharField(
        verbose_name='Имя',
        max_length=256
    )
    slug = models.SlugField(
        unique=True,
        max_length=50
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name[:20]


class Title(CreatedModel):
    """Модель произведений"""
    name = models.CharField(
        verbose_name='Название',
        max_length=256
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',
        validators=(validate_year,)
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание',
        help_text='Введите описание произведения'
    )
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name='title',
        verbose_name='Категория',
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:20]


class GenreTitle(CreatedModel):
    """Модель связи жанров и произведений"""
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Жанр-Произведение'
        verbose_name_plural = 'Жанры-Произведения'
        constraints = (
            models.UniqueConstraint(fields=('title', 'genre',),
                                    name='unique_genre_title'),
        )

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(CreatedModel):
    """Модель отзыва к произведению."""
    text = models.TextField(
        verbose_name='Текст отзыва',
        help_text='Текст отзыва'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва'
    )
    score = models.SmallIntegerField(
        verbose_name='Оценка',
        validators=(
            MinValueValidator(1, 'Минимальная оценка %(limit_value)s.'),
            MaxValueValidator(10, 'Максимальная оценка %(limit_value)s.'),
        )
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = (
            models.UniqueConstraint(
                fields=('title', 'author', ),
                name='unique review'
            ),
        )

    def __str__(self):
        return self.text[:20]


class Comment(CreatedModel):
    """Модель комментария."""

    text = models.TextField(
        verbose_name='Текст комментария:',
        help_text='Текст вашего комментария'
    )
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:20]
