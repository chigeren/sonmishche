#!/usr/bin/env python3
"""
Деплой Сонмище на PythonAnywhere/Render
Скопируй все файлы в Files:
- mirror_nursery_bot.py
- chigerev_bot.py
- .env
- diaries/ (создай папку)
"""

import os
import sys

REQUIRED_FILES = [
    'mirror_nursery_bot.py',
    'chigerev_bot.py',
    '.env'
]

def check_files():
    missing = []
    for f in REQUIRED_FILES:
        if not os.path.exists(f):
            missing.append(f)
    return missing

def main():
    print("=" * 40)
    print("🚀 СОНМИЩЕ DEPLOY CHECK")
    print("=" * 40)
    
    missing = check_files()
    if missing:
        print(f"❌ Отсутствуют: {missing}")
        return 1
    
    print("✅ Все файлы на месте")
    print("\n📋 Инструкция для PythonAnywhere:")
    print("1. Зарегистрируйся на pythonanywhere.com")
    print("2. Открой Consoles → Files")
    print("3. Загрузи mirror_nursery_bot.py")
    print("4. Загрузи chigerev_bot.py")
    print("5. Загрузи .env")
    print("6. Создай папку diaries/")
    print("7. Consoles → python3 mirror_nursery_bot.py")
    print("\n🚀 Бот запущен!")
    return 0

if __name__ == '__main__':
    sys.exit(main())