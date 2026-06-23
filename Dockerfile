#Use a light version

FROM node:20-slim

WORKDIR /app

#Copy the dependency configuration files.
COPY package*.json ./
RUN rm -f package-lock.json && npm install

#Copy all the React cod
COPY . .
#Expose Vite port
EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host"]