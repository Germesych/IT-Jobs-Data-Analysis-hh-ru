# Библиотека Requests в Python

Библиотека [Requests](https://requests.readthedocs.io/en/latest/) — это основной пакет для выполнения HTTP-запросов в Python. Она абстрагирует сложности выполнения запросов за интуитивно понятным [API](https://realpython.com/ref/glossary/api/). Хотя она не входит в стандартную библиотеку Python, стоит рассмотреть Requests для выполнения HTTP-действий, таких как GET, POST и другие.

**К концу этого руководства вы поймете, что:**

*   **Requests не является встроенным** модулем Python — это сторонняя библиотека, которую необходимо устанавливать отдельно.
*   **GET-запрос** в Python выполняется с помощью `requests.get()` с указанием нужного URL.
*   **Чтобы добавить заголовки к запросам**, передайте словарь заголовков в параметр `headers` вашего запроса.
*   **Чтобы отправить данные POST**, используйте параметр `data` для данных в формате form-encoded или параметр `json` для данных JSON.
*   **`response.text` дает строковое** представление содержимого ответа, а **`response.content` предоставляет сырые байты**.

Это руководство проведет вас через настройку запросов с заголовками и данными, обработку ответов, аутентификацию и оптимизацию производительности с использованием сессий и повторных попыток.

Если вы хотите изучить примеры кода, которые вы увидите в этом руководстве, вы можете скачать их здесь:

> **Получите свой код:** [Нажмите здесь, чтобы скачать бесплатный пример кода](https://realpython.com/bonus/python-requests-code/), который показывает, как использовать библиотеку Requests в Python.

## Начало работы с библиотекой Requests в Python

Несмотря на то, что библиотека Requests является распространенным инструментом для многих Python-разработчиков, она не входит в [стандартную библиотеку](https://realpython.com/ref/glossary/standard-library/) Python. Это позволяет библиотеке развиваться более свободно как самостоятельный проект.

> **Примечание:** Если вы хотите делать HTTP-запросы только с помощью стандартной библиотеки Python, то [urllib.request](https://realpython.com/urllib-request/) в Python — хороший выбор для вас.

Поскольку Requests является сторонней библиотекой, вам нужно установить ее перед использованием в вашем коде. Как хорошая практика, вы должны устанавливать внешние пакеты в [виртуальное окружение](https://realpython.com/python-virtual-environments-a-primer/), но вы можете выбрать установку `requests` в ваше глобальное окружение, если планируете использовать ее в нескольких проектах.

Работаете ли вы в виртуальном окружении или нет, вам нужно установить `requests`:

```shell
$ python -m pip install requests
```

После того как `pip` завершит установку `requests`, вы можете использовать ее в своем приложении. Импорт `requests` выглядит так:

```python
import requests
```

Теперь, когда вы все настроили, пора начать ваше путешествие с Requests. Ваша первая цель — сделать запрос `GET`.

## Сделайте GET-запрос

[HTTP-методы](https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol#Request_methods), такие как `GET` и `POST`, определяют действие, которое вы хотите выполнить при выполнении HTTP-запроса. В дополнение к `GET` и `POST` есть несколько других распространенных методов, которые вы будете использовать позже в этом руководстве.

Одним из наиболее часто используемых HTTP-методов является `GET`, который извлекает данные из указанного ресурса. Чтобы сделать `GET`-запрос с помощью Requests, вы можете вызвать `requests.get()`.

Чтобы попробовать это, вы можете сделать `GET`-запрос к [REST API GitHub](https://docs.github.com/en/rest), вызвав `get()` со следующим URL:

```python
>>> import requests
>>> requests.get("https://api.github.com")
<Response [200]>
```

Поздравляем! Вы сделали свой первый запрос. Теперь вы глубже погрузитесь в ответ на этот запрос.

## Изучите ответ

`Response` — это объект, который содержит результаты вашего запроса. Попробуйте сделать тот же запрос еще раз, но на этот раз сохраните возвращаемое значение в [переменной](https://realpython.com/python-variables/), чтобы вы могли поближе познакомиться с его [атрибутами](https://realpython.com/ref/glossary/attribute/) и поведением:

```python
>>> import requests
>>> response = requests.get("https://api.github.com")
```

В этом примере вы захватили возвращаемое значение `requests.get()`. Это экземпляр `Response`, и вы сохранили его в переменной с именем `response`. Теперь вы можете использовать `response`, чтобы увидеть много информации о результатах вашего `GET`-запроса.

### Работа с кодами состояния

Первая информация, которую вы можете получить из `Response`, — это **код состояния**. Код состояния информирует вас о статусе запроса.

Например, статус `200 OK` означает, что ваш запрос был успешным, а статус `404 NOT FOUND` означает, что ресурс, который вы искали, не был найден. Существует много других возможных [кодов состояния](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes), которые также дают вам конкретное представление о том, что произошло с вашим запросом.

Обратившись к `.status_code`, вы можете увидеть код состояния, который вернул сервер:

```python
>>> response.status_code
200
```

`.status_code` вернул `200`, что означает, что ваш запрос был успешным, и сервер ответил запрошенными данными.

Иногда вы можете захотеть использовать эту информацию для принятия решений в вашем коде:

```python
if response.status_code == 200:
    print("Success!")
elif response.status_code == 404:
    print("Not Found.")
```

С этой логикой, если сервер возвращает код состояния `200`, ваша программа [напечатает](https://realpython.com/python-print/) `Success!`. Если результат `404`, то ваша программа напечатает `Not Found`.

Requests идет на шаг дальше, упрощая этот процесс для вас. Если вы используете экземпляр `Response` в [логическом](https://realpython.com/ref/glossary/boolean/) контексте, таком как [условный оператор](https://realpython.com/python-conditional-statements/), то он будет оцениваться как [True](https://realpython.com/ref/keywords/true/), когда код состояния меньше `400`, и [False](https://realpython.com/ref/keywords/false/) в противном случае.

Это означает, что вы можете изменить последний пример, переписав оператор [if](https://realpython.com/ref/keywords/if/):

```python
if response:
    print("Success!")
else:
    raise Exception(f"Non-success status code: {response.status_code}")
```

В приведенном выше фрагменте кода вы неявно проверяете, находится ли `.status_code` `response` между `200` и `399`. Если это не так, то вы [вызываете](https://realpython.com/python-raise-exception/) [исключение](https://realpython.com/python-exceptions/) с сообщением об ошибке, которое включает код состояния, не указывающий на успех, обернутый в [f-строку](https://realpython.com/python-f-strings/).

> **Примечание:** Эта [проверка истинности](https://realpython.com/python-boolean/#python-boolean-testing) возможна потому, что [`.__bool__()` является перегруженным методом](https://realpython.com/operator-function-overloading/#making-your-objects-truthy-or-falsey-using-bool) в `Response`. Это означает, что адаптированное поведение по умолчанию для `Response` учитывает код состояния при определении истинности объекта.

Имейте в виду, что этот метод *не* проверяет, равен ли код состояния `200`. Это связано с тем, что другие коды состояния в диапазоне от `200` до `399`, такие как `204 NO CONTENT` и `304 NOT MODIFIED`, также считаются успешными, поскольку они предоставляют некоторый рабочий ответ.

Например, код состояния `204` сообщает вам, что ответ был успешным, но в теле сообщения нет содержимого для возврата.

Поэтому убедитесь, что вы используете этот удобный ярлык только в том случае, если хотите узнать, был ли запрос в целом успешным. Затем, при необходимости, вам нужно будет соответствующим образом обработать ответ на основе кода состояния.

Предположим, вы не хотите проверять код состояния ответа в операторе `if`. Вместо этого вы хотите использовать встроенные возможности Request для вызова [исключения](https://realpython.com/ref/glossary/exception/), если запрос был неудачным. Вы можете сделать это с помощью `.raise_for_status()`:

```python
import requests
from requests.exceptions import HTTPError

URLS = ["https://api.github.com", "https://api.github.com/invalid"]

for url in URLS:
    try:
        response = requests.get(url)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")
    else:
        print("Success!")
```

Если вы вызываете [`.raise_for_status()`](https://requests.readthedocs.io/en/latest/api/#requests.Response.raise_for_status), то Requests вызовет `HTTPError` для кодов состояния между `400` и `600`. Если код состояния указывает на успешный запрос, то программа продолжит работу без вызова этого исключения.

Теперь вы знаете много о том, как работать с кодом состояния ответа, который вы получаете от сервера. Однако, когда вы делаете `GET`-запрос, вы редко заботитесь только о коде состояния ответа. Обычно вы хотите увидеть больше. Далее вы узнаете, как просмотреть фактические данные, которые сервер отправил обратно в теле ответа.

### Доступ к содержимому ответа

Ответ на `GET`-запрос часто содержит некоторую ценную информацию, известную как [полезная нагрузка (payload)](https://en.wikipedia.org/wiki/Payload_(computing)), в теле сообщения. Используя атрибуты и методы `Response`, вы можете просмотреть полезную нагрузку в различных форматах.

Чтобы увидеть содержимое ответа в [байтах](https://realpython.com/ref/builtin-types/bytes/), вы используете `.content`:

```python
>>> import requests

>>> response = requests.get("https://api.github.com")
>>> response.content
b'{"current_user_url":"https://api.github.com/user", ...}'

>>> type(response.content)
<class 'bytes'>
```

В то время как `.content` дает вам доступ к сырым байтам полезной нагрузки ответа, вы часто захотите преобразовать их в [строку](https://realpython.com/python-data-types/), используя [кодировку символов](https://realpython.com/python-encodings-guide/), такую как [UTF-8](https://en.wikipedia.org/wiki/UTF-8). `response` сделает это за вас, когда вы обратитесь к `.text`:

```python
>>> response.text
'{"current_user_url":"https://api.github.com/user", ...}'

>>> type(response.text)
<class 'str'>
```

Поскольку декодирование [байтов](https://realpython.com/ref/builtin-types/bytes/) в [строку](https://realpython.com/ref/builtin-types/str/) требует схемы кодирования, Requests попытается угадать [кодировку](https://docs.python.org/3/howto/unicode.html#encodings) на основе [заголовков](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers) ответа, если вы не укажете ее. Вы можете предоставить явную кодировку, установив `.encoding` перед доступом к `.text`:

```python
>>> response.encoding = "utf-8"  # Опционально: Requests определяет это.
>>> response.text
'{"current_user_url":"https://api.github.com/user", ...}'
```

Если вы посмотрите на ответ, то увидите, что это фактически сериализованное содержимое [JSON](https://realpython.com/python-json/). Чтобы получить словарь, вы могли бы взять `str`, который вы получили из `.text`, и десериализовать его с помощью [`json.loads()`](https://realpython.com/python-json/#deserialize-json-data-types). Однако прямой способ выполнить эту задачу — использовать `.json()`:

```python
>>> response.json()
{'current_user_url': 'https://api.github.com/user', ...}

>>> type(response.json())
<class 'dict'>
```

Тип возвращаемого значения `.json()` — это [словарь](https://realpython.com/ref/glossary/dictionary/), поэтому вы можете получить доступ к значениям в объекте по ключу:

```python
>>> response_dict = response.json()
>>> response_dict["emojis_url"]
'https://api.github.com/emojis'
```

Вы можете многое сделать с кодами состояния и телами сообщений. Но если вам нужно больше информации, например, [метаданные](https://en.wikipedia.org/wiki/Metadata) о самом ответе, вам нужно будет посмотреть на заголовки ответа.

### Просмотр заголовков ответа

Заголовки ответа могут дать вам полезную информацию, такую как [тип содержимого](https://en.wikipedia.org/wiki/Media_type) полезной нагрузки ответа и как долго кэшировать ответ. Чтобы просмотреть эти заголовки, обратитесь к `.headers`:

```python
>>> import requests

>>> response = requests.get("https://api.github.com")
>>> response.headers
{'Server': 'github.com',
...
'X-GitHub-Request-Id': 'AE83:3F40:2151C46:438A840:65C38178'}
```

Атрибут `.headers` возвращает объект, похожий на словарь, позволяющий вам получить доступ к значениям заголовков по ключу. Например, чтобы увидеть тип содержимого полезной нагрузки ответа, вы можете обратиться к `"Content-Type"`:

```python
>>> response.headers["Content-Type"]
'application/json; charset=utf-8'
```

Есть что-то особенное в этом похожем на словарь объекте заголовков. Спецификация HTTP определяет заголовки как нечувствительные к регистру, что означает, что вы можете получить к ним доступ, не беспокоясь об их капитализации:

```python
>>> response.headers["content-type"]
'application/json; charset=utf-8'
```

Независимо от того, используете ли вы ключ `"content-type"` или `"Content-Type"`, вы получите одно и то же значение.

Теперь, когда вы увидели наиболее полезные [атрибуты](https://realpython.com/ref/glossary/attribute/) и [методы](https://realpython.com/ref/glossary/method/) `Response` в действии, у вас уже есть хороший обзор базового использования Requests. Вы можете получать контент из интернета и работать с ответом, который вы получаете.

Но в интернете есть нечто большее, чем простые прямые URL. В следующем разделе вы сделаете шаг назад и посмотрите, как меняются ваши ответы, когда вы настраиваете свои `GET`-запросы с учетом параметров строки запроса.

## Добавление параметров строки запроса

Один из распространенных способов настроить `GET`-запрос — передать значения через [параметры строки запроса](https://en.wikipedia.org/wiki/Query_string) в URL. Чтобы сделать это с помощью `get()`, вы передаете данные в `params`. Например, вы можете использовать [поисковый API репозиториев GitHub](https://docs.github.com/en/rest/search/search#search-repositories) для поиска популярных репозиториев Python:

```python
import requests

response = requests.get(
    "https://api.github.com/search/repositories",
    params={"q": "language:python", "sort": "stars", "order": "desc"},
)

json_response = response.json()
popular_repositories = json_response["items"]
for repo in popular_repositories[:3]:
    print(f"Name: {repo['name']}")
    print(f"Description: {repo['description']}")
    print(f"Stars: {repo['stargazers_count']}\n")
```

Передавая словарь в параметр `params` `get()`, вы можете изменить результаты, возвращаемые из поискового API.

Вы можете передать `params` в `get()` либо как словарь, как вы только что сделали, либо как список [кортежей](https://realpython.com/python-tuple/):

```python
>>> import requests

>>> requests.get(
...     "https://api.github.com/search/repositories",
...     [("q", "language:python"), ("sort", "stars"), ("order", "desc")],
... )
<Response [200]>
```

Вы даже можете передать значения как `bytes`:

```python
>>> requests.get(
...     "https://api.github.com/search/repositories",
...     params=b"q=language:python&sort=stars&order=desc",
... )
<Response [200]>
```

Строки запроса полезны для параметризации `GET`-запросов. Другой способ настроить ваши запросы — добавить или изменить заголовки, которые вы отправляете.

## Настройка заголовков запроса

Чтобы настроить заголовки, вы передаете словарь HTTP-заголовков в `get()`, используя параметр `headers`. Например, вы можете изменить ваш предыдущий поисковый запрос, чтобы выделить соответствующие условия поиска в результатах, указав медиатип `text-match` в заголовке `Accept`:

```python
import requests

response = requests.get(
    "https://api.github.com/search/repositories",
    params={"q": '"real python"'},
    headers={"Accept": "application/vnd.github.text-match+json"},
)

json_response = response.json()
first_repository = json_response["items"][0]
print(first_repository["text_matches"][0]["matches"])
```

Заголовок `Accept` сообщает серверу, с какими типами контента может работать ваше приложение. В этом случае, поскольку вы ожидаете, что соответствующие условия поиска будут выделены, вы используете значение заголовка `application/vnd.github.text-match+json`. Это проприетарный заголовок `Accept` GitHub, где содержимое имеет специальный JSON-формат.

Когда вы [запустите этот Python-скрипт](https://realpython.com/run-python-scripts/), вы получите результат, похожий на показанный ниже:

```shell
$ python text_matches.py
[{'text': 'Real Python', 'indices': [23, 34]}]
```

Прежде чем вы узнаете больше способов настройки запросов, вы расширите свой кругозор, изучив другие HTTP-методы.

## Использование других HTTP-методов

Помимо `GET`, другие популярные HTTP-методы включают `POST`, `PUT`, `DELETE`, `HEAD`, `PATCH` и `OPTIONS`. Для каждого из этих HTTP-методов Requests предоставляет [функцию](https://realpython.com/ref/glossary/function/) с сигнатурой, похожей на `get()`.

> **Примечание:** Чтобы опробовать эти HTTP-методы, вы будете делать запросы к [httpbin.org](https://httpbin.org/). Сервис httpbin — это отличный ресурс, созданный оригинальным автором Requests, [Кеннетом Рейтцем](https://realpython.com/interview-kenneth-reitz/). Сервис принимает тестовые запросы и отвечает данными о запросах.

Вы заметите, что Requests предоставляет интуитивный интерфейс для всех распространенных HTTP-методов:

```python
>>> import requests

>>> requests.get("https://httpbin.org/get")
<Response [200]>
>>> requests.post("https://httpbin.org/post", data={"key": "value"})
<Response [200]>
>>> requests.put("https://httpbin.org/put", data={"key": "value"})
<Response [200]>
>>> requests.delete("https://httpbin.org/delete")
<Response [200]>
>>> requests.head("https://httpbin.org/get")
<Response [200]>
>>> requests.patch("https://httpbin.org/patch", data={"key": "value"})
<Response [200]>
>>> requests.options("https://httpbin.org/get")
<Response [200]>
```

В приведенном выше примере вы вызывали каждую функцию, чтобы сделать запрос к сервису httpbin, используя соответствующий HTTP-метод.

Все эти функции являются высокоуровневыми ярлыками для [`requests.request()`](https://requests.readthedocs.io/en/latest/api/#requests.request), который принимает имя метода в качестве своего первого аргумента:

```python
>>> requests.request("GET", "https://httpbin.org/get")
<Response [200]>
```

Вы могли бы использовать эквивалентный низкоуровневый вызов функции, но сила библиотеки Requests Python в ее удобном для человека высокоуровневом интерфейсе. Вы можете проверять ответы так же, как вы делали это раньше:

```python
>>> response = requests.head("https://httpbin.org/get")
>>> response.headers["Content-Type"]
'application/json'

>>> response = requests.delete("https://httpbin.org/delete")
>>> json_response = response.json()
>>> json_response["args"]
{}
```

Независимо от того, какой метод вы используете, вы получаете объект `Response`, который предоставляет доступ к заголовкам, телам ответов, кодам состояния и многому другому.

Далее вы внимательнее посмотрите на методы `POST`, `PUT` и `PATCH` и узнаете, чем они отличаются от других типов запросов.

## Отправка данных запроса

Согласно спецификации HTTP, запросы `POST`, `PUT` и менее распространенный `PATCH` передают свои данные через тело сообщения, а не через параметры в строке запроса. С Requests вы передаете эту полезную нагрузку в параметр `data` соответствующей функции.

Параметр `data` принимает словарь, список кортежей, байты или файлоподобный объект. Вы захотите адаптировать данные, которые вы отправляете в теле вашего запроса, к конкретным потребностям службы, с которой вы взаимодействуете.

Например, если тип содержимого вашего запроса — `application/x-www-form-urlencoded`, то вы можете отправить данные формы в виде словаря:

```python
>>> import requests

>>> requests.post("https://httpbin.org/post", data={"key": "value"})
<Response [200]>
```

Вы также можете отправить те же данные в виде списка кортежей:

```python
>>> requests.post("https://httpbin.org/post", data=[("key", "value")])
<Response [200]>
```

Если вам нужно отправить данные [JSON](https://realpython.com/ref/glossary/json/), то вы можете использовать параметр `json`. Когда вы передаете данные JSON через `json`, Requests сериализует ваши данные и добавит правильный заголовок `Content-Type` за вас.

Как вы узнали ранее, сервис httpbin принимает тестовые запросы и отвечает данными о запросах. Например, вы можете использовать его для проверки базового `POST`-запроса:

```python
>>> response = requests.post("https://httpbin.org/post", json={"key": "value"})
>>> json_response = response.json()
>>> json_response["data"]
'{"key": "value"}'
>>> json_response["headers"]["Content-Type"]
'application/json'
```

Из ответа видно, что сервер получил данные и заголовки вашего запроса точно так, как вы их отправили. Requests также предоставляет вам эту информацию в виде `PreparedRequest`, который вы рассмотрите более внимательно в следующем разделе.

## Изучите подготовленный запрос

Когда вы делаете запрос, библиотека Requests подготавливает запрос перед фактической отправкой на сервер назначения. Подготовка запроса включает такие вещи, как проверка заголовков и сериализация JSON-содержимого.

Вы можете просмотреть объект `PreparedRequest`, обратившись к `.request` на объекте `Response`:

```python
>>> import requests

>>> response = requests.post("https://httpbin.org/post", json={"key":"value"})

>>> response.request
<PreparedRequest [POST]>

>>> response.request.headers["Content-Type"]
'application/json'

>>> response.request.url
'https://httpbin.org/post'

>>> response.request.body
b'{"key": "value"}'
```

Проверка `PreparedRequest` дает вам доступ ко всей kinds of information about the request being made, such as payload, URL, headers, authentication, and more.

До сих пор вы делали много различных типов запросов, но все они имели одну общую черту: это были неаутентифицированные запросы к публичным API. Многие сервисы, с которыми вы столкнетесь, захотят, чтобы вы каким-то образом аутентифицировались.

## Использование аутентификации

Аутентификация помогает сервису понять, кто вы. Обычно вы предоставляете свои учетные данные серверу, передавая данные через заголовок `Authorization` или пользовательский заголовок, определенный службой. Все функции в Requests, которые вы видели до этого момента, предоставляют параметр с именем `auth`, который позволяет вам передавать ваши учетные данные напрямую:

```python
>>> import requests

>>> response = requests.get(
...     "https://httpbin.org/basic-auth/user/passwd",
...     auth=("user", "passwd")
... )

>>> response.status_code
200
>>> response.request.headers["Authorization"]
'Basic dXNlcjpwYXNzd2Q='
```

Запрос завершается успешно, если учетные данные, которые вы передаете в кортеже в `auth`, действительны.

Когда вы передаете свои учетные данные в кортеже в параметр `auth`, Requests применяет учетные данные, используя схему [базовой аутентификации доступа HTTP (Basic access authentication)](https://en.wikipedia.org/wiki/Basic_access_authentication) под капотом.

> **Схема базовой аутентификации**
>
> Вам может быть интересно, откуда берется строка `Basic dXNlcjpwYXNzd2Q=`, которую Requests установил в качестве значения для вашего заголовка `Authorization`. Короче говоря, это строка в кодировке [Base64](https://en.wikipedia.org/wiki/Base64) имени пользователя и пароля с префиксом `"Basic "`:
>
> 1.  Сначала Requests объединяет предоставленные имя пользователя и пароль, вставляя между ними двоеточие. Так, для имени пользователя `"user"` и пароля `"passwd"` это становится `"user:passwd"`.
> 2.  Затем Requests кодирует эту строку в Base64 с помощью `base64.b64encode()`. Кодировка преобразует строку `"user:passwd"` в `"dXNlcjpwYXNzd2Q="`.
> 3.  Наконец, Requests добавляет `"Basic "` перед этой строкой Base64.
>
> Вот как окончательное значение для заголовка `Authorization` становится `Basic dXNlcjpwYXNzd2Q=` в примере, показанном выше.
>
> Обратите внимание, что базовая аутентификация HTTP (BA) сама по себе не очень безопасна, потому что любой может декодировать строку Base64, чтобы раскрыть ваши учетные данные. Вот почему всегда важно отправлять эти запросы по [HTTPS](https://realpython.com/python-https/), который шифрует весь запрос и обеспечивает дополнительный уровень защиты.

Вы могли бы сделать тот же запрос, передав явные учетные данные базовой аутентификации с помощью `HTTPBasicAuth`:

```python
>>> from requests.auth import HTTPBasicAuth
>>> requests.get(
...     "https://httpbin.org/basic-auth/user/passwd",
...     auth=HTTPBasicAuth("user", "passwd")
... )
<Response [200]>
```

Хотя вам не нужно быть явным для базовой аутентификации, вы можете захотеть аутентифицироваться с помощью другого метода. Requests предоставляет [другие методы аутентификации](https://requests.readthedocs.io/en/latest/api/#authentication) из коробки, такие как `HTTPDigestAuth` и `HTTPProxyAuth`.

Реальным примером API, который требует аутентификации, является API [аутентифицированного пользователя GitHub](https://docs.github.com/en/rest/users/users/#get-the-authenticated-user). Эта конечная точка предоставляет информацию о профиле аутентифицированного пользователя.

Если вы попытаетесь сделать запрос без учетных данных, то увидите, что код состояния — `401 Unauthorized`:

```python
>>> requests.get("https://api.github.com/user")
<Response [401]>
```

Этот метод работает, но это не правильный способ [аутентификации с помощью токена `Bearer`](https://docs.github.com/en/rest/authentication/authenticating-to-the-rest-api?apiVersion=2022-11-28#about-authentication) — и использование пустой строки ввода для избыточного имени пользователя неудобно.

С Requests вы можете предоставить свой собственный механизм аутентификации, чтобы исправить это. Чтобы попробовать это, создайте [подкласс](https://realpython.com/ref/glossary/subclass/) `AuthBase` и реализуйте `.__call__()`:

```python
from requests.auth import AuthBase

class TokenAuth(AuthBase):
    """Implements a token authentication scheme."""

    def __init__(self, token):
        self.token = token

    def __call__(self, request):
        """Attach an API token to the Authorization header."""
        request.headers["Authorization"] = f"Bearer {self.token}"
        return request
```

Здесь ваш пользовательский механизм `TokenAuth` получает токен, затем включает этот токен в заголовок `Authorization` вашего запроса, также устанавливая рекомендуемый префикс `"Bearer "` к строке.

Теперь вы можете использовать эту пользовательскую токенную аутентификацию для вызова API аутентифицированного пользователя GitHub:

```python
>>> import requests
>>> from custom_token_auth import TokenAuth

>>> token = "<YOUR_GITHUB_PA_TOKEN>"
>>> response = requests.get(
...     "https://api.github.com/user",
...     auth=TokenAuth(token)
... )

>>> response.status_code
200
>>> response.request.headers["Authorization"]
'Bearer ghp_b...Tx'
```

Ваш пользовательский `TokenAuth` создал хорошо отформатированную строку для заголовка `Authorization`. Это дает вам более интуитивный и многократно используемый способ работы со схемами аутентификации на основе токенов, подобными тем, которые требуются частями API GitHub.

> **Примечание:** Хотя вы могли бы сконструировать строку аутентификации вне пользовательского класса аутентификации и передать ее напрямую с `headers`, этот подход [не рекомендуется](https://github.com/psf/requests/issues/2062#issuecomment-44095986), потому что это может привести к [неожиданному поведению](https://github.com/psf/requests/issues/2066).
>
> Когда вы пытаетесь установить свои учетные данные аутентификации напрямую с помощью `headers`, Requests может внутренне перезаписать ваш ввод. Это может произойти, например, если у вас есть [файл `.netrc`](https://everything.curl.dev/usingcurl/netrc.html), который предоставляет учетные данные аутентификации. Requests попытается [получить учетные данные из файла `.netrc`](https://requests.readthedocs.io/en/latest/user/authentication/), если вы не предоставите метод аутентификации с помощью `auth`.

Плохие механизмы аутентификации могут привести к уязвимостям безопасности. Если только служба не требует пользовательский механизм аутентификации по какой-то причине, лучше придерживаться проверенного метода, такого как встроенная базовая аутентификация или [OAuth](https://requests.readthedocs.io/en/latest/user/authentication/#oauth-1-authentication) — например, через [Requests-OAuthlib](https://requests-oauthlib.readthedocs.io/en/latest/).

Пока вы думаете о безопасности, рассмотрите возможность работы с TLS/SSL-сертификатами с помощью Requests.

## Безопасное общение с серверами

Всякий раз, когда данные, которые вы пытаетесь отправить или получить, являются конфиденциальными, безопасность становится essential. Способ, которым вы общаетесь с защищенными сайтами по HTTP, заключается в установлении зашифрованного соединения с использованием [Transport Layer Security (TLS)](https://en.wikipedia.org/wiki/Transport_Layer_Security). TLS является преемником Secure Sockets Layer (SSL), предлагая повышенную безопасность и эффективность в безопасной связи. Тем не менее, программисты все еще часто используют термин SSL вместо TLS.

Requests проверяет цифровой сертификат серверов для вас по умолчанию, и вам редко нужно вносить коррективы в это поведение. Однако есть некоторые случаи, когда вам может потребоваться настроить процесс проверки.

Например, когда вы работаете в корпоративной среде с пользовательскими центрами сертификации, вам может потребоваться предоставить свой собственный набор сертификатов:

```python
>>> import requests

>>> requests.get(
...     "https://internal-api.company.com",
...     verify="/path/to/company-ca.pem"
... )
<Response [200]>
```

Вы также можете предоставить каталог, содержащий файлы сертификатов, если вам нужно доверять нескольким пользовательским центрам.

Если вы отлаживаете проблемы с сертификатами в разработке, то вы можете быть tempted to отключить проверку entirely. Хотя это работает, это значительный риск безопасности, и вы никогда не должны использовать этот подход в production:

```python
>>> requests.get("https://api.github.com", verify=False)
InsecureRequestWarning: Unverified HTTPS request is being made to host
⮑ 'api.github.com'. Adding certificate verification is strongly advised.
⮑ See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#tls-warnings
⮑  warnings.warn(
<Response [200]>
```

Requests предупреждает вас об этой опасной практике, потому что отключение проверки делает вас уязвимыми для атак "man-in-the-middle".

> **Примечание:** [Requests использует пакет под названием `certifi`](https://requests.readthedocs.io/en/latest/user/advanced/#ca-certificates) для предостав