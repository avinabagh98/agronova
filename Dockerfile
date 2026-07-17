# Stage 1: Build the Next.js frontend
FROM node:18-alpine AS builder

WORKDIR /app/frontend

# Install dependencies first for better caching
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm install

# Copy the rest of the frontend source code
COPY frontend/ ./

# Build Next.js
ENV NEXT_PUBLIC_API_URL=/api/py
RUN npm run build


# Stage 2: Final Image with Python and Node.js
FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

# Install Node.js 18
RUN apt-get update && apt-get install -y curl \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy backend code
COPY backend/ ./backend/

# Copy Next.js standalone build output
COPY --from=builder /app/frontend/.next/standalone ./frontend/

# Copy Next.js static files
COPY --from=builder /app/frontend/.next/static ./frontend/.next/static

# Copy startup script
COPY start.sh ./
RUN chmod +x start.sh

ENV NODE_ENV=production
ENV PORT=3000

EXPOSE 3000

CMD ["./start.sh"]