БЦМ2 project. Consumer.
=========================
*Clavius* - прототип цифрового двойника нефтеперерабатывающей установки.\
*Consumer* сервисы - обеспечивают получение данных для записи в БД.

Структура проекта
------------
**Consumer**\
├── **/bin**- *каталог с исполняемыми файлами.*\
│   ├── **consumer.py** - *Основной исполняемый файл реализующий функционал из config файлов*\
├── **/docker**- *каталог с описанием сервисов для docker-compose.*\
│   ├── **/[name]** - *каталог с описанием сервиса для отправки данных в БД.*\
│   │   ├── **config.yml** - *YAML файл конфигурации сервиса и сценариев его работы.*\
│   │   ├── **Dockerfile** - *Dockerfile для запуска данного сервиса.*\
├── **docker-compose.yml** - *YAML файл конфигурации и общих параметров однотипных сервисов.*\
├── **requirements.txt** - *файл с информации об использованных в проекте библиотеках.*

Запуск сервисов
------------
Файл *docker-compose.yml* служит для запуска нескольких сервисов одновременно. Как частный случай -с помощью 
него можно запустить один отдельный сервис (для этого в структуре файла должна быть описан только он).\
\
Запуск сервисов производится командой:
```
$ docker-compose up --build
```

Конфигурирование Подключения к БД (пока только MySQL) и описние топика Kafka производится в *docker-compose.yml*:

```
environment:
      DB_HOST: 172.16.0.128
      DB_PORT: 30104
      DB_USER: root
      DB_PASS: gpnPsw19
      DB_NAME: consumer
      KAFKA_HOST: 'localhost:9092'
      KAFKA_TOPIC: 'consumer'
```

## Настройка сборки проекта
Необходимо установить дополнительно ПО на локальной машине
1. Установка kubectl https://kubernetes.io/docs/tasks/tools/install-kubectl/
2. Скачиваем kubeconfig из ранчера https://172.16.0.112:8443, создаем папку .kube в домашней директории, в файл ~/.kube/config
 копируем содержимое kubeconfig
3. Установка helm и подключение к существующему tiller https://helm.sh/docs/using_helm/

Настройка проекта
1. Внутри проекта создаем папку helm
2. В папке helm выполняем команду helm create kafka-%project_name%
3. Появилась следующая структура (файлы, не вошедшие в структуру ниже, можно удалить)
**Project_name**\
├── **/helm**- *каталог helm*\
│   ├── **/project-name** - *Каталог, созданный командой helm create*\
│   │   ├── **/templates** - 
│   │   │   ├── **/tests/test-connection.yaml** - *Сгенерирован автоматически*\
│   │   │   ├── **/deployments.yaml** - *Описываем контейнеры для запуска, переменные среды, путь к image*\
│   │   │   ├── **/NOTES.txt** - *Сгенерирован автоматически*\
│   │   ├── **/.helmignore** - *Сгенерирован автоматически*\
│   │   ├── **/Chart.yaml** - *Сгенерирован автоматически*\
│   │   ├── **/values.yaml** - *Сгенерирован автоматически*\
├── **/.gitlab-ci.yaml** - *Прописываем путь для создания image в registry gitlab*