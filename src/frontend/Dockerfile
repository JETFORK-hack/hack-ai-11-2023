# build-stage
FROM node:lts-alpine as build-stage

RUN mkdir -p /app

WORKDIR /app

COPY package*.json ./
COPY yarn.lock ./

RUN yarn install --frozen-lockfile

COPY . .

RUN yarn build


# production-stage
FROM nginx:stable-alpine as production-stage

COPY nginx.conf /etc/nginx/conf.d/default.conf

RUN rm -rf /usr/share/nginx/html/*

COPY --from=build-stage /app/dist /usr/share/nginx/html

CMD ["nginx", "-g", "daemon off;"]



# FROM node:16 as build

# WORKDIR /app

# COPY package.json yarn.lock /app/

# RUN yarn install --frozen-lockfile

# COPY . /app/


# RUN yarn build


# FROM nginx:latest

# RUN ls

# COPY --from=build /app/dist /usr/share/nginx/html

# COPY --from=build /app/nginx.conf /etc/nginx/conf.d/default.conf
