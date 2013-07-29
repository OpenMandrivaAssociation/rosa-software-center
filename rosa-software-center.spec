# Please update git_revision and git_commit_date macros if you want to update sources
# If you update one more time in the same day then increment LAST number of Release: tag
# Do not change FIRST number of Release: tag, it is fixed to make package be newer
# Constants ###################################################################
%define git_revision d8fbbba
%define git_commit_date 20130729

# Required version of Qt5
%define qt_version 5.1.0


# Main Package ################################################################
Name: rosa-software-center
Version: 0.0.0
Release: 20.%{git_commit_date}.1
License: GPLv3+
Group: System/Configuration/Packaging
URL: http://www.rosalab.ru
Summary: Software Center 

# Sources #####################################################################
Source0: %{name}-%{version}-%{git_commit_date}-%{git_revision}.tar.gz

# Requires ####################################################################
BuildRequires: cmake
BuildRequires: qmake5 >= %{qt_version}
BuildRequires: qt5-devel >= %{qt_version}
BuildRequires: intltool
BuildRequires: qt5-linguist-tools >= %{qt_version}

Requires: %{name}-pkhelper == %{EVRD}
Requires: %{name}-updater == %{EVRD}

%description
Software Center main application


# Core library ################################################################
%package core
Summary: Core library for Software Center and RPM/URPM support libraries 
Group: System/Libraries

BuildRequires: polkit-qt5-1-devel
BuildRequires: rpm-devel
BuildRequires: curl-devel

%description
Core library for Software Center and RPM/URPM support libraries


# Polkit helper ###############################################################
%package pkhelper
Summary: PolicyKit helper for Software Center
Group: System/Configuration/Packaging

BuildRequires: polkit-qt5-1-devel

%description
PolicyKit helper for Software Center


# Notifier application ########################################################
%package notifier
Summary: Notifier for Software Center
Group: System/Configuration/Packaging

BuildRequires: qt5-linguist-tools >= %{qt_version}

%description
Notifier for Software Center


# Update Service ##############################################################
%package updater
Summary: System service for checking updates 
Group: System/Configuration/Packaging
BuildArch: noarch

%description
System service for checking updates


# Preparation #################################################################
%prep
%setup -c


# Build #######################################################################
%build
%cmake_qt5 -DCMAKE_BUILD_TYPE=Release \
    -DBUILD_TESTING=OFF \
    -DAPP_GIT_VERSION="%{git_revision}" \
    -DCMAKE_INSTALL_DATADIR="%{_datadir}/%{name}" \
    -DCMAKE_INSTALL_LIBDIR="%{_libdir}/%{name}" \
    -DCMAKE_INSTALL_SYSCONFDIR="%{_sysconfdir}"

%make


# Install ####################################################################
%install

%makeinstall_std -C build



# Files ######################################################################
%files
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/*
%{_datadir}/%{name}/images/*
%{_datadir}/%{name}/translations/rsc_*.qm
%{_datadir}/%{name}/ui/*


%files core
%{_libdir}/%{name}/libsoftwarecenterrpm.so
%{_libdir}/%{name}/libsoftwarecenterurpm.so
%{_datadir}/%{name}/urpm/*
%{_libdir}/%{name}/libsoftwarecenter.so


%files pkhelper
%{_bindir}/%{name}-helper
%config %{_sysconfdir}/dbus-1/system.d/com.rosalinux.softwarecenter.conf
%{_datadir}/dbus-1/system-services/com.rosalinux.softwarecenter.service
%{_datadir}/polkit-1/actions/com.rosalinux.softwarecenter.policy


%files notifier
%{_bindir}/%{name}-notifier
%{_datadir}/%{name}/notifier/*
%{_datadir}/%{name}/translations/notifier_*.qm


%files updater
%{_sysconfdir}/systemd/system/rosa-software-center-updater.service
%{_sysconfdir}/systemd/system/rosa-software-center-updater.timer
%{_bindir}/%{name}-updater.sh

