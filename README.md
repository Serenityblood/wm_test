# Скрипт для обработки логов


Примеры работы:

* В --file можно отправлять несколько файлов

![](pics/report.png)

* Можно использовать --date для фильтрации по дате

![](pics/date.png)

* Есть тесты. Из главной директории:
> pytest

#### Cтэк
> tabulate, black, pytest, pipenv


#### Установка зависимостей
Два варианта:
1) Через pipenv
```bazaar
pip install pipenv
pipenv shell
pipenv install
```

2) Через pip
```bazaar
pip install -r requriements.txt
```