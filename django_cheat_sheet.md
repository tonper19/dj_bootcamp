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

## Day One

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
