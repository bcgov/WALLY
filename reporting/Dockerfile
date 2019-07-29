FROM node:10

WORKDIR /app

COPY package*.json /app/

RUN npm ci

COPY . .

RUN chmod +x /src/app.js

RUN npm run build

EXPOSE 3000

CMD ["npm", "run", "serve"]
