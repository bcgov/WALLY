FROM node:22-alpine AS build
WORKDIR /app
COPY package*.json /app/
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:1.27-alpine

COPY --from=build /app/dist/ /usr/share/nginx/html

# Make nginx's runtime directories writable by the group, not just a fixed
# UID - OpenShift assigns a random UID at runtime (with GID 0), so
# permissions must be group-based, not owner-based, to work correctly there.
RUN chgrp -R 0 /var/cache/nginx /var/run /usr/share/nginx/html /etc/nginx/conf.d && \
    chmod -R g=u /var/cache/nginx /var/run /usr/share/nginx/html /etc/nginx/conf.d && \
    touch /var/run/nginx.pid && \
    chgrp 0 /var/run/nginx.pid && \
    chmod g=u /var/run/nginx.pid

EXPOSE 8080

USER 1001
CMD ["nginx", "-g", "daemon off;"]