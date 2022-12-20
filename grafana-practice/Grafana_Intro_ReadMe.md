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
docker-compose up -d grafana
```
Команда развернет
- http://your_machine_ip:3000 - web ui графаны
- http://your_machine_ip:8080 - web ui графита. Так будут расшарено много портов для взаимодействия с графитом

Проверить поднятые контейнеры можно так:
```shell
docker ps
```

### Остановить работу grafana и graphite:
```shell
docker-compose down
```

## Знакомство c Graphite

### Компоненты
1. carbon - сервис, принимающий данные на вход
2. whisper - БД для сохранения данных
3. graphite-web - http://your_machine_ip:8080/ web ui

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

- Почистить данные графана можно так: `docker volume rm grafana-volume` (убедитесь, что контейнеры остановлены)
- Почистить все volumes можно так: `docker volume prune`
- Почистить все объекты: `docker system prune --volumes`

[Полная документация](https://docs.docker.com/config/pruning/)
