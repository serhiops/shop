from rest_framework.test import APITestCase
from myshop.models import CustomUser, Ordering, Product, Category
from django.urls import reverse

class OrdderingTest(APITestCase):

    def __init__(self, methodName):
        self.url = reverse('myshop:create-ordering')
        super().__init__(methodName)

    @classmethod
    def setUpTestData(cls):
        Product.objects.create(name = 'test_name product */_13 \|',
                                description = 'test description',
                                price = 125.15,
                                salesman = CustomUser.objects.create(
                                    username='testuser', 
                                    password='12345',
                                ),
                                category = Category.objects.create(
                                    name = 'test_category',
                                    description = 'test category description',
                                    slug = 'test_category',
                                 ))

    def test_createOrdering(self):
        self.client.post(self.url, data = {'salesman':CustomUser.objects.last().id, 'product':Product.objects.last().id, 
                                            'post_office':'test post office', 'city':'test city', 'number':1})
        self.assertTrue(bool(Ordering.objects.filter(city = 'test city')), msg='Order not create')

    