# Use Node.js 18 Alpine as base image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Expose port 4173 (Vite preview default)
EXPOSE 4173

# Run the preview server
CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0"]