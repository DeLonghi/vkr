Efotix project. Producer.
=========================
*Efotix* - прототип Библиотеки цифровых моделей.\
*Producer* сервисы - обеспечивают отправку данных на обработку модели по заданным сценариям.\

Структура проекта
------------
**Producer**\
├── **/bin**- *каталог с исполняемыми файлами.*\
│   ├── **producer.py** - *описывает сценарии отправки данных.*\
│   ├── **broadcast.py** - *запускает отработку сценариев отправки данных.*\
├── **/docker**- *каталог с описанием сервисов для docker-compose.*\
│   ├── **Dockerfile** - *Dockerfile для запуска данного сервиса.*\
│   ├── **Supervised.Dockerfile** - *Dockerfile для запуска сервиса  через супервизор*\
├── **/resources** - *каталог с примерами конфигов для запуска сервиса (модели)*\
├── **requirements.txt** - *файл с информации об использованных в проекте библиотеках.*\ 

Пример входных и выходных данных
--------------------------------
**Сенарий #1**: *Hysys (Feed 29)*
input.yaml:
```
type: Producer
id: thread_name
threads:
  service_name:
    delay: 100
    input:
    -
        Methane: 0.031
        Ethane: 0.002
        Propane: 0.135
        i-Butane: 0.12
        n-Butane: 0.19
        i-Pentane: 0.01
        n-Pentane: 0.17
...
```
output json:
```
{"Methane": 0.031, "Ethane": 0.002, "Propane" : 0.135, "i-Butane" : 0.12, "n-Butane" : 0.19, "i-Pentane" : 0.01, "n-Pentane" : 0.17}
...
```


**Сенарий #2**: *Excel & Hysys (Temperature)*
input.yaml:
```
type: Producer
id: thread_name
threads:
  service_name:
    delay: 100
    input:
    -
        T cond K-6: 42
    -
        T top K-6: 53.9
...
```
output json:
```
{"T cond K-6":42}
{"T top K-6":53.9}
...
```
