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
- http://your_machine_ip:8000 - сервис с ML моделью. Модель предсказывает пол по имени.
Поиграться и побросать запросы в него можно со странички http://your_machine_ip:8000/docs
- http://your_machine_ip:3000 - web ui графаны
- http://your_machine_ip:8080 - web ui графита. Так будут расшарено много портов для взаимодействия с графитом
- http://your_machine_ip:8089 - web ui locust'а - инструмента, для нагрузочного тестирования.

Проверить поднятые контейнеры можно так:
```shell
docker ps
```

## Снесение изменений
Внести изменения в код сервиса можно в файлике:
[service.py](./ml_service/service.py)

Внести изменения в код построения запросов для locust можно в файлике:
[locustfile.py](./locustfile.py)

Код написан таким образом, что пересобирать docker образы не нужно (если, конечно, вы не добавляете новые библиотеки).

## Настройка аллертов в ММ

См [пост в ММ](https://mt.avito.ru/avito/pl/ttobbi151jntjc4ziucof17xjo)
