# TODO:
# - external libraries packages (is there any sense in that?)
#
%define		snap	20121105
%define		rel	6
Summary:	Cinelerra - capturing, editing and production of audio/video material
Summary(pl.UTF-8):	Cinelerra - nagrywanie, obróbka i produkcja materiału audio/video
Name:		cinelerra-cv
Version:	2.2
Release:	0.%{snap}.%{rel}
License:	GPL
Group:		X11/Applications
# git clone git://git.cinelerra.org/CinelerraCV.git cinelerra-cv
Source0:	%{name}-%{snap}.tar.bz2
# Source0-md5:	86559f96282802d0dc3006817a7c11e3
Patch0:		%{name}-build.patch
Patch1:		%{name}-desktop.patch
# http://bugs.cinelerra.org/raw-attachment/ticket/949/remove-support-v4l-buzz-k2-6-38.diff
Patch2:		remove-support-v4l-buzz-k2-6-38.diff
Patch3:		%{name}-ffmpeg.patch
Patch4:		%{name}-format-security.patch
Patch5:		%{name}-ffmpeg2.patch
URL:		http://cinelerra.org/
BuildRequires:	OpenEXR-devel >= 1.2.1
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	OpenGL-devel
BuildRequires:	a52dec-libs-devel
BuildRequires:	alsa-lib-devel >= 1.0.8
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	ffmpeg-devel >= 0.7.1
BuildRequires:	fftw3-devel
BuildRequires:	freetype-devel >= 2.1.4
BuildRequires:	gettext-devel
BuildRequires:	lame-libs-devel >= 3.93.1
BuildRequires:	libavc1394-devel >= 0.5.1
BuildRequires:	libdv-devel
BuildRequires:	libiec61883-devel >= 1.0.0
#BuildRequires:	libmpeg3-devel >= 1.7
BuildRequires:	libpng-devel >= 2:1.4.0
BuildRequires:	libraw1394-devel >= 1.2.0
BuildRequires:	libsndfile-devel >= 1.0.11
BuildRequires:	libstdc++-devel >= 5:3.2.2
BuildRequires:	libtheora-devel >= 1.0-0.alpha4
BuildRequires:	libtiff-devel >= 3.5.7
BuildRequires:	libtool
BuildRequires:	libuuid-devel
BuildRequires:	mjpegtools-devel
BuildRequires:	pkgconfig
%ifarch %{ix86} %{x8664}
BuildRequires:	nasm
%endif
#BuildRequires:	quicktime4linux-devel >= 2.2
BuildRequires:	sed >= 4.0
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXv-devel
BuildRequires:	xorg-lib-libXxf86vm-devel
Requires:	OpenEXR >= 1.2.1
Requires:	alsa-lib >= 1.0.8
Requires:	freetype >= 2.1.4
Requires:	libavc1394 >= 0.5.1
Requires:	libiec61883 >= 1.0.0
#Requires:	libmpeg3 >= 1.7
Requires:	libraw1394 >= 1.2.0
Requires:	libsndfile >= 1.0.11
Requires:	libtheora >= 1.0-0.alpha4
#Requires:	quicktime4linux >= 2.2
Obsoletes:	bcast
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautostrip	.*/microtheme.plugin

%description
There are two types of moviegoers: producers who create new content,
going back over their content at future points for further refinement,
and consumers who want to acquire the content and watch it. Cinelerra
is not intended for consumers. Cinelerra has many features for
uncompressed content, high resolution processing, and compositing,
with very few shortcuts. Producers need these features because of the
need to retouch many generations of footage with alterations to the
format, which makes Cinelerra very complex.

Cinelerra was meant to be a Broadcast 2000 replacement.

This is Community Version.

%description -l pl.UTF-8
Są dwa rodzaje użytkowników zajmujących się filmami: producenci
tworzący nowe filmy, wracający do nich w przyszłości w celu dalszego
wygładzenia, oraz konsumenci, którzy chcą tylko zdobyć film i go
obejrzeć. Cinelerra nie jest dla konsumentów. Program ma wiele
możliwości do edycji nieskompresowanej zawartości, obróbki w wysokiej
rozdzielczości oraz montażu, z bardzo małą liczbą skrótów. Producenci
potrzebują tych możliwości ze względu na konieczność retuszowania oraz
modyfikacji formatu, co czyni program bardzo złożonym.

Cinelerra była tworzona z myślą o zastąpieniu programu Broadcast 2000.

Wersja społecznościowa.

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1
#%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p0

find -name Makefile.am | xargs %{__sed} -i -e 's#^LIBTOOL =.*##g'

%build
rm -f m4/*.m4 *.m4
touch config.rpath
%{__gettextize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoheader}
%{__automake}
%{__autoconf}

%configure \
	CPPFLAGS="%{rpmcppflags} -I/usr/include/freetype2" \
	CXXFLAGS="%{rpmcxxflags} -D__STDC_CONSTANT_MACROS=1" \
%ifarch ppc
	--enable-altivec \
%endif
%ifarch %{ix86} %{x8664}
	--enable-mmx \
	--enable-3dnow \
%endif
	--disable-esd \
	--enable-freetype2 \
	--with-external-ffmpeg \
	--with-alsa-prefix=%{_prefix} \
	--with-fontsdir=%{_fontsdir} \
	--with-plugindir=%{_libdir}/cinelerra

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_libdir}/cinelerra/fonts

%find_lang cinelerra

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f cinelerra.lang
%defattr(644,root,root,755)
%doc doc/* README* TODO
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/cinelerra
%attr(755,root,root) %{_libdir}/cinelerra/*.so
%{_libdir}/cinelerra/*.la
%{_libdir}/cinelerra/shapewipe
%{_libdir}/cinelerra/fonts
%attr(755,root,root) %{_libdir}/lib*.so.*
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*.*
