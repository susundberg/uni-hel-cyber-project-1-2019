FROM ubuntu:18.04

RUN apt-get update && apt-get -y upgrade

RUN apt-get install -y python3 python3-requests libsqlite3-0


ADD hackforum /hackforum
RUN cd / && python3 /hackforum/tests/test_main.py 

EXPOSE 8080/tcp
CMD ["python3", "/hackforum/main.py"]



