from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()


class SubCategory(models.Model):
    category = models.ForeignKey(Category, related_name='sub_categories', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField()


class Profile(models.Model):
    telegram_id = models.CharField(max_length=100, unique = True)
    ref_slug = models.URLField(max_length=200, unique = True)
    referal = models.ForeignKey('self', related_name = 'referals', null=True, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='category_users', null=True, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, related_name='subcategory_users',null=True, on_delete=models.CASCADE)
