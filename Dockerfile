FROM node:20-alpine

# Set shell for pipefail support
SHELL ["/bin/ash", "-o", "pipefail", "-c"]

# Install runtime dependencies
RUN apk add --no-cache curl git

# Set working directory
WORKDIR /app

# Copy dependency files
COPY package*.json ./

# Install Node.js dependencies
RUN npm install --no-audit --no-fund --legacy-peer-deps

# Copy application source code
COPY . .

# Expose server port
EXPOSE 8066

# Define default volumes/directories
VOLUME ["/data", "/media"]

# Healthcheck
HEALTHCHECK --interval=15s --timeout=5s --start-period=10s --retries=3 \
    CMD curl --fail -s http://127.0.0.1:8066/health || exit 1

# Start the application
CMD ["node", "index.js"]
