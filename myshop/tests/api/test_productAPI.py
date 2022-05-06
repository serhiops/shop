from rest_framework.test import APITestCase
from myshop.models import Category, CustomUser, Product
from myshop.serializers import ProductSerializer

URL_PRODUCT = "/api/v1/product/"

class ProductAPITestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        print("as")
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
        

    def test_getData(self):
        serializer_data = ProductSerializer(Product.objects.all(), many = True).data
        request_data = self.client.get(URL_PRODUCT).data
        self.assertEqual(serializer_data, request_data)

    

        

    