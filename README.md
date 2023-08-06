### Описание проекта: 

Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»). 
Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»).

### Как запустить проект: 

Клонировать репозиторий и перейти в него в командной строке: 

``` 
git clone git@github.com:Evgenmater/api_yamdb.git
``` 

``` 
cd api_yamdb
``` 

Cоздать и активировать виртуальное окружение: 

* Если у вас Linux/macOS 

    ``` 
    python3 -m venv env 
    ``` 

    ``` 
    source env/bin/activate 
    ``` 

    ``` 
    python3 -m pip install --upgrade pip 
    ``` 

* Если у вас windows 

    ``` 
    python -m venv venv 
    ``` 

    ``` 
    source venv/Scripts/activate 
    ``` 

    ``` 
    python -m pip install --upgrade pip 
    ``` 

Установить зависимости из файла requirements.txt: 

``` 
pip install -r requirements.txt 
``` 

Выполнить миграции:

* Если у вас Linux/macOS 

    ``` 
    python3 api_yamdb/manage.py migrate --run-syncdb
    ```

* Если у вас windows

    ``` 
    python api_yamdb/manage.py migrate --run-syncdb
    ```

Импортируем данные из csv файлов:

* Если у вас Linux/macOS 

    ``` 
    python3 api_yamdb/manage.py push_to_db
    ``` 

* Если у вас windows

    ``` 
    python api_yamdb/manage.py push_to_db
    ```

Запустить проект:

* Если у вас Linux/macOS 

    ``` 
    python3 manage.py runserver 
    ```

* Если у вас windows

    ``` 
    python manage.py runserver 
    ```

### Примеры запросов к API. 


Получение списка всех категорий: 

``` 
http://127.0.0.1:8000/api/v1/categories/ 
``` 

Получение списка всех жанров

```
http://127.0.0.1:8000/api/v1/genres/
``` 

Получение списка всех комментариев к отзыву: 

``` 
http://127.0.0.1:8000/api/v1/titles/1/reviews/1/comments/
``` 

Получение списка всех произведений: 

``` 
http://127.0.0.1:8000/api/v1/titles/
``` 

По адресу будет доступна документация для API YaMDb в формате Redoc. В документации описано, как должен работать API 

``` 
http://127.0.0.1:8000/redoc/ 
```
