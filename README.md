# Fazt - DJANGO CRUD AUTH PROJECT

## Steps

1. **Create Envieronment:**

    ```
    python3 -m venv venv
    ```

2. **Install Django:**

    ```
    pip install django
    ```

3. **Create Project:**

    ```
    django-admin startproject <project-name> .
    ```

4. **Run Server:**

    ```
    python manage.py runserver
    ```

5. **Create App:**

    ```
    python manage.py startapp <app-name> .
    ```

6. **Make Migrate :**

    ```
    python manage.py migrate
    ```

7. **Make Migrations:**

    ```
    python manage.py makemigrations
    ```

8. **Run table :**

    ```
    python manage.py migrate
    ```

9. **Connect to Database and edit tables:**

    **This process is more tedious**

    ```
    python manage.py shell
    ```

    or go our browser and run

    ```
    /admin
    ```

10. **Create a superuser:**

    ```
    python manage.py createsuperuser
    user: admin
    mail: python@django.com
    PASSWORD: 12345678@
    ```

11. **Create Static file:**

    ```
    python manage.py collectstatic --no-input
    ```