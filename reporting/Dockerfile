FROM node:10

WORKDIR /app

COPY package*.json /app/

RUN npm ci

COPY . .

EXPOSE 3000

CMD ["npm", "run", "start"]
