# wish-list
Fast API Проект для составления и обмена списками пожеланий

Этот проект находится в стадии разработки.
В нем Пользователь может создать свой вишлист:
- Описать пожелание;
- По желанию приложить ссылку на него;
- Написать небольшой комментарий.

По ссылке другие пользователи получают доступ к вишлисту и могут забронировать пожелание.
Наиболее важным я считаю возможность выполнения пожелания Пользователем-автором пожелания.
Пользователь знает, какой подарок зарезервирован, и если он свободен - может сам закрыть пожелание.

На данный момент реализована логика с запросами на api приложения. Я занимаюсь разработкой
визуальной составляющей приложения, и очень надеюсь, что в скором времени могу представить 
этот проект для первых пользователей.

### Протестировать работу API можно так:
1. Клонируйте репозиторий wish-list в свою рабочую директорию на компьютере.
2. Переключитель в ветку **develop**
3. Заполните следующие файлы в соответствии с примерами:
    - .env
    - .env.db
4. Выполните команду `docker compose build --no-cache`
5. Выполните команду `docker compose up`

Вам станет доступна документация: http://localhost:8001/docs#/
