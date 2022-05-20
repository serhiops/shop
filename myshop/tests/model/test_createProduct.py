from django.test import TestCase
from myshop.models import Product, CustomUser, Category
from django.utils.text import slugify

class TestProductModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        Product.objects.create(name = 'test_name product */_13 \|',
                                description = 'test description',
                                price = 125.15,
                                salesman = CustomUser.objects.create(
                                    username='testuser', 
                                    password='12345',
                                    is_salesman = True,
                                ),
                                category = Category.objects.create(
                                    name = 'test_category',
                                    description = 'test category description'
                                ))

    def test_productSlug(self):
        self.assertEqual(Product.objects.last().slug, slugify('test_name product */_13 \|'))

    def test_productSlugisUnique(self):
        new_product = Product.objects.create(name = 'test_name product */_13 \|',description = 'test description',
                                            price = 125.15, salesman = CustomUser.objects.last(), category = Category.objects.last())
        self.assertNotEqual(new_product.slug, Product.objects.get(pk = 1).slug)
