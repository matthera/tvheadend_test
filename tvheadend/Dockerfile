FROM [arch]/fedora:[dist]
RUN dnf -y install https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-[dist].noarch.rpm
COPY [tvheadend-rpm] .
RUN dnf -y install ./[tvheadend-rpm]
EXPOSE 9981 9982
VOLUME /home/tvheadend
ENTRYPOINT ["/usr/bin/tvheadend", "-c", "/home/tvheadend"]
