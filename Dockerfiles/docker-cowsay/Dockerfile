FROM debian:buster-slim

RUN apt-get update                             && \
    apt-get install -y --no-install-recommends    \
        cowsay                                    \
        screenfetch                            && \
        rm -rf /var/lin/apt/lists/*

ENV PATH "$PATH:/usr/games"

#CMD ["cowsay", "To improve is to change; to be perfect is to change often"]
CMD ["-f", "tux", "Default is the easiest choice"]
ENTRYPOINT ["cowsay"]