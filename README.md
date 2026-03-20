# HACKATHON Security-Breach

## 💫 Introduction

Welcome to the SB_Sagyz web app! This guide will help you get started with our app and explain the main features.

## 💻 Tech Stack

<p>
  <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" alt="Python">
  <img src="https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/django_rest_framework-A30000?style=for-the-badge&logo=django&logoColor=white" alt="Django REST Framework">
  <img src="https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white" alt="JWT">
  <img src="https://img.shields.io/badge/sqlalchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white" alt="SQLAlchemy">
  <img src="https://img.shields.io/badge/postgresql-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/sqlite-07405E?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite">
  <img src="https://img.shields.io/badge/openai-412991?style=for-the-badge&logo=openai&logoColor=white" alt="OpenAI API">
  <img src="https://img.shields.io/badge/shodan-E85D04?style=for-the-badge&logo=shodan&logoColor=white" alt="Shodan API">
  <img src="https://img.shields.io/badge/nmap-004C97?style=for-the-badge&logo=gnu-bash&logoColor=white" alt="Nmap">
  <img src="https://img.shields.io/badge/tailwind_css-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="Tailwind CSS">
  <img src="https://img.shields.io/badge/beautifulsoup-2E7D32?style=for-the-badge&logo=python&logoColor=white" alt="BeautifulSoup">
  <img src="https://img.shields.io/badge/celery-37814A?style=for-the-badge&logo=celery&logoColor=white" alt="Celery">
</p>

## CLI / Technical Section

### Run the server

```bash
python manage.py runserver
```

### Fetch and populate the exploit list in the database:

```bash
python manage.py fetch_exploit
```

### Fetch and populate the PoC (Proof of Concept) list in the database:

```bash
python manage.py fetch_poc
```

### Clear the exploit and PoC (Proof of Concept) table:

```bash
python manage.py clear_tables
```

*Note: after cleanup, regenerate the table using the commands above for proper operation.*

### Clear all scan requests and history records:

```bash
python manage.py clear_scan
```

## API Requests

Important: to use the REST API, you must obtain access tokens first.

### Get token (JSON authorization)

```
POST /api/token {username} {password}
```

### Refresh token

```
POST /api/token {username} {refresh_token}
```

### Get vulnerabilities and available PoC (Proof of Concept)

```
POST /api/vulnerabilities
```

### Create an IPv4 scan request.

```
GET /api/scan {ip_address}
```
