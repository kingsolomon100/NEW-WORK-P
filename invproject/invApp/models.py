from django.db import models 
from django.db.models import F 
from django.conf import settings 
from django.core.validators import MinValueValidator 


class Product(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete= models.CASCADE, 
        related_name= 'products'
    )

    product_id = models.BigAutoField(
        primary_key= True, 
        help_text= 'Unique identifier product ID'
    )

    name = models.CharField(
        max_length= 100, 
        verbose_name= 'Product',
        help_text= 'Enter the full commercial name of product'
    )

    sku = models.CharField(
        max_length= 50, 
        verbose_name= 'SKU', 
        help_text= 'Unique store keeping units(eg. 237y)'
    )

    price = models.DecimalField(
        decimal_places= 2, 
        max_digits= 10,
        validators= [MinValueValidator(0.01)], 
        help_text= 'Set the price in minimum of 0.01(eg.123)'
    )

    quantity = models.PositiveIntegerField(
        help_text= 'Enter Current quantity stored in the warehouse'
    )

    supplier = models.CharField(
        max_length= 100,
        verbose_name= 'Enter the primary vendor name'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name_plural = 'Products'
        constraints = [
            models.UniqueConstraint(fields=['user', 'sku'], name= 'unique_user_sku')
        ]

    def __str__(self):
        return f"{self.user}, ({self.sku})"

    @classmethod 
    def add_or_update_product(cls, user, sku, quantity_to_add, defaults_dict):
        defaults_dict.update({'quantity': quantity_to_add})

        product, created = cls.objects.update_or_create(
            user=user, 
            sku=sku, 
            defaults= defaults_dict
        ) 

        if not created:
            product.quantity = F('quantity') + quantity_to_add 
            product.save(update_fields=['updated_at', 'quantity'])
            product.refresh_from_db()   
        return product    