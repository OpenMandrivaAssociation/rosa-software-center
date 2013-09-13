# Please update git_revision and git_commit_date macros if you want to update sources
# If you update one more time per same day then increment the LAST number of Release: tag
# Do not change FIRST number of Release: tag, it is fixed to make package be newer
# Constants ###################################################################
%define git_revision 7dfb864
%define git_commit_date 20130913

# Required version of Qt5
%define qt_version 5.1.1


# Main Package ################################################################
Name: rosa-software-center
Version: 0.0.0
Release: 21.%{git_commit_date}.1
License: GPLv3+
Group: System/Configuration/Packaging
URL: http://www.rosalab.ru
Summary: Software Center

# Sources #####################################################################
Source0: %{name}-%{version}-%{git_commit_date}-%{git_revision}.tar.gz
Source1: yaml-cpp-0.5.1.tar.gz

# Requires ####################################################################
BuildRequires: cmake
BuildRequires: qmake5 >= %{qt_version}
BuildRequires: qt5-devel >= %{qt_version}
BuildRequires: intltool
BuildRequires: qt5-linguist-tools >= %{qt_version}
BuildRequires: boost-devel
BuildRequires: polkit-qt5-1-devel
BuildRequires: rpm-devel
BuildRequires: curl-devel

Requires: %{_lib}qt5gui5-x11

Obsoletes: %{name}-updater
Obsoletes: %{name}-notifier
Obsoletes: %{name}-core

%description
Software Center main application


# Preparation #################################################################
%prep
%setup -c -a 1


# Build #######################################################################
%build

# Build and install yaml-cpp
cd yaml-cpp-0.5.1
%cmake -DCMAKE_BUILD_TYPE=Release \
    -DBUILD_SHARED_LIBS=OFF \
    -DYAML_CPP_BUILD_TOOLS=OFF
%make
make DESTDIR=../install install

cd %{_builddir}/%{name}-%{version}

# Build SC
%cmake_qt5 -DCMAKE_BUILD_TYPE=Debug \
    -DBUILD_TESTING=OFF \
    -DAPP_GIT_VERSION="%{git_revision}" \
    -DCMAKE_INSTALL_DATADIR="%{_datadir}/%{name}" \
    -DCMAKE_INSTALL_LIBDIR="%{_libdir}/%{name}" \
    -DCMAKE_INSTALL_SYSCONFDIR="%{_sysconfdir}" \
    -DCMAKE_PREFIX_PATH=%{_builddir}/%{name}-%{version}/yaml-cpp-0.5.1/install/%{_prefix}

%make


# Install ####################################################################
%install

%makeinstall_std -C build

# Make autostart of notifier by default => add update skel 
mkdir -p %{buildroot}%{_sysconfdir}/skel/.config/autostart
cp %{buildroot}%{_datadir}/%{name}/desktop_integration/%{name}-notifier.desktop %{buildroot}%{_sysconfdir}/skel/.config/autostart


# Files ######################################################################
%files
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/*
%{_datadir}/%{name}/images/*
%{_datadir}/%{name}/translations/rsc_*.qm
%{_datadir}/%{name}/ui/*
%{_libdir}/%{name}/libsoftwarecenterrpm.so
%{_libdir}/%{name}/libsoftwarecenterurpm.so
%{_datadir}/%{name}/urpm/*
%{_libdir}/%{name}/libsoftwarecenter.so
%{_bindir}/%{name}-pkhelper
%config %{_sysconfdir}/dbus-1/system.d/com.rosalinux.softwarecenter.pk.conf
%{_datadir}/dbus-1/system-services/com.rosalinux.softwarecenter.pk.service
%{_datadir}/polkit-1/actions/com.rosalinux.softwarecenter.pk.policy
%{_bindir}/%{name}-rpmhelper
%config %{_sysconfdir}/dbus-1/system.d/com.rosalinux.softwarecenter.rpm.conf
%{_datadir}/dbus-1/system-services/com.rosalinux.softwarecenter.rpm.service
%{_bindir}/%{name}-notifier
%{_datadir}/%{name}/notifier/*
%{_datadir}/%{name}/translations/notifier_*.qm
%{_datadir}/%{name}/desktop_integration/*
%{_sysconfdir}/skel/.config/autostart/%{name}-notifier.desktop
