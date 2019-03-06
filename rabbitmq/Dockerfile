FROM rabbitmq:management

RUN apt-get update && apt-get install -y netcat busybox

ADD init.sh /

RUN ["chmod", "+x", "./init.sh"]

RUN ln -sf /bin/busybox /usr/bin/nslookup

RUN sed -i 's/exec "$@"/\
    sh -c "while ! nc -z localhost 15672; do sleep 0.1; done; sleep 3; .\/init.sh" \&\
    \nexec "$@"/' /usr/local/bin/docker-entrypoint.sh
