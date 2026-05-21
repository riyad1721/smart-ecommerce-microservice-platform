# Smart E-Commerce Microservice Frontend

A portfolio-level React + TypeScript frontend for the **Smart E-Commerce Microservice Platform**. This repository only contains frontend code and integrates with these backend services:

| Service | URL |
|---|---|
| Auth Service | `http://localhost:8000/api/v1` |
| Product Service | `http://localhost:8001/api/v1` |
| Order Service | `http://localhost:8002/api/v1` |
| Payment Service | `http://localhost:8003/api/v1` |
| Notification Service | `http://localhost:8004/api/v1` |

## Features

- Register and login
- JWT saved in `localStorage`
- Axios interceptor automatically attaches `Authorization: Bearer <token>`
- Protected routes
- Dashboard with summary cards
- Product listing and search
- Add product to cart
- View and remove cart items
- Create order from cart
- Process fake payment
- View payment status
- View notification logs
- Responsive sidebar dashboard
- Loading, error, success, and empty states

## Windows CMD Setup

```cmd
npm install
copy .env.example .env
npm run dev
```

Open:

```txt
http://localhost:5173
```

## Docker Run

```cmd
docker build -t ecommerce-frontend .
docker run -p 3000:80 ecommerce-frontend
```

Open:

```txt
http://localhost:3000
```

## Full Testing Flow

1. Run backend services:
   - auth-service on port `8000`
   - product-service on port `8001`
   - order-service on port `8002`
   - payment-service on port `8003`
   - notification-service on port `8004`
2. Start frontend with `npm run dev`.
3. Go to `/register` and create a user.
4. Go to `/login` and login.
5. Confirm token exists in browser localStorage.
6. Browse products from product-service.
7. Search product by keyword.
8. Add product to cart.
9. Go to cart page and confirm item.
10. Remove item or create order.
11. Go to orders page.
12. Click **Process Payment**.
13. Go to payments page and check payment status.
14. Go to notifications page and check notification logs.
15. Logout.

## Common Error Fixes

### CORS Error

Allow frontend origin in each FastAPI backend service:

```python
allow_origins=["http://localhost:5173", "http://localhost:3000"]
```

### JWT Not Sending

Check `src/api/axiosClient.ts`. The request interceptor reads token from localStorage and attaches it automatically.

### Environment Variables Not Working

Vite variables must start with `VITE_`. After editing `.env`, restart `npm run dev`.

### React Router 404 in Docker/Nginx

`nginx.conf` already uses:

```nginx
try_files $uri /index.html;
```

### Backend Response Shape Difference

If your backend returns wrapped data like `{ "data": [...] }`, update the related API function or page state assignment.

## Project Structure

```txt
ecommerce-frontend/
├── src/
│   ├── api/
│   ├── components/
│   ├── features/
│   ├── hooks/
│   ├── routes/
│   ├── types/
│   ├── utils/
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css
├── Dockerfile
├── nginx.conf
├── package.json
├── vite.config.ts
├── tsconfig.json
├── tailwind.config.js
├── postcss.config.js
├── .env.example
└── README.md
```
