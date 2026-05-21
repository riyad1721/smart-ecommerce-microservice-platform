# syntax=docker/dockerfile:1.7

ARG NODE_IMAGE=node:22-alpine
ARG NGINX_IMAGE=nginxinc/nginx-unprivileged:stable-alpine

FROM ${NODE_IMAGE} AS deps
WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci --ignore-scripts

FROM deps AS build
WORKDIR /app

ARG VITE_AUTH_SERVICE=/api/v1
ARG VITE_PRODUCT_SERVICE=/api/v1
ARG VITE_ORDER_SERVICE=/api/v1
ARG VITE_PAYMENT_SERVICE=/api/v1
ARG VITE_NOTIFICATION_SERVICE=/api/v1

ENV VITE_AUTH_SERVICE=${VITE_AUTH_SERVICE} \
    VITE_PRODUCT_SERVICE=${VITE_PRODUCT_SERVICE} \
    VITE_ORDER_SERVICE=${VITE_ORDER_SERVICE} \
    VITE_PAYMENT_SERVICE=${VITE_PAYMENT_SERVICE} \
    VITE_NOTIFICATION_SERVICE=${VITE_NOTIFICATION_SERVICE}

COPY . .
RUN npm run build

FROM ${NGINX_IMAGE} AS runtime

ENV NGINX_ENTRYPOINT_QUIET_LOGS=1

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build --chown=101:101 /app/dist /usr/share/nginx/html

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD wget -qO- http://127.0.0.1:8080/healthz || exit 1

USER 101

CMD ["nginx", "-g", "daemon off;"]
