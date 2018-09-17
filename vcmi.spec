%define _enable_debug_packages %{nil}
%define debug_package %{nil}
%define debugcflags %{nil}
%define Werror_cflags %nil

%define __noautoprov '(.*)\\.so(.*)'
%define __noautoreq 'libvcmi\\.so(.*)|libminizip\\.so(.*)'

Summary:	Open-source reimplementation and extension of the Heroes III game engine
Name:		vcmi
Version:	0.99
Release:	1
License:	GPLv2+
Group:		Games/Strategy
Url:		http://www.vcmi.eu/
Source0:	https://github.com/vcmi/vcmi/archive/%{version}/%{name}-%{version}.tar.gz
BuildRequires:	cmake
BuildRequires:	qmake5
BuildRequires:	boost-devel
BuildRequires:	pkgconfig(libavcodec)
BuildRequires:	pkgconfig(libavformat)
BuildRequires:	pkgconfig(libavutil)
BuildRequires:	pkgconfig(libswscale)
BuildRequires:	pkgconfig(Qt5Network)
BuildRequires:	pkgconfig(Qt5Widgets)
BuildRequires:	pkgconfig(sdl2)
BuildRequires:	pkgconfig(SDL2_image)
BuildRequires:	pkgconfig(SDL2_mixer)
BuildRequires:	pkgconfig(SDL2_ttf)
BuildRequires:	pkgconfig(minizip)
BuildRequires:	pkgconfig(zlib)
# For data extraction
Requires:	unshield

%description
VCMI is an open-source project aiming to reimplement the Heroes of Might and
Magic III: In the Wake of Gods game engine, giving it new and extended
possibilities.

To play Heroes III, you will need a copy of the original game.
See VCMI's wiki for Heroes III installation instructions:
http://wiki.vcmi.eu/index.php?title=Installation_on_Linux

%files
%doc README.md README.linux AUTHORS ChangeLog
%{_datadir}/applications/%{name}*.desktop
%{_iconsdir}/hicolor/*/apps/%{name}client.png
%{_libdir}/%{name}/
%{_gamesbindir}/%{name}*
%{_gamesdatadir}/%{name}/

#----------------------------------------------------------------------------

%prep
%setup -q
sed -i 's!-Werror!!g' AI/FuzzyLite/fuzzylite/CMakeLists.txt

%build
%cmake \
	-DCMAKE_CXX_FLAGS_RELWITHDEBINFO="" \
	-DBIN_DIR=games \
	-DDATA_DIR=share/games/%{name} \
	-DLIB_DIR=%{_lib}/%{name} \
	-DCMAKE_INSTALL_LIBDIR=%{_lib} \
	-DCMAKE_SKIP_RPATH=OFF
%make

%install
%makeinstall_std -C build

# don't ship headers and static libs
rm -rf %{buildroot}/%{_includedir}/fl/
rm -f %{buildroot}/%{_libdir}/libfuzzylite-static.a
