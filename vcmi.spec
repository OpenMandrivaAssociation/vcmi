#define _enable_debug_packages %{nil}
#define debug_package %{nil}
#define debugcflags %{nil}
%define Werror_cflags %nil

%define __noautoprov '(.*)\\.so(.*)'
%define __noautoreq 'libvcmi\\.so(.*)|libminizip\\.so(.*)'

Summary:	Open-source reimplementation and extension of the Heroes III game engine
Name:		vcmi
Version:	1.6.8
Release:	1
License:	GPLv2+
Group:		Games/Strategy
Url:		https://www.vcmi.eu/
Source0:	https://github.com/vcmi/vcmi/archive/refs/tags/%{version}/%{name}-%{version}.tar.gz
# git submodules
Source1:	https://github.com/fuzzylite/fuzzylite/archive/fuzzylite-13b3122f5c353c0389ed4e66041d548c44ec9df6.tar.gz
Source2:	https://github.com/google/googletest/archive/e2239ee6043f73722e7aa812a459f54a28552929.tar.gz
#Patch0:		https://patch-diff.githubusercontent.com/raw/vcmi/vcmi/pull/4091.patch
# Drop with 1.6 release
#Patch3:		fix-boost-1.86.0.patch
#Patch4:		fix-boost-1.87.0.patch
BuildRequires:	cmake
#BuildRequires:	qmake5
BuildRequires:	cmake(Qt6)
BuildRequires:	qmake-qt6
BuildRequires:	boost-devel
BuildRequires:	pkgconfig(libavcodec)
BuildRequires:	pkgconfig(libavformat)
BuildRequires:	pkgconfig(libavutil)
BuildRequires:	pkgconfig(libswscale)
BuildRequires:	pkgconfig(libunwind-llvm)
BuildRequires:	qt6-qttools
BuildRequires: 	qt6-qttools-linguist
BuildRequires:	qt6-qtbase-theme-gtk3
BuildRequires:  cmake(Qt6LinguistTools)
BuildRequires:	cmake(Qt6DBus)
BuildRequires: 	cmake(Qt6Core)
BuildRequires: 	cmake(Qt6Gui)
BuildRequires:	cmake(Qt6Network)
#BuildRequires:	cmake(Qt5Tools)
BuildRequires:	cmake(Qt6Widgets)
BuildRequires:	pkgconfig(sdl2)
BuildRequires:	pkgconfig(SDL2_image)
BuildRequires:	pkgconfig(SDL2_mixer)
BuildRequires:	pkgconfig(SDL2_ttf)
BuildRequires:	pkgconfig(minizip)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(icu-uc)
BuildRequires:	pkgconfig(tbb)
BuildRequires:	%{_lib}tbbind
# Lua or Luajit. Pick one. Currently only luajit compiles with VCMI.
BuildRequires:	pkgconfig(luajit)
#BuildRequires:	pkgconfig(lua)
BuildRequires:	cmake(VulkanHeaders)
BuildRequires:  pkgconfig(vulkan)
BuildRequires:	pkgconfig(xkbcommon-x11)
BuildRequires:	pkgconfig(xkbcommon)
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
%{_datadir}/applications/%{name}*.desktop
%{_iconsdir}/hicolor/*/apps/%{name}client.png
%{_iconsdir}/hicolor/*x*/apps/vcmieditor.png
%{_iconsdir}/hicolor/scalable/apps/vcmiclient.svg
%{_libdir}/*.so
%{_libdir}/AI/
%{_bindir}/%{name}*
%{_datadir}/%{name}/
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
	-DLIB_DIR=%{_lib} \
	-DCMAKE_INSTALL_LIBDIR=%{_libdir} \
 	-DENABLE_INNOEXTRACT=OFF \
	-DCMAKE_SKIP_RPATH=OFF
%make_build

%install
%make_install -C build

# don't ship headers and static libs
rm -rf %{buildroot}/%{_includedir}/fl/
rm -f %{buildroot}/%{_libdir}/libfuzzylite-static.a
