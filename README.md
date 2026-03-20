# HACKATHON Security-Breach

## Введение
Добро пожаловать в веб-приложение SB_Sagyz! Это руководство поможет вам начать работу с нашим приложением и объяснит основные функции.

## Технический стек

<p>
  <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" alt="Python">
  <img src="https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/django_rest_framework-A30000?style=for-the-badge&logo=django&logoColor=white" alt="Django REST Framework">
  <img src="https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white" alt="JWT">
  <img src="https://img.shields.io/badge/celery-37814A?style=for-the-badge&logo=celery&logoColor=white" alt="Celery">
  <img src="https://img.shields.io/badge/postgresql-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/sqlite-07405E?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite">
  <img src="https://img.shields.io/badge/openai-412991?style=for-the-badge&logo=openai&logoColor=white" alt="OpenAI API">
  <img src="https://img.shields.io/badge/shodan-E85D04?style=for-the-badge&logo=shodan&logoColor=white" alt="Shodan API">
  <img src="https://img.shields.io/badge/nmap-004C97?style=for-the-badge&logo=gnu-bash&logoColor=white" alt="Nmap">
  <img src="https://img.shields.io/badge/selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=white" alt="Selenium">
  <img src="https://img.shields.io/badge/beautifulsoup-2E7D32?style=for-the-badge&logo=python&logoColor=white" alt="BeautifulSoup">
  <img src="https://img.shields.io/badge/sqlalchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white" alt="SQLAlchemy">
  <img src="https://img.shields.io/badge/tailwind_css-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="Tailwind CSS">
</p>

## GUI Часть

### Регистрация и Вход
1. **Регистрация**:
   - Перейдите на страницу регистрации по адресу `/register`.
   - Заполните форму регистрации, указав ваш email, имя пользователя и пароль.
   - Нажмите кнопку "Зарегистрироваться".

2. **Вход**:
   - Перейдите на страницу входа по адресу `/login`.
   - Введите ваш email и пароль.
   - Нажмите кнопку "Войти".

### Личный Кабинет
После входа в систему вы попадете в ваш личный кабинет, где сможете:
- Просматривать личные данные.
- Просматривать историю запросов.

### Сканирование
1. Перейдите на страницу сканирования по адресу `/create_query`.
2. Введите IP или домен сервера, который вы хотите просканировать.
3. Нажмите кнопку "Начать сканирование".
4. Дождитесь завершения сканирования и просмотрите результаты.

### Просмотр Уязвимостей
1. Перейдите на страницу уязвимостей по адресу `/vulnerabilities`.
2. Просматривайте список уязвимостей, найденных в системе.

### Выход из Системы
Чтобы выйти из системы, нажмите на кнопку "Выйти" в верхнем меню.

## CLI/Техническая часть

### Запустить сервер
```bash
python manage.py runserver
```

### Получить и построить в БД список эксплойтов:
```bash
python manage.py fetch_exploit
```

### Получить и построить в БД список PoC (Proof of Concept):
```bash
python manage.py fetch_poc
```

### Очистить таблицу эксплойтов и PoC (Proof of Concept):
```bash
python manage.py clear_tables
```
*Примечание! Далее для правильной работы потребуется перегенирация таблицы командами выше.*

### Очистка всех записей запросов и истории:
```bash
python manage.py clear_scan
```

## Запросы API

Внимание! Для того, чтобы пользоваться REST API, необходимо получить токены.

### Получение токена (авторизация по json)
```
POST /api/token {username} {password}
```

### Обновление токена
```
POST /api/token {username} {refresh_token}
```


### Получение списка уязвимостей и возможных PoC (Proof of Concept)
```
POST /api/vulnerabilities
```

### Создание запроса на сканирование IPv4 адреса.
```
GET /api/scan {ip_adress}
```
