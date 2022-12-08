FROM node
USER node
WORKDIR /home/node
COPY package.json .
RUN npm install
COPY src ./src
COPY static ./static
COPY auth_config.js .
COPY vite.config.js .
COPY svelte.config.js .
RUN npm run build
CMD [ "npm", "run", "preview" ]
