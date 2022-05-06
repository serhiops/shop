from django.test import TestCase
from myshop.models import CustomUser, Product, Category
from django.utils.text import slugify

class ProductAPITestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        salesman = CustomUser.objects.create(username = "salesman", 
                                            company = "company_name", 
                                            is_salesman = True, 
                                            email = "salo@gmail.com", 
                                            password  = "159753_qazwsx")

        category = Category.objects.create(name = "category название",
                                            description = "description",
                                            slug = "asdqwe")

        Product.objects.create(name = "Товар /*фы//'+_.,48qw\s",
                                description = "descrition",
                                price_currency = 'UAH',
                                price = "159.45",
                                salesman = salesman,
                                category = category)

    def test_productSlug(self):
        product = Product.objects.get(pk = 1)
        self.assertEqual(product.slug, slugify("Товар /*фы//'+_.,48qw\s"))

    def test_changeProductSlug(self):
        product = Product.objects.get(pk = 1)
        product.title = "New title"
        product.save()
        self.assertEqual(product.slug, slugify("Товар /*фы//'+_.,48qw\s"))

    def test_sameProduct(self):
        salesman = CustomUser.objects.create(username = "salesman1", company = "company_name", is_salesman = True, email = "salo1@gmail.com", password  = "159753_qazwsx")
        category = Category.objects.create(name = "category название",description = "description",slug = "asdqwea")
        product = Product.objects.create(name = "Товар /*фы//'+_.,48qw\s",description = "descrition",price_currency = 'UAH',price = "159.45",salesman = salesman,category = category)
        product1 = Product.objects.get(pk = 1)
        self.assertNotEqual(product.slug, product1.slug)

    