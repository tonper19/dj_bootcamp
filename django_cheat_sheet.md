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
