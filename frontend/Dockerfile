FROM node:10 as build

WORKDIR /app

COPY package*.json /app/

RUN npm ci

COPY . .

RUN npm run build

FROM caddy:2.0.0-beta.17

WORKDIR /app/src
COPY --from=build /app/dist/ /app/src
COPY --from=build /app/Caddyfile /etc/caddy/Caddyfile

EXPOSE 8080
