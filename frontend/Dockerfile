FROM node:20-alpine
WORKDIR /app
COPY package.json ./
RUN npm install
COPY . .
ARG NEXT_PUBLIC_API_URL=http://localhost:8000
ENV NEXT_PUBLIC_API_URL=http://localhost:8000
RUN npm run build
EXPOSE 3000
CMD npm start
