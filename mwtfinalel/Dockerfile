# Multi-stage Dockerfile for unified Multi-Exam Platform
FROM node:20-alpine AS build

WORKDIR /app

COPY package*.json ./
COPY frontend/package*.json ./frontend/
COPY backend/package*.json ./backend/

RUN npm install
RUN npm install --prefix backend
RUN npm install --prefix frontend

COPY . .

RUN npm run build --prefix frontend

FROM node:20-alpine

WORKDIR /app

COPY --from=build /app/package*.json ./
COPY --from=build /app/backend ./backend
COPY --from=build /app/frontend/dist ./frontend/dist
COPY --from=build /app/node_modules ./node_modules
COPY --from=build /app/backend/node_modules ./backend/node_modules

ENV NODE_ENV=production
ENV PORT=5000

EXPOSE 5000

CMD ["node", "backend/server.js"]
