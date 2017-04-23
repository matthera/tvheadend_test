FROM fedora:25
RUN dnf -y install https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-25.noarch.rpm
RUN dnf -y install fedora-packager mock mock-rpmfusion-free rpmdevtools
RUN groupadd build && useradd -g build build
RUN usermod -a -G mock build
USER build
RUN rpmdev-setuptree
VOLUME /home/build/rpmbuild
WORKDIR /home/build
