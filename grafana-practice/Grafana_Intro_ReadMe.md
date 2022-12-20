# Grafana practice

## Подготовка к запуску
Подготовка диска для хранения состояния Grafana
```shell
docker volume create --name=grafana-volume
```

## Run
Склонируйте репозиторий. Перейдите в директорию `grafana-practice`

Чтобы развернуть демонстрационный стенд Grafana, выполните.
```shell
docker-compose up -d
```
Команда развернет
- http://your_machine_ip:3000 - web ui графаны
- http://your_machine_ip:8080 - web ui графита. Так будут расшарено много портов для взаимодействия с графитом
- Дополнительные сервисы, рассмотрим на workshope'е:
  - http://your_machine_ip:8000 - сервис с ML моделью. Модель предсказывает пол по имени.
  Поиграться и побросать запросы в него можно со странички http://your_machine_ip:8000/docs
  - http://your_machine_ip:8089 - web ui locust'а - инструмента, для нагрузочного тестирования.

Проверить поднятые контейнеры можно так:
```shell
docker ps
```

## Знакомство c Graphite

### Компоненты
1. carbon - сервис, принимающий данные на вход
2. whisper - БД для сохранения данных
3. graphite-web - http://62.84.113.93:8080/ web ui

### Документация по graphite
- [Терминология](https://graphite.readthedocs.io/en/latest/terminology.html)
- [Функции для работы с рядами данных](https://graphite.readthedocs.io/en/latest/functions.html)
- [Тэги](https://graphite.readthedocs.io/en/latest/tags.html)

## Знакомство с web UI
1. Web UI Grafana: http://your_machine_ip:3000
1. Стандартные login/pswd: `admin`/`admin`
1. Добавляем источник данных
   - Тип: Graphite
   - url: http://your_machine_ip:8080 (важно указать именно ip вашей машины, а не localhost)
   - остальное не меняем
   - Сообщение `Cannot read properties of undefined (reading 'get')` - не страшно
1. Можно проверить чтение данных из graphite в режиме explore
1. Добавляем папку для dashboard'ов
1. Добавляем первый dashboard

## Настройка аллертов в ММ

См [пост в ММ](https://mt.avito.ru/avito/pl/ttobbi151jntjc4ziucof17xjo)


## Удалить созданные объекты

- Почистить volumes можно так: `docker volume prune`
- Почистить все объекты: `docker system prune --volumes`

[Полная документация](https://docs.docker.com/config/pruning/)
