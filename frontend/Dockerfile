# Build stage
FROM node:20-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Serve stage (For production-like local running, serving dist folder via simple http server)
# Since we want a fast dev environment, let's just stick to dev server for local ease of use,
# but it's better to serve the dist if we are simulating production. Let's use serve.
FROM node:20-alpine
WORKDIR /app
COPY --from=build /app/dist /app/dist
RUN npm install -g serve
EXPOSE 3000
CMD ["serve", "-s", "dist", "-l", "3000"]
