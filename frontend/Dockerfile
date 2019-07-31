FROM node:10 as build

WORKDIR /app

COPY package*.json /app/

RUN npm ci

COPY . .

# run unit tests and build
RUN npm run test:unit && npm run build

FROM nginx:1.12

COPY --from=build /app/dist/ /tmp/src

COPY --from=build /app/nginx.conf.tmpl /tmp/src/nginx.conf

RUN /usr/libexec/s2i/assemble

EXPOSE 8080
CMD /usr/libexec/s2i/run
