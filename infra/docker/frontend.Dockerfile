# Vite + React frontend served via nginx.
FROM node:20-alpine AS builder

WORKDIR /app

COPY package.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine AS runner

COPY --from=builder /app/dist /usr/share/nginx/html

# Serve on port 3000 to match the rest of the compose stack
RUN sed -i 's/listen       80;/listen       3000;/g' /etc/nginx/conf.d/default.conf \
    && sed -i 's/listen  \[::]:80;/listen  [::]:3000;/g' /etc/nginx/conf.d/default.conf

EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]
