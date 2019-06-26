FROM node:10 as build

WORKDIR /app

COPY package*.json /app/

RUN npm ci

COPY ./ /app/

RUN npm run test:unit

RUN npm run build


FROM nginx:1.12

COPY --from=build /app/dist/ /usr/share/nginx/html

COPY --from=build /app/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 8080
