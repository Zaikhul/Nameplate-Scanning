# Dockerfile for App
FROM node:16.13-alpine as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM node:16.13-alpine as production-stage
WORKDIR /app
#COPY --from=build-stage /app/dist ./dist
RUN npm install -g serve
EXPOSE 8080
CMD ["serve", "-s", "dist"]
