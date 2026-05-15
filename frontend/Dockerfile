# Estágio 1: Build da aplicação Vite/React
FROM node:22-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Estágio 2: Servidor Web (Nginx) para servir os arquivos estáticos
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
# Expõe a porta padrão do Nginx
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]