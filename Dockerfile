FROM alpine
RUN apk update
RUN apk add python2
RUN apk add openssh
RUN apk add rsyslog
RUN apk add py2-pip
RUN apk add net-snmp
RUN pip install config
RUN pip install configparser
RUN pip install paho-mqtt
COPY ./app /usr/src/app
COPY ./etc/inittab /etc/inittab
COPY ./etc/rsyslog.conf /etc/rsyslog.conf
COPY ./etc/init.d/logrotate /etc/init.d/logrotate
COPY ./etc/init.d/snmptrapd /etc/init.d/snmptrapd
COPY ./etc/init.d/sshd /etc/init.d/sshd
COPY ./etc/init.d/syslogd /etc/init.d/syslogd
COPY ./data/package_config.ini /data/package_config.ini
COPY ./etc/ssh/sshd_config /etc/ssh/sshd_config
RUN  ssh-keygen -q -t rsa -N '' -f /etc/ssh/sshd.key
RUN /sbin/init
