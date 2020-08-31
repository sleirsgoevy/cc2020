FROM ubuntu:20.04 AS builder


RUN DEBIAN_FRONTEND=noninteractive apt-get update -qy
RUN DEBIAN_FRONTEND=noninteractive apt-get install -qy clang make
RUN rm -rf /var/cache/apt/

RUN useradd -m builder

WORKDIR /home/builder
USER builder

COPY --chown=builder:builder loader.c .
COPY --chown=builder:builder dejavu.c .
COPY --chown=builder:builder Makefile .

RUN make all


FROM ubuntu:20.04


RUN useradd -m challenge
RUN useradd pwn

WORKDIR /home/challenge/

COPY --from=builder /home/builder/dejavu .
RUN chown root:pwn dejavu
RUN chmod g+s dejavu

COPY --from=builder /home/builder/loader .
RUN chown challenge:challenge ./loader
RUN chmod 700 ./loader

COPY flag.txt .
RUN chown root:pwn flag.txt
RUN chmod 440 flag.txt

RUN mkdir storage
RUN chown root:pwn storage
RUN chmod 773 ./storage 
RUN chmod +t ./storage

USER challenge

CMD ["./loader"]
