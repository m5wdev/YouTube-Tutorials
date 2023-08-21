# Monolit README

## How to deploy
### 1. Create virtualenv:
```
$ virtualenv venv
```

**Activate venv:**  

*for Windows*
```
$ venv\Scripts\activate
```

*for Linux*
```
$ source venv\bin\activate
```


### 2. Install packages from requirements.txt:
```
$ pip install -r monolit\requirements\requirements.txt
```


### 3. If you need to update all Python packages
List outdated packages
```
$ pip list --outdated
```

Update outdated packages Manually
```
$ pip install django, pip, pillow --upgrade
```

Update all outdated packages from requirements.txt
```
$ pip install -r requirements\requirements.txt
```

**!!! IMPORTANT**
After update outdated packages save all to *requirements.txt*
```
$ pip freeze > requirements\requirements.txt
```


### 4. Go to monolit project folder:
```
$ cd monolit/
```


### 5. Create .env:
```
$ touch .env
```

with content:
```
DEBUG=True
ALLOWED_HOSTS=monolit.site|www.monolit.site
SECRET_KEY=1mnn8bj$(zm5$t9=io*_1ndo43w2p5kv$+sn(xf%d@2so7v_&#
```


### 6. Install & Update node packages
**Install node packages**
```
$ cd monolit\monolit
$ npm i
```

**Update node packages**
```
$ npm update --save-dev
$ npm update --save
```


### 7. Compile with Webpack:
```
$ npm run build
```


### 8. Run migrations:
```
$ python manage.py makemigrations
$ python manage.py migrate
```


### 9. Create Superuser:
```
$ python manage.py createsuperuser
```
then answer the questions in order to create Superuser account


### 10. Create default content:
```
$ python manage.py add_default_content
```


### 11. Run local server:
```
$ python manage.py runserver
```



## How to get from GitHub
Clone from GitHub:
```
$ git clone https://github.com/m5studio/monolit.git
then enter credentials
```


## How to update from GitHub
Run:
```
$ cd monolit/
$ git pull https://github.com/m5studio/monolit.git
... then enter your credentials
```

## Clean empty folders and unused files
Run:
```
$ python manage.py cleanup_unused_media
$ python manage.py clean_empty_media_dirs
```

## How fill site with dummy content
Enshure you're in DEBUG=True mode  
Then put or check in ```/media/``` folder two files: ```dummy-document.pdf``` and ```dummy-image.jpg```

Run:
```
$ python manage.py generate_content 5
```
Note: you can generate 10 objects at ones
