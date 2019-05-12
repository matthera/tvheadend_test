%global commit [commit]
%global shortcommit [short_commit]
%global major_no [major_no] 
%global minor_no [minor_no]
%global build_no [build_no]

Name:           tvheadend
Summary:        TV streaming server and Digital Video Recorder
Version:        %{major_no}.%{minor_no}
Release:        %{build_no}~g%{shortcommit}%{?dist}

License:        GPLv3
Group:          Applications/Multimedia
URL:            http://tvheadend.org

Source0:        https://github.com/tvheadend/%{name}/archive/%{commit}.tar.gz#/%{name}-%{shortcommit}.tar.gz

BuildRequires:  gcc
BuildRequires:  systemd-units
BuildRequires:  gettext-devel
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(avahi-client)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(liburiparser)
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavfilter)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libavresample)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(opus)
BuildRequires:  pkgconfig(vpx)
BuildRequires:  pkgconfig(libva)
BuildRequires:  x264-devel x265-devel libdvbcsa-devel wget python git cmake
%ifarch i686 x86_64 i386
BuildRequires:  libva-intel-driver
%endif


Requires:       systemd-units

%description
Tvheadend is a TV streaming server with Digital Video Recorder functionality
for Linux supporting DVB, ATSC, IPTV, SAT>IP, HDHomeRun as input sources.

It can be used as a back-end to HTTP (VLC, MPlayer), HTSP (Movian, Kodi),
SAT>IP and various other clients using these protocols.

%prep
%autosetup -n %{name}-%{commit}

%build
echo %{version}-%{release} > %{_builddir}/%{buildsubdir}/rpm/version
%configure --disable-dvbscan --disable-lockowner --enable-bundle --disable-ffmpeg_static --disable-libx264_static --disable-libx265_static --disable-libvpx_static --disable-libtheora_static --disable-libvorbis_static --disable-libfdkaac_static --disable-libsystemd_daemon
%{__make} %{?_smp_mflags}

%install
# binary
mkdir -p -m755 %{buildroot}%{_bindir}
install -p -m 755 build.linux/tvheadend %{buildroot}%{_bindir}
# systemd
mkdir -p -m755 %{buildroot}%{_sysconfdir}/sysconfig
install -p -m 644 rpm/tvheadend.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/tvheadend
mkdir -p -m755 %{buildroot}%{_unitdir}
install -p -m 644 rpm/tvheadend.service %{buildroot}%{_unitdir}

%pre
getent group tvheadend >/dev/null || groupadd -f -g 283 -r tvheadend
if ! getent passwd tvheadend > /dev/null ; then
  if ! getent passwd 283 > /dev/null ; then
    useradd -r -l -u 283 -g tvheadend -d /home/tvheadend -s /sbin/nologin -c "Tvheadend TV server" tvheadend
  else
    useradd -r -l -g tvheadend -d /home/tvheadend -s /sbin/nologin -c "Tvheadend TV server" tvheadend
  fi
fi
if ! test -d /home/tvheadend ; then
  mkdir -m 0755 /home/tvheadend || exit 1
  chown tvheadend.tvheadend /home/tvheadend || exit 1
fi
exit 0

%post
%systemd_post tvheadend.service

%preun
%systemd_preun tvheadend.service

%postun
%systemd_postun_with_restart tvheadend.service

%files
%{_bindir}/*
%{_sysconfdir}/sysconfig/*
%{_unitdir}/*

%changelog
* Wed May 27 2015 Jaroslav Kysela <perex@perex.cz> 4.0.3-1
- rpmlint fixes

* Mon May 25 2015 Jaroslav Kysela <perex@perex.cz> 4.0.2-1
- fix requires (libs) and improve description
- add support for final version to Source

* Thu May 21 2015 Jaroslav Kysela <perex@perex.cz> 4.0.1-1
- changed versioning system (put changes and git hash to revision)

* Thu May 14 2015 Jaroslav Kysela <perex@perex.cz> 3.9-2842
- add python to BuildRequires

* Wed Mar 25 2015 Bob Lightfoot <boblfoot@gmail.com> 3.9-2658-gb427d7e
- Patching rpm spec file so the arm architecture builds properly

* Mon Oct 13 2014 Jaroslav Kysela <perex@perex.cz> 3.9-1806-g6f3324e
- RPM: Typo fixes

* Mon Oct 13 2014 Jaroslav Kysela <perex@perex.cz> 3.9-1805-g14a7de8
- RPM build - config fixes

* Mon Oct 13 2014 Jaroslav Kysela <perex@perex.cz> 3.9-1803-g392dec0
- Add basic RPM build support

~
