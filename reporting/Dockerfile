FROM node:10

WORKDIR /app

USER 0

RUN apt-get update -y && apt-get install -y --no-install-recommends libvips-dev libegl1-mesa libgles2-mesa

COPY package*.json /app/

RUN chgrp -R 0 /app/ && \
    chmod -R g=u /app/

RUN npm install

COPY . .

RUN npm run build

EXPOSE 3000

USER 1001

CMD ["npm", "run", "serve"]
