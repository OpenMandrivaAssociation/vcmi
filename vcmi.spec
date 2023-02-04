#define _enable_debug_packages %{nil}
#define debug_package %{nil}
#define debugcflags %{nil}
%define Werror_cflags %nil

%define __noautoprov '(.*)\\.so(.*)'
%define __noautoreq 'libvcmi\\.so(.*)|libminizip\\.so(.*)'

Summary:	Open-source reimplementation and extension of the Heroes III game engine
Name:		vcmi
Version:	1.1.1
Release:	1
License:	GPLv2+
Group:		Games/Strategy
Url:		http://www.vcmi.eu/
#Source0:	https://github.com/vcmi/vcmi/archive/%{version}/%{name}-%{version}.tar.gz
#Current stable 0.99 too broken to fix, also too old.
#In anticipation of a new stable version, instead old broken stuff, we use latest git.
#Source0: 	https://github.com/vcmi/vcmi/archive/develop/%{name}-2022.08.26.tar.gz
Source0:	https://github.com/vcmi/vcmi/archive/refs/tags/%{version}/%{name}-%{version}.tar.gz
# git submodules
Source1:	https://github.com/fuzzylite/fuzzylite/archive/9751a751a17c0682ed5d02e583c6a0cda8bc88e5.tar.gz
Source2:	https://github.com/google/googletest/archive/e2239ee6043f73722e7aa812a459f54a28552929.tar.gz
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
BuildRequires:	pkgconfig(icu-uc)
BuildRequires:	pkgconfig(tbb)
# Lua or Luajit. Pick one. Currently only luajit compiles with VCMI.
BuildRequires:	pkgconfig(luajit)
#BuildRequires:	pkgconfig(lua)
# For data extraction
Requires:	unshield
Requires:	innoextract

%description
VCMI is an open-source project aiming to reimplement the Heroes of Might and
Magic III: In the Wake of Gods game engine, giving it new and extended
possibilities.

To play Heroes III, you will need a copy of the original game.
See VCMI's wiki for Heroes III installation instructions:
http://wiki.vcmi.eu/index.php?title=Installation_on_Linux

%files
%doc README.md AUTHORS ChangeLog
%{_datadir}/applications/%{name}*.desktop
%{_iconsdir}/hicolor/*/apps/%{name}client.png
%{_iconsdir}/hicolor/*x*/apps/vcmieditor.png
%{_libdir}/*.so
%{_libdir}/AI/
#{_libdir}/scripting/libvcmiERM.so
#{_libdir}/scripting/libvcmiLua.so
%{_gamesbindir}/%{name}*
%{_gamesdatadir}/%{name}/
%{_datadir}/metainfo/eu.vcmi.VCMI.metainfo.xml

#----------------------------------------------------------------------------

%prep
%setup -q -n %{name}-%{version}
cd AI
rmdir FuzzyLite
tar xf %{S:1}
mv fuzzylite-* FuzzyLite
cd ..
cd test
rmdir googletest
tar xf %{S:2}
mv googletest-* googletest
cd ..
%autopatch -p1
#sed -i 's!-Werror!!g' AI/FuzzyLite/fuzzylite/CMakeLists.txt

%build
%cmake \
	-DCMAKE_CXX_FLAGS_RELWITHDEBINFO="" \
	-DBIN_DIR=games \
	-DDATA_DIR=share/games/%{name} \
	-DLIB_DIR=%{_lib} \
	-DCMAKE_INSTALL_LIBDIR=%{_libdir} \
	-DCMAKE_SKIP_RPATH=OFF
%make_build

%install
%make_install -C build

# don't ship headers and static libs
rm -rf %{buildroot}/%{_includedir}/fl/
rm -f %{buildroot}/%{_libdir}/libfuzzylite-static.a
