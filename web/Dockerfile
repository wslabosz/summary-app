FROM node:20-alpine
WORKDIR /code

COPY package*json ./
RUN npm install

COPY ./ /code/

EXPOSE 5173
CMD [ "npm", "run", "dev" ]
