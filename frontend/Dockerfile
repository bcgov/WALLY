FROM node:10 as build

WORKDIR /app

COPY package*.json /app/

RUN npm ci

COPY . .

RUN npm run build


FROM nginx:1.12

COPY --from=build /app/dist/ /usr/share/nginx/html

COPY --from=build /app/nginx.conf /etc/nginx/nginx.conf

EXPOSE 8080
CMD /tmp/scripts/run
