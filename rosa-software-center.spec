# Constants ###################################################################
# Required version of Qt5
%define qt_version 5.2.1


# Main Package ################################################################
Name: rosa-software-center
Version: 0.1.0
Release: 4
License: GPLv3+
Group: System/Configuration/Packaging
URL: http://www.rosalab.ru
Summary: Software Center

# Sources #####################################################################
Source0: %{name}-%{version}.tar.gz
Source1: yaml-cpp-0.5.1.tar.gz

# Patches #####################################################################
Patch0: rsc_disable_check_main_repo.patch

# to test metadata generation without ABF
Patch1: try_local_metadata.patch

Patch2:	rosa-software-center-clang.patch
Patch3:	rosa-software-center-link.patch

# Requires ####################################################################
BuildRequires: cmake
BuildRequires: qmake5 >= %{qt_version}
BuildRequires: pkgconfig(Qt5Core) >= %{qt_version}
BuildRequires: pkgconfig(Qt5Quick) >= %{qt_version}
BuildRequires: pkgconfig(Qt5DBus) >= %{qt_version}
BuildRequires: pkgconfig(Qt5Gui) >= %{qt_version}
BuildRequires: pkgconfig(Qt5Svg) >= %{qt_version}
BuildRequires: intltool
BuildRequires: qt5-linguist-tools >= %{qt_version}
BuildRequires: boost-devel
BuildRequires: polkit-qt5-1-devel
BuildRequires: rpm-devel
BuildRequires: curl-devel
BuildRequires: xapian-devel
BuildRequires: pkgconfig(QtCore)

Requires: %{_lib}qt5gui5-x11

Obsoletes: %{name}-updater
Obsoletes: %{name}-notifier
Obsoletes: %{name}-core

%description
Software Center main application.


# Preparation #################################################################
%prep
%setup -c -a 1
%patch0 -p1
%patch1 -p1
%patch2 -p0
%patch3 -p0

# upstream polkit qt5 no longer uses POLKITQT5 var prefix
sed -i 's/POLKITQT5/POLKITQT/' */CMakeLists.txt

# Build #######################################################################
%build
%global optflags %{optflags} -Qunused-arguments

# Build and install yaml-cpp
cd yaml-cpp-0.5.1
%cmake -DCMAKE_BUILD_TYPE=Release \
    -DBUILD_SHARED_LIBS=OFF \
    -DYAML_CPP_BUILD_TOOLS=OFF
%make
make DESTDIR=../install install

cd %{_builddir}/%{name}-%{version}

# Build SC
mkdir -p build 
cd build
export CXXFLAGS="-O2 -Wa,--compress-debug-sections -ggdb3 -Wstrict-aliasing=2 -pipe -Wformat -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2 -fstack-protector --param=ssp-buffer-size=4 -fPIC"
cmake .. -DCMAKE_BUILD_TYPE=Debug \
    -DCMAKE_INSTALL_PREFIX="/usr" \
    -DBUILD_TESTING=OFF \
    -DAPP_GIT_VERSION="%{version}-%{release}" \
    -DCMAKE_INSTALL_DATADIR="%{_datadir}/%{name}" \
    -DCMAKE_INSTALL_LIBDIR="%{_libdir}" \
    -DCMAKE_INSTALL_SYSCONFDIR="%{_sysconfdir}" \
    -DCMAKE_PREFIX_PATH=%{_builddir}/%{name}-%{version}/yaml-cpp-0.5.1/install/%{_prefix}

%make VERBOSE=1


# Install ####################################################################
%install

%makeinstall_std -C build

# Make autostart of notifier by default => add update skel 
mkdir -p %{buildroot}%{_sysconfdir}/skel/.config/autostart
cp %{buildroot}%{_datadir}/%{name}/desktop_integration/%{name}-notifier.desktop %{buildroot}%{_sysconfdir}/skel/.config/autostart


# Files ######################################################################
%files

# main application
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/*
%{_datadir}/%{name}/images/*
%{_datadir}/%{name}/translations/rsc_*.qm
%{_datadir}/%{name}/ui/*
%{_datadir}/%{name}/ui_modules/*

# rpm support lib
%{_libdir}/libsoftwarecenterrpm.so

# urpm support lib
%{_libdir}/libsoftwarecenterurpm.so
%{_datadir}/%{name}/urpm/*

# core lib
%{_libdir}/libsoftwarecenter.so

# pkhelper
%{_bindir}/%{name}-pkhelper
%config %{_sysconfdir}/dbus-1/system.d/com.rosalinux.softwarecenter.pk.conf
%{_datadir}/dbus-1/system-services/com.rosalinux.softwarecenter.pk.service
%{_datadir}/polkit-1/actions/com.rosalinux.softwarecenter.pk.policy

# rpmhelper
%{_bindir}/%{name}-rpmhelper
%config %{_sysconfdir}/dbus-1/system.d/com.rosalinux.softwarecenter.rpm.conf
%{_datadir}/dbus-1/system-services/com.rosalinux.softwarecenter.rpm.service

# notifier
%{_bindir}/%{name}-notifier
%{_datadir}/%{name}/notifier/*

# notifier-trayicon
%{_bindir}/%{name}-notifier-trayicon
%{_datadir}/%{name}/notifier_trayicon/*

# desctop integration: icon, etc
%{_datadir}/%{name}/desktop_integration/*
%{_sysconfdir}/skel/.config/autostart/%{name}-notifier.desktop
