# --- Stage 1: Dependency & Build Management ---
FROM node:20-alpine AS builder
WORKDIR /app

# Declare build arguments to make values dynamic during building
ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL

COPY package*.json ./
RUN npm ci

COPY . .
# Compile the client layout components 
RUN npm run build

# --- Stage 2: Minimal Runtime Surface ---
FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production

# Copy built code structure and dependencies directly
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public

EXPOSE 3000
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

CMD ["npm", "run", "start"]