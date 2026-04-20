from django.db import models

# class Category(models.Model):
#     name = models.CharField(max_length=255)
#     slug = models.SlugField(unique=True)

#     parent = models.ForeignKey(
#         'self',
#         null=True,
#         blank=True,
#         on_delete=models.CASCADE,
#         related_name='children'
#     )

#     def __str__(self):
#         return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock =models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
        
    # additional maybe use
    # category = models.