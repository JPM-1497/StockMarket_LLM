<<<<<<< HEAD
FROM node:18
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "run", "dev"]  
=======
FROM node:18-alpine

WORKDIR /app

COPY . .

RUN npm install

CMD ["npm", "run", "dev"]
>>>>>>> b8fb39c1e47ecb3da4bad163fb4f4a234c37e7be
