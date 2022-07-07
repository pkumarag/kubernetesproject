FROM ubuntu

ENV TZ=Asia/Dubai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update
RUN apt-get -y install apache2
RUN apt-get update
RUN apt-get -y install apache2-utils
RUN apt install -y tcl

RUN apt-get -y  install zip
RUN apt-get install unzip

ADD https://www.free-css.com/assets/files/free-css-templates/download/page247/kindle.zip /var/www/html/

WORKDIR /var/www/html

RUN unzip kindle.zip
RUN cp -rvf markups-kindle/* .


EXPOSE 8090
ENTRYPOINT ["apache2ctl"]
CMD ["-DFOREGROUND"]
