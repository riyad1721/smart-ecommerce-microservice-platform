# Smart E-Commerce Microservice Platform - order-service

FastAPI-based order-service using PostgreSQL, SQLAlchemy, RabbitMQ, JWT, Clean Architecture style, and internal product-service REST validation.

## Features

- Add product to cart
- Remove product from cart
- View cart
- Clear cart after order creation
- Create order from cart
- Get order by ID
- List user orders
- Order status lifecycle:
  - PENDING
  - PAYMENT_PENDING
  - PAID
  - PAYMENT_FAILED
  - CANCELLED
- Publish `order.created`
- Consume `payment.completed`
- Consume `payment.failed`
- JWT protected APIs
- Extract `user_id` from JWT token
- Validate product and price from product-service
- PostgreSQL database: `order_db`
- Database user: `order_user`
- Database password: `order_pass`
- Host PostgreSQL port: `5435`

## Run PostgreSQL

```cmd
docker run --name order-postgres -e POSTGRES_DB=order_db -e POSTGRES_USER=order_user -e POSTGRES_PASSWORD=order_pass -p 5435:5432 -d postgres:16
```

## Run RabbitMQ

```cmd
docker run --name ecommerce-rabbitmq -p 5672:5672 -p 15672:15672 -d rabbitmq:3-management
```

RabbitMQ dashboard:

```text
http://127.0.0.1:15672
username: guest
password: guest
```

## Run FastAPI locally

```cmd
cd order-service
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --host 127.0.0.1 --port 8002
```

Swagger:

```text
http://127.0.0.1:8002/docs
```

## JWT test token

Use the helper command:

```cmd
python -c "from app.core.security import create_access_token; print(create_access_token({'sub':'user-123'}))"
```

Then use it as:

```text
Authorization: Bearer YOUR_TOKEN
```

## Product-service contract expected

This order-service expects product-service endpoint:

```http
GET /api/v1/products/{product_id}
```

Expected JSON:

```json
{
  "id": "product-1",
  "name": "Demo Product",
  "price": "100.00",
  "is_active": true,
  "stock_quantity": 10
}
```

## Payment event payloads

Payment completed:

```json
{
  "order_id": "ORDER_UUID"
}
```

Payment failed:

```json
{
  "order_id": "ORDER_UUID",
  "reason": "Insufficient balance"
}
```
