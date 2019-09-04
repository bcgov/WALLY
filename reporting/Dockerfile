FROM node:10

WORKDIR /app

USER 0

COPY package*.json /app/

RUN chgrp -R 0 /app/ && \
    chmod -R g=u /app/

RUN npm install

COPY . .

RUN npm run build

EXPOSE 3000

USER 1001

CMD ["npm", "run", "serve"]
