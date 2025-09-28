from django.db import models
from django.db.models import CASCADE
from django.db.models import Avg
from django.utils.text import slugify
from django_resized import ResizedImageField
from django.contrib.auth import get_user_model

User = get_user_model()


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True




class Category(BaseModel):
    title = models.CharField(max_length=255, unique=True)
    image = ResizedImageField(size=[300, 300], crop=['middle', 'center'], upload_to='category_images/')
    slug = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def get_absolute_url(self):
        if self.image:
            return self.image.url
        return ''

    class Meta:
        verbose_name_plural = 'Categories'




class Product(BaseModel):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=14, decimal_places=2)
    image = models.ImageField(upload_to='product_images/')
    category = models.ForeignKey(Category, related_name='products', on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    @property
    def avg_rating(self):
        return self.comments.aggregate(Avg('rating'))['rating__avg'] or 0

    @property
    def get_image_url(self):
        if self.image:
            return self.image.url
        return ''

    class Meta:
        ordering = ['-created_at']




class ProductImage(BaseModel):
    image = models.ImageField(upload_to='product_images/')
    product = models.ForeignKey(Product, related_name='images', on_delete = CASCADE)

    def __str__(self):
        return self.image.url




class Comment(BaseModel):
    class RatingChoices(models.IntegerChoices):
        ONE   = 1,    '★☆☆☆☆'
        TWO   = 2,    '★★☆☆☆'
        THREE = 3,    '★★★☆☆'
        FOUR  = 4,    '★★★★☆'
        FIVE  = 5,    '★★★★★'

    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    rating = models.IntegerField(choices=RatingChoices.choices, default=RatingChoices.THREE)

    def __str__(self):
        return f'{self.name} - {self.rating}'


class CartItem(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.email} - {self.product.name} x{self.quantity}"

    @property
    def total_price(self):
        return self.product.price * self.quantity

    class Meta:
        unique_together = ['user', 'product']
        ordering = ['-created_at']


class Like(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return f"{self.user.email} likes {self.product.name}"

    class Meta:
        unique_together = ['user', 'product']
        ordering = ['-created_at']