FROM ubuntu:latest
LABEL authors="randysalas"

ENTRYPOINT ["top", "-b"]