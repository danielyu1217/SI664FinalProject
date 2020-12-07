from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.conf import settings


class Category(models.Model) :
    name = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(2, "name must be greater than 2 characters")]
    )
    def __str__(self):
        return self.name


class Price(models.Model) :
    value = models.CharField(
            max_length=4,
            validators=[MinLengthValidator(1, "value: $ $$ $$$ $$$$")]
    )
    def __str__(self):
        return self.value


class Tag(models.Model) :
    name = models.CharField(
            max_length=20,
            validators=[MinLengthValidator(2, "name must be greater than 2 characters")]
    )
    def __str__(self):
        return self.name


class Restaurant(models.Model) :
    name = models.CharField(
            max_length=20,
            validators=[MinLengthValidator(2, "Name must be greater than 2 characters")]
    )
    description = models.TextField(null=True, blank=True)
    location = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(2, "Location must be greater than 2 characters")],
            blank=True
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='sub_res')
    tag1 = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True, blank=True, related_name='tag_1')
    tag2 = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True, blank=True, related_name='tag_2')
    tag3 = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True, blank=True, related_name='tag_3')
    rating = models.IntegerField(
             validators=[MinValueValidator(0, "rating >= 0"),
             MaxValueValidator(10, "rating <= 10")])
    price = models.ForeignKey(Price, on_delete=models.SET_NULL, null=True, blank=True)
    comments = models.ManyToManyField(settings.AUTH_USER_MODEL,
        through='Comment', related_name='res_comments')

    # pictures
    pic1 = models.ImageField(upload_to='images/')
    pic2 = models.ImageField(upload_to='images/')
    pic3 = models.ImageField(upload_to='images/')

    # Favorites
    favorites = models.ManyToManyField(settings.AUTH_USER_MODEL,
        through='Fav', related_name='favorite_restaurants')

    def __str__(self):
        return self.name


class Comment(models.Model) :
    text = models.TextField(
        validators=[MinLengthValidator(3, "Comment must be greater than 3 characters")]
    )
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Shows up in the admin list
    def __str__(self):
        if len(self.text) < 15 : return self.text
        return self.text[:11] + ' ...'


class Fav(models.Model) :
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # https://docs.djangoproject.com/en/3.0/ref/models/options/#unique-together
    class Meta:
        unique_together = ('restaurant', 'user')

    def __str__(self) :
        return '%s likes %s'%(self.user.username, self.restaurant.title[:10])


