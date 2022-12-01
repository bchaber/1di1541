FROM node
USER node
WORKDIR /home/node
COPY package.json .
RUN npm install
COPY index.html .
COPY auth_config.js .
COPY jsconfig.json .
COPY vite.config.js .
COPY public ./public
COPY src ./src
RUN npm run build
CMD [ "npm", "run", "preview" ]
