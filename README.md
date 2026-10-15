# astro090-pm.github.io

Сайт-портфолио Романа Понурова: https://astro090-pm.github.io

- Тексты кейсов — `content/cases/*.md` (те же, что в [product-cases](https://github.com/astro090-pm/product-cases)).
- Главная страница и список кейсов — в `build.py`.
- Пересобрать после изменений: `pip install markdown && python build.py`, затем закоммитить HTML.

Сайт статический, без фреймворков: GitHub Pages отдаёт файлы из ветки `main`.

## Как опубликовать пост

1. Создайте файл `content/posts/ГГГГ-ММ-ДД-короткое-имя.md`:

   ```
   ---
   title: Заголовок поста
   date: 2026-10-20
   tags: продукт, AI
   ---

   Первый абзац — он же анонс на главной.

   Дальше текст в Markdown.
   ```

2. `python build.py`, затем закоммитьте изменения. Пост появится на главной (5 последних) и в разделе «Посты».
