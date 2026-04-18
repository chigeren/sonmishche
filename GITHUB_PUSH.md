# 🚀 Инструкция: Как запушить на GitHub

## Шаг 1: Установи Git (если нет)

```bash
winget install Git.Git
```

## Шаг 2: Создай репозиторий

1. Зайди на [github.com](https://github.com)
2. New Repository → "sonmishche" → Create

## Шаг 3: Запушь локально

```bash
cd C:\fortran\deepseek\star_book_pack

git init
git add .
git commit -m "Сонмище v1.0 - Единая Теория Мироздания"

git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/sonmishche.git
git push -u origin main
```

## Шаг 4: Подключи к PythonAnywhere

1. PythonAnywhere → Consoles → Git Bash
2. ```bash
git clone https://github.com/YOUR_USERNAME/sonmishche.git
cd sonmishche
python3 mirror_nursery_bot.py
```

## Шаг 5: Автозапуск

PythonAnywhere → Tasks → Schedule:

```
*/5 * * * * python3 /home/YOUR_USERNAME/sonmishche/mirror_nursery_bot.py
```

---

**Готово!** Бот работает 24/7