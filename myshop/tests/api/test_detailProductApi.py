from rest_framework.test import APITestCase
from myshop.models import CustomUser,Product, Category, Mark,Rating,Coments
from django.urls import reverse

class DetailProductTest(APITestCase):

    def __init__(self, methodName):
        self.urlRating = reverse('myshop:rating-api')
        self.urlCommentPush = reverse('myshop:coment-list-api')
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


    def getUrlMark(self):
        return reverse('myshop:detail-product-api', args=(Product.objects.last().id,))

    def getProduct(self):
        return Product.objects.last()

    def getUser(self):
        return CustomUser.objects.last()

    def getUrlDetailComent(self):
        return reverse('myshop:detail-coment', args=(Product.objects.last().id,))
    

    def test_setLike(self):
        self.client.post(self.getUrlMark(), data={'like':True})

        self.assertTrue(Mark.objects.last().like)
        self.assertFalse(Mark.objects.last().dislike)
        self.assertEqual(Mark.objects.last().user, self.getUser())

    def test_setDislike(self):
        self.client.post(self.getUrlMark(), data={'dislike':True})

        self.assertTrue(Mark.objects.last().dislike)
        self.assertFalse(Mark.objects.last().like)
        self.assertEqual(Mark.objects.last().user, self.getUser())

    def test_deleteLike(self):
        self.client.post(self.getUrlMark(), data={'like':True})
        self.client.post(self.getUrlMark(), data={'like':True})

        self.assertIsNone(Mark.objects.last())

    def test_deleteDislike(self):
        self.client.post(self.getUrlMark(), data={'dislike':True})
        self.client.post(self.getUrlMark(), data={'dislike':True})

        self.assertIsNone(Mark.objects.last())

    def test_changeLikeToDislike(self):
        self.client.post(self.getUrlMark(), data={'like':True})
        self.client.post(self.getUrlMark(), data={'dislike':True})

        self.assertTrue(Mark.objects.last().dislike)
        self.assertFalse(Mark.objects.last().like)
        self.assertEqual(Mark.objects.last().user, self.getUser())

    def test_changeDislikeToLike(self):
        self.client.post(self.getUrlMark(), data={'dislike':True})
        self.client.post(self.getUrlMark(), data={'like':True})

        self.assertTrue(Mark.objects.last().like)
        self.assertFalse(Mark.objects.last().dislike)
        self.assertEqual(Mark.objects.last().user, self.getUser())

    
    def test_setRating(self):
        self.client.post(self.urlRating, data={'product':self.getProduct().id, 'rating':2})

        self.assertEqual(Rating.objects.last().rating, 2)
        self.assertEqual(Rating.objects.last().user, self.getUser())

    def test_changeRating(self):
        self.client.post(self.urlRating, data={'product':self.getProduct().id, 'rating':4})
        self.client.post(self.urlRating, data={'product':self.getProduct().id, 'rating':2})

        self.assertEqual(Rating.objects.last().rating, 2)
        self.assertEqual(Rating.objects.last().user, self.getUser())

    def test_deleteRating(self):
        self.client.post(self.urlRating, data={'product':self.getProduct().id, 'rating':5})
        self.client.post(self.urlRating, data={'product':self.getProduct().id, 'rating':5})

        self.assertIsNone(Rating.objects.last())

    def test_incorrectNumberRating(self):
        self.client.post(self.urlRating, data={'product':self.getProduct().id, 'rating':100})
        self.client.post(self.urlRating, data={'product':self.getProduct().id, 'rating':-100})

        self.assertIsNone(Rating.objects.last())

    
    def test_addComment(self):
        self.client.post(self.urlCommentPush, data={'text':'test comment text','product':self.getProduct().id})

        self.assertEqual(Coments.objects.last().text , 'test comment text')
        self.assertEqual(Coments.objects.last().author, self.getUser())

    def test_changeComment(self):
        self.client.post(self.urlCommentPush, data={'text':'test comment text','product':self.getProduct().id})
        self.client.patch(self.getUrlDetailComent(), data = {'text':'New nice text'})

        self.assertEqual(Coments.objects.last().text, 'New nice text')

    def test_deleteComent(self):
        self.client.post(self.urlCommentPush, data={'text':'test comment text','product':self.getProduct().id})
        self.client.delete(self.getUrlDetailComent())

        self.assertFalse(bool(Coments.objects.all()))

    



       
