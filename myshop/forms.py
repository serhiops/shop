from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Coments, Product, Ordering
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField
from moneyed import Money, UAH

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    captcha = CaptchaField()
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ['username', 'first_name', "last_name","age", "number_of_phone", "city", "password1", "password2", "is_salesman", "email", "company"]
        widgets = {
            "username":forms.TextInput(attrs={
                "class":"form-control"
            }),
            "first_name":forms.TextInput(attrs={
                "class":"form-control"
            }),
            "last_name":forms.TextInput(attrs={
                "class":"form-control"
            }),
            "number_of_phone":forms.TextInput(attrs={
                "class":"form-control",
                "placeholder":"+380123456789",
                "type":"number"
            }),
            "age":forms.TextInput(attrs={
                "class":"form-control", 
                "type":"number"
            }),
            "city":forms.TextInput(attrs={
                "class":"form-control"
            }),
            "email":forms.EmailInput(attrs={
                "class":"form-control"
            }),
            "company":forms.TextInput(attrs={
                "class":"form-control"
            })
        }
        help_texts = {"username":"Должно состоять только из латинских букв."}

    def clean_number_of_phone(self):
        number_of_phone = self.cleaned_data["number_of_phone"]
        if len(number_of_phone) == 9:
            raise ValidationError("Вам стоит добавить код страны!")
        elif len(number_of_phone)<12:
            raise ValidationError("Этот номер телефона не подходит!")
        return number_of_phone

    def clean_age(self):
        age = self.cleaned_data["age"]
        if int(age)<13:
            raise ValidationError("Вы еще слишком малы!")
        return age

class CustomUserCreationCodForm(forms.Form):
    code = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))


class ChangeEmail(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)
        widgets = {"email":forms.EmailInput(attrs={"class":"form-control"})}


class Filter(forms.Form):
    text = forms.CharField(max_length=32, widget=forms.TextInput(attrs={"class":"form-control me-2", "type":"search", "placeholder":"Search", "aria-label":"Search"}))

    def clean_text(self):
        text = self.cleaned_data["text"]
        if len(text)<3:
            raise ValidationError("Слово должно состоять минимум из 3 букв.")
        return text


class ComentForm(forms.ModelForm):
    class Meta:
        model = Coments
        fields = ("text", )
        widgets = {
            "text":forms.Textarea(attrs={
                "class":"form-control",
                "placeholder":"Будьте вежливы и соблюдайте принципы сообщества",
                "rows":5,
                "id":"comentText"
            }),
        }

class AddProductForm(forms.ModelForm):
    image = forms.ImageField(label=u'Фотографии', widget=forms.FileInput(attrs={'multiple': 'multiple'}))
    class Meta:
        model = Product
        fields = ("name","description","price","category")
        widgets = {
            "name":forms.TextInput(attrs={
                "class":"form-control",
            }),
            "description":forms.Textarea(attrs={
                "class":"form-control",
            }),
            #"price":forms.Select(attrs={
            #   "class":"form-control",
            #}), 
            "category":forms.Select(attrs={
                "class":"form-control",
            })
        }

    def clean_description(self):
        description = self.cleaned_data["description"]
        if len(description)<50:
            raise ValidationError("Описание слишком короткое, опишите свой товар получше!")
        elif len(description.split())<10:
            raise ValidationError("Описание состоит из слишком малого количества слов, опишите свой товар получше!")
        return description

    def clean_price(self):
        price = self.cleaned_data["price"]
        if price < Money("0", UAH):
            raise ValidationError("Я сомневаюсь, что вы хотите выставить товар за отрицательную цену:)")
        return price

class OrderingForm(forms.ModelForm):
    class Meta:
        model = Ordering
        fields = ("post_office", "number")
        widgets = {
            "post_office":forms.Select(attrs={
                "class":"form-control",
            }),
            "number":forms.TextInput(attrs={
                "class":"form-control",
                "type":"number"
            })
        }

class DetailFilter(forms.Form):
    city = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "id":"cityInput"}), required=False)
    begin_price = forms.IntegerField(widget=forms.TextInput(attrs={"class":"form-control", "id":"begin_priceInput", "type":"number"}), required=False)
    end_price = forms.IntegerField(widget=forms.TextInput(attrs={"class":"form-control", "id":"end_priceInput", "type":"number"}), required=False)

    def clean_end_price(self):
        end_price = self.cleaned_data["end_price"]
        if end_price == None:
            end_price = Product.objects.filter(price__gte = self.cleaned_data["begin_price"]).values("price")
            max = end_price[0]["price"]
            for i in end_price:
                if i["price"] > max:
                    max = i["price"]
            return max                
        return end_price

    def clean_begin_price(self):
        begin_price = self.cleaned_data["begin_price"]
        if begin_price == None:
            return Money("0", UAH)
        max_price = max(Product.objects.filter(is_active = True).values_list("price"))
        if Money(max_price[0], UAH) < Money(begin_price, UAH):
            begin_price = max_price
        return begin_price

    def clean_city(self):
        city = self.cleaned_data["city"]
        if len(city) <3 and len(city) >0:
            raise ValidationError("Слишком короткое название населенного пункта!")
        return city


