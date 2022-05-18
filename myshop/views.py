from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy

from .models import Product, Category,FavoriteProducts,CustomUser, Ip, Ordering, Mark, Photo, Rating
from . import forms
from django.contrib.auth import login, logout,authenticate
from django.core.mail import send_mail
from django.views.generic import UpdateView, ListView, FormView, DetailView
from django.contrib import messages
from django.db.models import Q, Avg
from django.core.files.base import ContentFile
from .additionally import func
from django.views.generic.edit import FormView
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import user_passes_test
from .permissions import permissions


class Index(ListView, FormView):
    form_class = forms.Filter
    queryset = Category.objects.all()
    template_name = "myshop/index.html"
    context_object_name = "categories"
    success_url = reverse_lazy("myshop:index")

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["title"] = "Главная страница"
        context["side"] = True
        return context

    def form_valid(self, form):
        products = Product.objects.filter(name__icontains = form.cleaned_data["text"])
        if products.count()<1:
                messages.error(self.request, "По запросу " + form.cleaned_data["text"] + " ничего не найдено:(")
                return super().form_valid(form)
        elif products.count()==1:
            messages.success(self.request, "По запросу " + form.cleaned_data["text"] + f" найдено {products.count()} товар!")
        else:
            messages.success(self.request, "По запросу " + form.cleaned_data["text"] + f" найдено {products.count()} товаров!")
        return render(self.request, "myshop/filter_products.html", {"products":products})

    def form_invalid(self, form):
        func.get_error_messages(self.request, form)
        return redirect('myshop:index')

class ByCategory(ListView, FormView):
    form_class = forms.DetailFilter
    context_object_name = "products"
    template_name = "myshop/by_category.html"
    
    def get_queryset(self):
        return Product.objects.filter(category__slug = self.kwargs["cat_slug"], is_active = True)

    def form_valid(self, form):
        begin_price = form.cleaned_data["begin_price"]
        end_price = form.cleaned_data["end_price"]
        if len(form.cleaned_data["city"]) == 0:
            products = Product.objects.filter(Q(price__gte = begin_price)&Q(price__lte = end_price)&Q(category__slug = self.kwargs["cat_slug"]))
        else:
            products = Product.objects.filter(Q(salesman__city__icontains = form.cleaned_data["city"])&Q(price__gte = begin_price)&Q(price__lte = end_price)&Q(category__slug = self.kwargs["cat_slug"]))
        if products.count() > 0:
            messages.success(self.request, f"По вашему запросу найдено {products.count()} товаров")
        else:
            messages.error(self.request,"По такому запросу ничего не найдено:(")
        return render(self.request, "myshop/by_category.html", {"products":products,"form":self.get_form(),"detail_filterjs":True, "category":Category.objects.all()})

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context

    def form_invalid(self, form):
        func.get_error_messages(self.request, form)
        return super().form_invalid(form)        

class ProductDetail(DetailView):
    template_name = "myshop/react_pages/detail/index.html"
    context_object_name = "product"
    model = Product

    def get_object(self):
        return Product.objects.get(pk = self.kwargs["prod_pk"], is_active = True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context["categories"] = Category.objects.all()
        if not self.request.user.is_authenticated:
            context["is_bought"] = False
        else:
            context["is_bought"] = Ordering.objects.filter(user = self.request.user, product = product)
        context['react_detail'] = True
        context['product'] = product
        return context

    def get(self, request, *args, **kwargs):
        ip = func.get_client_ip(request)
        if Ip.objects.filter(ip=ip).exists():
            self.get_object().views.add(Ip.objects.get(ip=ip))
        else:
            Ip.objects.create(ip=ip)
            self.get_object().views.add(Ip.objects.get(ip=ip))  
        return super().get(request, *args, **kwargs)

class FavoriteProductsList(permissions.AuthenticatedOnlyPermission,permissions.DefaultUserOnlyPermission,ListView):
    template_name = "myshop/favorite_products.html"
    context_object_name = "fav_pr"

    def get_queryset(self):
        return CustomUser.objects.get(username = self.request.user.username).get_fp.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["createroomjs"] = True
        return context

class Register(permissions.AuthenticatedOnlyPermission, FormView):
    form_class = forms.CustomUserCreationForm
    template_name = "myshop/auth/registr.html"
    success_url = reverse_lazy("myshop:register_code")

    def form_valid(self, form):
        code = func.generate_code()
        user = form.save()
        user.is_active = False
        user.code = code
        user.save()
        send_mail('Лист від сайта новин.',
                f'Дякую вас за те, що ви зареєструвалися на моему на сайті! Якщо у вас виникнуть якісь питання чи побажання щодо покращення сайту, то ви можете звернутися до мене у розділі "Зворотній звєязок" або відправити листа на цю пошту!{code}',
                'serrheylitvinenko@gmail.com',
                [form.cleaned_data["email"]],
                fail_silently=False)
        return super().form_valid(form)

    def form_invalid(self, form):
        func.get_error_messages(self.request, form)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.path != "/register/":
            context["salesman_register"] = True
        else:
            context["salesman_register"] = False
        context["categories"] = Category.objects.all()
        return context

def register_code(request):
    if request.method == 'POST':
        form = forms.CustomUserCreationCodForm(request.POST)
        if form.is_valid():
            code_use = form.cleaned_data.get("code")
            user = CustomUser.objects.get(code=code_use)
            try:
                user.is_active = True
                user.save()
                login(request, user)
                return redirect("myshop:index")
            except:
                messages.error(request, "Произошла ошибка!")
        else:
            messages.error(request, form.errors.as_text().replace("*",""))
    else:
        form = forms.CustomUserCreationCodForm()
    context = {
        "form":form,
        "side":True,
    }
    return render(request, "myshop/auth/registr_code.html", context)

class Login(FormView):
    template_name = "myshop/auth/login.html"
    form_class = forms.UserLoginForm
    success_url = reverse_lazy("myshop:index")

    def form_valid(self, form):
        try:
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(self.request, user)
            return super().form_valid(form)
        except:
            messages.error(self.request, "Пароль или логин не совпадают")
            return redirect("myshop:login")

    def form_invalid(self, form):
        func.get_error_messages(self.request, form)
        return redirect("myshop:login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["loginjs"] = True
        return context

def user_logout(request):
    logout(request)
    return redirect("myshop:index")

def user_profile(request):
    categories = Category.objects.all()
    user = CustomUser.objects.get(username = request.user.username)
    backorders_count = Ordering.objects.filter(salesman = request.user, is_done = False, is_take = False).count()
    active_oders_count = Ordering.objects.filter(user = request.user, is_done = False).count()
    context = {
        "user":user,
        "categories":categories,
        "backorders_count":backorders_count,
        "active_oders_count":active_oders_count,
        "changeUserDatajs":True
    }
    return render(request,"myshop/user_profile.html", context)

@user_passes_test(lambda user: not user.is_salesman, login_url=reverse_lazy('myshop:index'), redirect_field_name=None)
def user_orders(request):
    orders = Ordering.objects.filter(user = request.user, is_done = True)
    context = {
        "orders":orders
    }
    return render(request, "myshop/user_orders.html", context)

@user_passes_test(lambda user: not user.is_salesman, login_url=reverse_lazy('myshop:index'), redirect_field_name=None)
def user_active_oders(request):
    orders = Ordering.objects.filter(user = request.user, is_done = False)
    context = {
        "orders":orders,
    }
    return render(request, "myshop/user_active_oders.html", context)

def set_unactive(request,slug_pr):
    product = get_object_or_404(Product, slug = slug_pr)
    if product.salesman == request.user:
        product.is_active = False
        product.save(update_fields=["is_active"])
        return redirect("myshop:statistic")
    else:
        return redirect('myshop:index')

def set_active(request, slug_prd):
    product = get_object_or_404(Product, slug = slug_prd)
    if product.salesman == request.user:
        product.is_active = True
        product.save(update_fields=["is_active"])
        return redirect("myshop:statistic")
    else:
        return redirect('myshop:index')

def change_email(request):
    if request.method == 'POST':
        form = forms.ChangeEmail(request.POST,instance = request.user)
        if form.is_valid():
            if form.has_changed():
                code = func.generate_code()
                request.user.code = code
                request.user.email = form.cleaned_data["email"]
                request.user.save()
                send_mail('Лист від сайта новин.',
                        f'Дякую вас за те, що ви зареєструвалися на моему на сайті! Якщо у вас виникнуть якісь питання чи побажання щодо покращення сайту, то ви можете звернутися до мене у розділі "Зворотній звєязок" або відправити листа на цю пошту!{code}',
                        'serrheylitvinenko@gmail.com',
                        [form.cleaned_data["email"]],
                        fail_silently=False
                )
                return redirect("myshop:register_code")
            else:
                messages.error(request, "Вы ввели ту же почту!")
                return redirect("change_email")
        else:
            messages.error(request, form.errors.as_text().replace("*",""))
    else:
        form = forms.ChangeEmail()
    context = {
        "form":form
    }
    return render(request, "myshop/change_gmail_form.html", context)

def delete_fav_pr(request, pk_fp):
    try:
        object = FavoriteProducts.objects.get(pk = pk_fp)
        messages.success(request, f"{object.product.name} удален из вашей корзины!")
        object.delete()
    except:
        messages.error(request, "Произошла ошибка!")
    return redirect("myshop:favorite_products")

class AddProduct(permissions.SalesmanOnlyPermission,FormView):
    form_class = forms.AddProductForm
    template_name = "myshop/add_product.html"

    def form_valid(self, form):
        form.cleaned_data['salesman'] = self.request.user
        product = Product.objects.create(salesman =form.cleaned_data['salesman'], 
                                        price = form.cleaned_data['price'],
                                        category = form.cleaned_data['category'], 
                                        description = form.cleaned_data["description"],
                                        name =form.cleaned_data["name"]  )
        for f in self.request.FILES.getlist('image'):
            data = f.read() 
            photo = Photo(product=product)
            photo.image.save(f.name, ContentFile(data))
            photo.save()
        messages.success(self.request, "Товар успешно добавлен!")
        return redirect(product)

    def form_invalid(self, form):
        func.get_error_messages(self.request, form)
        return super().form_invalid(form)

@user_passes_test(lambda user: user.is_salesman, login_url=reverse_lazy('myshop:index'), redirect_field_name=None)
def statistic(request):
    categories = Category.objects.all()
    products = Product.objects.filter(salesman = request.user)

    views_list = func.get_views_array(products)

    much_fp = FavoriteProducts.objects.filter(salesman = request.user).count()
    orderings = Ordering.objects.filter(salesman = request.user).count()
    done_orderings = Ordering.objects.filter(salesman = request.user, is_done = True).count()
    count_likes = Mark.objects.filter(product__salesman = request.user, like = True).count()
    count_dislikes = Mark.objects.filter(product__salesman = request.user, dislike = True).count()
    rating = Rating.objects.filter(product__salesman = request.user).aggregate(average = Avg('rating'))["average"]

    context = {
        "much_views":sum(views_list),
        "much_fp":much_fp,
        "products":products,
        "max_views":max(views_list),
        "min_views":min(views_list),
        "orderings":orderings,
        "categories":categories,
        "done_orderings":done_orderings,
        "count_likes":count_likes,
        "count_dislikes":count_dislikes,
        "rating":rating,
        "statisticjs":True
    }

    return render(request, "myshop/statistic.html", context)

@user_passes_test(lambda user: user.is_salesman, login_url=reverse_lazy('myshop:index'), redirect_field_name=None)
def detail_statistic(request, slug_pr):
    product = get_object_or_404(Product, slug = slug_pr)
    much_fp = FavoriteProducts.objects.filter(salesman = request.user , product =product).count()
    orderings = Ordering.objects.filter(salesman = request.user, product = product).count()
    done_orderings = Ordering.objects.filter(salesman = request.user, product = product, is_done = True).count()
    rating = Rating.objects.filter(product = product).aggregate(average = Avg('rating'))["average"]
    context = {
        "product":product,
        "much_fp":much_fp,
        "orderings":orderings,
        "done_orderings":done_orderings,
        "rating":rating,
    }
    return render(request, "myshop/detail_statistic.html", context)

@user_passes_test(lambda user: not user.is_salesman, login_url=reverse_lazy('myshop:index'), redirect_field_name=None)
def ordering(request, pk_sal, slug_prod):
    salesman = get_object_or_404(CustomUser, is_salesman = True,pk = pk_sal)
    product = get_object_or_404(Product, slug = slug_prod)
    if request.method == "POST":
        form = forms.OrderingForm(request.POST)
        if form.is_valid():
            post_office = form.cleaned_data["post_office"]
            number = form.cleaned_data['number']
            Ordering.objects.create(user = request.user, salesman = salesman, product=product, post_office = post_office, number = number)
            send_mail('Новый заказ!',
                    f'Добрый день, {salesman.first_name} {salesman.last_name}! Только что у вас заказали {product.name} в город {request.user.city}, отделение почты - {post_office.name}, количиство - {number}.Контактный номер : {request.user.number_of_phone}',
                    'serrheylitvinenko@gmail.com',
                    [salesman.email],
                    fail_silently=False
                )
            messages.success(request, "Вы цспешно оформили заказ! Продавец свяжется с вами в скором времени.")
            return redirect("myshop:index")
        else:
            messages.success(request, "Произошла ошибка")
    else:
        form = forms.OrderingForm()
    context = {
        "salesman":salesman,
        "product":product,
        "form":form,
        "ChangeOrderingDatajs":True ,
    }
    return render(request, "myshop/ordering.html", context)

def set_done(request,pk_ord):
    ordering = get_object_or_404(Ordering, pk = pk_ord)
    if(ordering.user == request.user):
        ordering.is_done = True
        ordering.save(update_fields=["is_done"])
        return redirect("myshop:user_orders")
    else:
        return redirect('myshop:index')

@user_passes_test(lambda user: user.is_salesman, login_url=reverse_lazy('myshop:index'), redirect_field_name=None)
def backorders(request):
    products = Ordering.objects.filter(salesman = request.user, is_done = False, is_take = False, is_sent = False)
    context = {
        "products":products,
        "title":"Заказы",
        "step":0,
        'product_sendingjs':True
    }
    return render(request, "myshop/product_sending.html", context)

@user_passes_test(lambda user: user.is_salesman, login_url=reverse_lazy('myshop:index'), redirect_field_name=None)
def completed_orders(request):
    products = Ordering.objects.filter(salesman = request.user, is_done = True, is_sent = True)
    context = {
        "products":products,
        "title":"Выполненные заказы",
    }
    return render(request, "myshop/product_sending.html", context)

@user_passes_test(lambda user: user.is_salesman, login_url=reverse_lazy('myshop:index'), redirect_field_name=None) 
def accepted_products(request):
    products = Ordering.objects.filter(salesman = request.user, is_done = False, is_take = True, is_sent = False)
    wait_products = Ordering.objects.filter(salesman = request.user, is_done = False, is_take = True, is_sent = True)
    context = {
        "products":products,
        "title":"Принятые товары",
        "wait_products":wait_products,
        "step":1,
        'product_sendingjs':True
    }
    return render(request, "myshop/product_sending.html", context)

class ChangeProduct(permissions.SalesmanOnlyPermission,UpdateView):
    model = Product
    template_name = "myshop/change_product.html"
    fields = ["name", "description", "price"]
    success_url = reverse_lazy("myshop:statistic")
    slug_url_kwarg = "slug_pr"

    def get_form(self, *args, **kwargs):
        form = super(ChangeProduct, self).get_form(*args, **kwargs)
        form.fields["name"].widget.attrs["class"] = "form-control"
        form.fields["description"].widget.attrs["class"] = "form-control"
        form.fields["price"].widget.attrs["class"] = "form-control"
        return form 

    def form_invalid(self, form):
        func.get_error_messages(self.request, form)
        return super().form_invalid(form)

def salesman_profile(request, salesman_slug):
    salesman = get_object_or_404(CustomUser, username = salesman_slug)
    products = Product.objects.filter(salesman = salesman)
    products_count = products.count()
    rating = Rating.objects.filter(product__salesman = salesman).aggregate(average = Avg("rating"))["average"]
    done_orderings = Ordering.objects.filter(salesman = salesman, is_done = True).count()
    context = {
        "salesman":salesman,
        "products":products,
        "rating":rating,
        "done_orderings":done_orderings,
        "products_count":products_count
    }
    return render(request, "myshop/salesman_profile.html", context)

class ChangePassword(PasswordChangeView):
    template_name = "myshop/change_password.html"

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields["old_password"].widget.attrs["class"] = "form-control"
        form.fields["new_password1"].widget.attrs["class"] = "form-control"
        form.fields["new_password2"].widget.attrs["class"] = "form-control"
        return form

    def form_invalid(self, form):
        func.get_error_messages(self.request, form)
        return super().form_invalid(form)

    def form_valid(self, form):
        if form.cleaned_data["old_password"] == form.cleaned_data["new_password1"] == form.cleaned_data["new_password2"]:
            messages.error(self.request, "У вас в данный момент такой же пароль!")
            return redirect("myshop:change_password")
        messages.success(self.request, "Вы успешно сменили пароль!")
        return super().form_valid(form)

class PasswordReset(SuccessMessageMixin,PasswordResetView):
    """Изменение пароля с почтой"""
    template_name = "myshop/reset_password.html"
    subject_template_name = "myshop/reset_password/reset_subject.txt"
    email_template_name = "myshop/reset_password/reset_text.txt"
    from_email = "serrheylitvinenko@gmail.com"
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy("myshop:index")

    def get_form(self, *args, **kwargs):
        form =  super().get_form(*args, **kwargs)
        form.fields["email"].widget.attrs["class"] = "form-control"
        return form 

class PasswordResetConfirm(SuccessMessageMixin, PasswordResetConfirmView):
    template_name = "myshop/reset_password/password_confirm.html"
    success_message = "Вы успешно изменили пароль"
    success_url = reverse_lazy("myshop:login")

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields["new_password1"].widget.attrs["class"] = "form-control"
        form.fields["new_password2"].widget.attrs["class"] = "form-control"
        return form
