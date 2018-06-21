FROM redis:4.0.2-alpine

COPY redis-trib.rb /usr/local/bin
COPY clusterize.sh /usr/local/bin
COPY clusterize-robodock.sh /usr/local/bin

RUN apk --update add --no-cache add ruby ruby-irb ruby-rdoc bash docker python && \
    gem install redis