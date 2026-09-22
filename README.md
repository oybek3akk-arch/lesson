# Progress — Django project

## Установка

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Открой:

http://127.0.0.1:8000/

## Страницы

- `/` — Splash, 10 секунд
- `/home/` — главная
- `/vote/` — голосование
- `/admin-panel/login/` — вход в красивую админ-панель
- `/admin-panel/` — управление вопросами и голосованиями
- `/django-admin/` — стандартная Django Admin

## Админ

Создай суперпользователя:

```powershell
python manage.py createsuperuser
```

Для входа в `/admin-panel/login/` нужен этот же пользователь, и он должен иметь `is_staff=True`.

## Особенности

- Django 6.0.7
- Tailwind CSS через CDN
- Google Fonts
- Splash около 10 секунд
- случайный шрифт для сессии пользователя
- фиксированный header
- footer
- голосование за две команды
- защита от повторного голоса в одной сессии
- результаты голосования обновляются каждые 2 секунды
- вопросы с выбором или собственным текстовым ответом
- вопросы и результаты управляются через собственную админ-панель
- SQLite

### Персональный стиль
У каждого пользователя в его сессии случайно выбираются Google Font и визуальная цветовая тема. При новой сессии комбинация может быть другой.

## Деплой: GitHub → Railway

### 1. Загрузка на GitHub

```bash
cd progress_self_knowledge
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/<ваш-логин>/<название-репозитория>.git
git push -u origin main
```

(Или создайте репозиторий на github.com и загрузите папку любым удобным
способом — через GitHub Desktop, веб-интерфейс и т.п.)

### 2. Деплой на Railway

1. Зайдите на [railway.app](https://railway.app/), New Project →
   **Deploy from GitHub repo** → выберите репозиторий.
2. Railway автоматически определит Python-проект (Nixpacks) и найдёт
   `Procfile` / `railway.json` со стартовой командой.
3. **Обязательно задайте переменные окружения** в Project → Variables:
   - `SECRET_KEY` — сгенерируйте новый ключ (не используйте тот, что в
     репозитории), например:
     `python -c "import secrets; print(secrets.token_urlsafe(50))"`
   - `DEBUG` = `False`
   - `ALLOWED_HOSTS` = `*` (или ваш домен, например `myapp.up.railway.app`)
   - (переменную `RAILWAY_PUBLIC_DOMAIN` Railway задаёт сама — проект уже
     учитывает её для `ALLOWED_HOSTS` и CSRF автоматически)
4. **База данных.** По умолчанию проект использует SQLite — на Railway
   файловая система эфемерна, и данные (голоса, ответы) будут стираться при
   каждом новом деплое. Для постоянного хранения:
   - В проекте Railway нажмите **+ New → Database → PostgreSQL**.
   - Railway сам создаст переменную `DATABASE_URL` и подключит её к сервису
     — ничего дополнительно настраивать в коде не нужно (используется
     `dj-database-url`).
5. При каждом деплое автоматически выполняются `migrate`, `collectstatic`
   и запускается `gunicorn` (см. `Procfile` / `railway.json`).
6. После первого деплоя создайте суперпользователя (нужен и для входа в
   `/admin-panel/login/`, и для `/django-admin/`). В Railway откройте
   вкладку сервиса → **Shell**, либо через
   [Railway CLI](https://docs.railway.com/guides/cli):
   ```bash
   railway run python manage.py createsuperuser
   ```
7. Откройте выданный Railway домен
   (`https://<ваш-проект>.up.railway.app/`) — заставка → главная →
   голосование; `/admin-panel/login/` — красивая админка,
   `/django-admin/` — стандартная Django Admin.

### Файлы, добавленные для деплоя

- `Procfile` — команда запуска на Railway (миграции → статика → gunicorn).
- `railway.json` — явная конфигурация билда/старта (дублирует Procfile на
  случай нестандартного автодетекта).
- `.python-version` — версия Python для сборщика Nixpacks.
- `.gitignore` — исключает venv, `db.sqlite3`, `staticfiles/`, `.env` и т.п.
  (в исходном проекте этого файла не было).
- `.env.example` — список переменных окружения для Railway → Variables
  (сам `.env` в репозиторий не попадает).
- В `requirements.txt` добавлены `gunicorn`, `whitenoise`,
  `dj-database-url`, `psycopg2-binary`.
- `config/settings.py` переведён на переменные окружения (`SECRET_KEY`,
  `DEBUG`, `ALLOWED_HOSTS`, `DATABASE_URL`), добавлен `STATIC_ROOT` и
  подключён `whitenoise` для раздачи статики в продакшене (раньше
  `STATIC_ROOT` не был задан — `collectstatic` не работал бы вовсе).

