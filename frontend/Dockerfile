FROM node:20-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
ARG VITE_TELEGRAM_BOT_NAME
ENV VITE_TELEGRAM_BOT_NAME=$VITE_TELEGRAM_BOT_NAME
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
