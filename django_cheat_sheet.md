# Django cheat sheet

## Setup a Django Project

### Create a Github project

https://github.com/tonper19

### Move to the Development folder and clone the Github project locally

```zsh
git clone git@github.com:tonper19/dj_bootcamp.git
```

### Move to new folder and create a virtual environment

```zsh
cd ./dj_bootcamp
python -m venv ./venv
```

### Activate the virtual environment

```zsh
source ./venv/bin/activate
```

#### To deactivate the virtual environment

```zsh
deactivate
```

### Install Django inside of the virtual environment

```zsh
pip install django
```

### Update pip (optional)

```zsh
pip install --upgrade pip
```

### Check if Django is installed inside of the virtual environment

```zsh
pip freeze
```

- asgiref==3.3.1
- **_Django==3.1.3_**
- pytz==2020.4
- sqlparse==0.4.1

### Create a src directory in the project separated from the virtual environment

```zsh
mkdir src
```

### Create a Django project in the src directory

```zsh
django-admin startproject dj_bootcamp ./src
```

### Move to the src directory and run the initial migrations

```zsh
cd ./src
python manage.py migrate
```

### Create a super user

```zsh
python manage.py createsuperuser
```

## Day One - Why Django

### Create Apps

```zsh
python manage.py startapp products
python manage.py startapp profiles
```

In settings.py

```python
INSTALLED_APPS = [
   'django.contrib.admin',
   'django.contrib.auth',
   'django.contrib.contenttypes',
   'django.contrib.sessions',
   'django.contrib.messages',
   'django.contrib.staticfiles',
   # own
   'products',
   'profiles',
]
```

### Create models

In products/models.py

```python
from django.db import models

# Create your models here.


class Product(models.Model):
    title = models.CharField(max_length=220)
    content = models.TextField(null=True, blank=True)
    price = models.IntegerField(default=0)

```

Create model for profile as well.

### Migrations

```zsh
python manage.py makemigrations
python manage.py migrate
```

### Register models in the admin

In products/admin.py

```python
from django.contrib import admin

# Register your models here.
from .models import Product
admin.site.register(Product)
```

### Working with the Django shell

#### Create records

```python
(venv) ➜  src git:(main) ✗  python manage.py shell
Python 3.8.3 (default, Jul  6 2020, 19:29:12)
[Clang 11.0.0 (clang-1100.0.33.8)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> from products.models import Product
>>> Product.objects.create(title='Raspberry Pi')
<Product: Product object (1)>
```

#### Update records

```python
>>> obj = Product.objects.get(id=2)
>>> obj.content = "this is the content for the database field content"
>>> obj.save()
```

## Day Two - From Database to Webpage

### Working with views

#### Simple view

Modify the products/view.py

```python
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Product
# Create your views here.


def home_view(request, *args, **kwargs):
    return HttpResponse("<h1>Hello World</h1>")


def product_detail_view(request, pk):
    try:
        obj = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        raise Http404
    return HttpResponse(f"<h1>Product: {obj.id}</h1><p>title: {obj.title}</p><p>content: {obj.content}</p>")


def product_api_detail_view(request, pk, *arg, **kwargs):
    try:
        obj = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return JsonResponse({"message": "Not found"})
    return JsonResponse({"id": obj.id, "title": obj.title, "content": obj.content})

```

Add the view in the dj_bootcamp/urls.py

```python
from django.contrib import admin
from django.urls import path
from products.views import (
    home_view,
    product_detail_view,
    product_api_detail_view,
)
urlpatterns = [
    path('admin/', admin.site.urls),
    # own
    path("search/", home_view),
    path("products/<int:pk>/", product_detail_view),  # dynamic url
    path("api/products/<int:pk>/", product_api_detail_view),  # dynamic url
]

```

## Day 3 - Rendering dynamic HTML

### Working with Templates

#### Add the templates dir in settings.py

Modify the TEMPLATES list on settings.py by adding the templates directory:

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],  # main templates directory
        'APP_DIRS': True, ...
```

#### Create HTML templates with Django Template Language

Templates could be stored in the main src/template directory, at the same level
as manage.py or at the App level e.g.: src/products/**templates/products/**

##### src/template/base.html

This is the base.html and all the templates should be inherit from it, lives
in the main template directory src/template/

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>
      {%block title%}Django Bootcamp from Justin Mitchel{%endblock%}
    </title>
    <style>
      h1 {
        color: green;
      }
    </style>
  </head>
  <body>
    {% include "navbar.html" %} {% block content %} {% endblock %} {% block js
    %} {% endblock %}
  </body>
</html>
```

##### src/products/templates/product/product_list.html

Example of extended template and template language

```html
{% extends "base.html" %} {% block title %} Products - {{ block.super }}
{%endblock %} {% block content %} {% for object in object_list %}
<div>
  {{ object.title }} {% include "detail_snippet.html" with object=object %}
</div>
{% endfor %} {% endblock %}
```

### Add a function base view

Add a function based view on src/products/views.py to use the template

```python
def product_list_view(request, *args, **kwargs):
    qs = Product.objects.all()
    context = {"object_list": qs}
    return render(request, "products/product_list.html", context)
```

### Wire the FBV to the URL

Add the view to the src/url.py

```python
from products.views import (
    home_view,
    product_detail_view,
    product_api_detail_view,
    product_list_view,
)
urlpatterns = [
    path('admin/', admin.site.urls),
    # own
    path("search/", home_view),
    path("products/<int:pk>/", product_detail_view),  # dynamic url
    path("api/products/<int:pk>/", product_api_detail_view),  # dynamic url
    path("products/", product_list_view),  # dynamic url
]
```

## Day 4 - Add data with Django Forms

### Create src/products/forms.py

```python
from django import forms
from .models import Product

class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "title",
            "content",
            "price",
        ]

    def clean_title(self):
        data = self.cleaned_data.get("title")
        if len(data) < 3:
            raise forms.ValidationError(
                "Title must be 3 or more characters long")
        return data
```

### Create a src/templates/forms.html template

```html
{% extends "base.html"%} {% block content %}
<form method="POST" action=".">
  {% csrf_token %} {{ form.as_p }}
  <button type="submit">Send data</button>
</form>
{% endblock %}
```

### Add a FBV to use the form

```python
def product_create_view(request, *arg, **kwargs):
    form = ProductModelForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        # do some stuff
        obj.save()
        form = ProductModelForm()
    context = {"form": form}
    return render(request, "forms.html", context)

```

### Wire the view to the url

In the urls.py:

```python
from products.views import (
...
    product_create_view,
...
)
urlpatterns = [
...
    path("products/create/", product_create_view),
...
]
```

## Day 5 - Login and Register Users

### Create a new App: accounts

```zsh
python manage.py startapp accounts
```

### Add LOGIN_URL and LOGIN_REDIRECT_URL to settings.py

```python
# own 20201204
LOGIN_URL = "/login"
LOGIN_REDIRECT_URL = "/"
```

### Add a form to the new App: src/accounts/form.py

```python
from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()

class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "user-password",
            }
        )
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "user-confirm-password",
            }
        )
    )

    def clean_username(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        qs = User.objects.filter(username__iexact=username)
        if qs.exists():
            raise forms.ValidationError(
                "This is an invalid username, pick another one")
        return username

    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email__iexact=email)
        if qs.exists():
            raise forms.ValidationError(
                "This is an invalid email, pick another one")
        return email


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "user-password",
            }
        )
    )

    def clean_username(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        qs = User.objects.filter(username__iexact=username)
        if not qs.exists():
            raise forms.ValidationError("Invalid user")
        return username
```

### Add the FBV to the src/accounts/views.py

#### Imports from django.contrib.aut, forms and set the User

```python
from django.shortcuts import render, redirect
from django.contrib.auth import (
    authenticate,
    login,
    logout,
    get_user_model
)
from .forms import LoginForm, RegisterForm
# Create your views here.

User = get_user_model()
```

#### Register view

```python
def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password1 = form.cleaned_data.get("password1")
        password2 = form.cleaned_data.get("password2")
        try:
            user = User.objects.create_user(username, email, password1)
        except:
            user = None

        if user != None:
            login(request, user)
            return redirect("/")
        request.session["invalid_user"] = 1
    return render(request, "forms.html", {"form": form})
```

#### Login view

```python
def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user != None:
            login(request, user)
            return redirect("/")
        request.session["invalid_user"] = 1
    return render(request, "forms.html", {"form": form})
```

#### Logout view

```python
def logout_view(request):
    logout(request)
    return redirect("/login")
```

#### Wire to the URLs

```python
...
from accounts.views import (
    login_view,
    logout_view,
    register_view,
)
...
urlpatterns = [
...
    path("login/", login_view),
    path("logout/", logout_view),
    path("register/", register_view),
...
]
```

#### Add user FK (luby) field to the Product model

```python
from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL

class Product(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
...
```

#### Modify src/products/views.py to add the user

```python
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
...
# @login_required
@staff_member_required
def product_create_view(request, *arg, **kwargs):
    form = ProductModelForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        # do some stuff:
        obj.user = request.user
        obj.save()
        form = ProductModelForm()
    context = {"form": form}
    return render(request, "forms.html", context)

```
