FROM node
USER root
WORKDIR /app
COPY package.json .
RUN npm install
COPY src ./src
COPY static ./static
COPY scripts ./scripts
COPY auth_config.js .
COPY rollup.config.js .
RUN npm run build
CMD [ "npm", "start" ]
