from rest_framework.test import APITestCase
from myshop.models import CustomUser, Product, Category
from chat.models import Room

class RoomApiTest(APITestCase):

    def __init__(self, methodName):
        self.urlRoom = '/chat/api/v1/rooms/'
        self.urlMessage = '/chat/api/v1/messages/'
        self.defaultUser = CustomUser.objects.get(pk = 1)
        super().__init__(methodName)

    @classmethod 
    def setUpTestData(cls):
        Product.objects.create(name = 'test_name product',
                                description = 'test description',
                                price = 125.15,
                                salesman = CustomUser.objects.create(
                                    username='testuser_salesman', 
                                    password='12345',
                                    is_salesman = True
                                ),
                                category = Category.objects.create(
                                    name = 'test_category',
                                    description = 'test category description',
                                    slug = 'test_category',
                                 ))
    def createRoom(self):
        self.client.post(self.urlRoom, data={'product':Product.objects.last().id})

    def test_createRoom(self): 
        self.createRoom()
        self.assertEqual(Room.objects.last().product, Product.objects.last())
        self.assertEqual(Room.objects.last().user,self.defaultUser)
        self.assertEqual(Room.objects.last().salesman, CustomUser.objects.last())
    

