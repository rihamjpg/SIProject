from setuptools import setup, find_packages

setup(
    name="SIProject",
    version="0.1",
    packages=find_packages(),  
    install_requires=[
        asgiref==3.8.1
black==23.11.0
click==8.1.8
colorama==0.4.6
coverage==7.3.2
Django==4.2.7
django-cleanup==8.0.0
django-cors-headers==4.3.0
django-debug-toolbar==4.2.0
django-filter==23.3
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.0
drf-yasg==1.21.7
factory_boy==3.3.1
Faker==33.3.1
flake8==6.1.0
gunicorn==23.0.0
inflection==0.5.1
iniconfig==2.0.0
isort==5.12.0
mccabe==0.7.0
mypy-extensions==1.0.0
packaging==24.2
pathspec==0.12.1
Pillow==10.1.0
platformdirs==4.3.6
pluggy==1.5.0
psycopg2==2.9.9
psycopg2-binary==2.9.9
pycodestyle==2.11.1
pyflakes==3.1.0
PyJWT==2.10.1
pytest==7.4.3
pytest-django==4.7.0
python-dateutil==2.9.0.post0
python-dotenv==1.0.0
pytz==2023.3
PyYAML==6.0.1
six==1.17.0
sqlparse==0.5.3
typing_extensions==4.12.2
tzdata==2024.2
uritemplate==4.1.1

    ],
    description="Système de gestion des ressources humaines",
    author="Riham",
    author_email="your_email@example.com",
    url="https://github.com/rihamjpg/SIProject",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  
)
