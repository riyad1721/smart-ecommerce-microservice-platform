# Notification Service

Standalone notification-service for Smart E-Commerce Microservice Platform.

## Run PostgreSQL

```cmd
docker run --name notification-postgres ^
-e POSTGRES_DB=notification_db ^
-e POSTGRES_USER=notification_user ^
-e POSTGRES_PASSWORD=notification_pass ^
-p 5437:5432 ^
-d postgres:16
```

## Run RabbitMQ

```cmd
docker run --name ecommerce-rabbitmq ^
-p 5672:5672 ^
-p 15672:15672 ^
-d rabbitmq:3-management
```

RabbitMQ dashboard:

```txt
http://127.0.0.1:15672
username: guest
password: guest
```

## Setup Python

```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

## Run FastAPI

```cmd
uvicorn app.main:app --reload --host 127.0.0.1 --port 8005
```

Swagger:

```txt
http://127.0.0.1:8005/docs
```

## Test REST APIs

```cmd
curl -X GET http://127.0.0.1:8005/api/v1/health
curl -X GET http://127.0.0.1:8005/api/v1/notifications
curl -X GET http://127.0.0.1:8005/api/v1/notifications/user/user-1/logs
```

## Publish Test Events

```cmd
python scripts\publish_test_event.py order.created
python scripts\publish_test_event.py payment.completed
python scripts\publish_test_event.py payment.failed
```

## Database Verification

```cmd
docker exec -it notification-postgres psql -U notification_user -d notification_db
```

```sql
\dt
SELECT id, event_id, user_id, notification_type, status, recipient_email, created_at
FROM notifications
ORDER BY created_at DESC;
```

## Common Fixes

If PostgreSQL port is busy:

```cmd
docker rm -f notification-postgres
```

If RabbitMQ port is busy:

```cmd
docker rm -f ecommerce-rabbitmq
```

If module not found:

```cmd
venv\Scripts\activate
pip install -r requirements.txt
```
