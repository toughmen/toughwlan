FROM index.alauda.cn/toughstruct/tough-pypy:twlan
MAINTAINER jamiesun <jamiesun.net@gmail.com>

VOLUME ["/var/toughwlan"]

ADD scripts/toughrun /usr/local/bin/toughrun
RUN chmod +x /usr/local/bin/toughrun
RUN /usr/local/bin/toughrun install

# admin web port
EXPOSE 1810

# portal listen port
EXPOSE 50100/udp


CMD ["/usr/local/bin/supervisord","-c","/etc/supervisord.conf"]
