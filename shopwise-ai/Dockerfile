FROM node:22-alpine AS frontend-build
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci
COPY index.html vite.config.ts tsconfig.json tailwind.config.js postcss.config.js ./
COPY frontend ./frontend
RUN npm run build

FROM python:3.12-slim AS runtime
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY backend ./backend
COPY public ./public
COPY --from=frontend-build /app/frontend/dist ./frontend/dist
COPY .env.example ./
EXPOSE 3000
CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-3000}"]
