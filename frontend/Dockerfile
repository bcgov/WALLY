FROM node:10 as build

WORKDIR /app

COPY package*.json /app/

RUN npm ci

COPY . .

RUN npm run build


FROM nginx:mainline

COPY --from=build /app/dist/ /usr/share/nginx/html

COPY --from=build /app/nginx.conf /etc/nginx/conf.d/default.conf

RUN chmod g+rwx /var/cache/nginx /var/run /var/log/nginx

EXPOSE 8080
CMD ["nginx", "-g", "daemon off;"]
