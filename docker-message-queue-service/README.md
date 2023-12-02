# Docker x PostgreSQL x RabbitMQ Video Service

## Задание

Mоля да направите следната задача (с оценка) като проект:

Използвайте docker compose за да изградите собствен service с инфраструктура и функционалност по ваш избор.
Задължително service-а трябва да използва SQL база данни и messaging service (RabbitMQ, Apache Kafka etc.).
Защитата на проекта ще е на 06.12.2023г.

## Описание на проекта

### API Service

CRUD Rest API, което може да чете и пише данни за видеа, съхранявани в PostgeSQL база данни. При създаване на ново видео, комуникира с Notification Service-а чрез RabbitMQ.
