FROM node:22-alpine AS build
WORKDIR /app
COPY package*.json /app/
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:1.27-alpine

COPY --from=build /app/dist/ /usr/share/nginx/html

EXPOSE 8080

USER 1001
CMD ["nginx", "-g", "daemon off;"]