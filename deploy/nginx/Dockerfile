FROM nginx:1.13
MAINTAINER Mikael Mukhsikaroyan <example@gmail.com>

# Delete the default welcome to nginx page.
RUN rm /usr/share/nginx/html/*

# Copy over the custom nginx and default configs.
COPY configs/nginx.conf /etc/nginx/nginx.conf
COPY configs/default.conf /etc/nginx/conf.d/default.conf

# Allow us to customize the entrypoint of the image.
COPY docker_entry.sh /
RUN chmod +x /docker_entry.sh
ENTRYPOINT ["/docker_entry.sh"]

CMD ["nginx", "-g", "daemon off;"]
