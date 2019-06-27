FROM node:10 as build

WORKDIR /app

COPY package*.json /app/

RUN npm ci

COPY . .

RUN npm run build


FROM nginx:1.12

COPY --from=build /app/dist/ /tmp/src

# COPY --from=build /app/nginx.conf /tmp/src/nginx.conf

RUN /usr/libexec/s2i/assemble

EXPOSE 8080
CMD /usr/libexec/s2i/run
