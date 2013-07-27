# Please update git_revision and increment release number (first number separated by point)
# Constants ###################################################################
%define git_revision 2601026

# Required version of Qt5
%define qt_version 5.1.0

# Main name of package
%define pkg_name rosa-software-center

# Names for library packages
%define lib_name %mklibname %{pkg_name}


# Main Package ################################################################
Name: %{pkg_name}
Version: 0.0.0
Release: 17.%{git_revision}
Summary: Software Center 
License: GPLv3+
Vendor: ROSA
Packager: Dmitry Ashkadov <dmitry.ashkadov@rosalab.ru>
Group: System/Configuration/Packaging
URL: http://www.rosalab.ru

# Sources #####################################################################
Source0: %{name}-%{version}-%{git_revision}.tar.gz

# Requires ####################################################################
BuildRequires: cmake
BuildRequires: qmake5 >= %{qt_version}
BuildRequires: qt5-devel >= %{qt_version}
BuildRequires: intltool
BuildRequires: qt5-linguist-tools >= %{qt_version}

Requires: %{lib_name}-core == %{EVRD}
Requires: %{name}-pkhelper == %{EVRD}
Requires: %{name}-updater == %{EVRD}

%description
Software Center main application


# RPM support library #########################################################
%package -n %{lib_name}-rpm
Summary: RPM support library for Software Center
Group: System/Libraries

BuildRequires: rpm-devel

%description
RPM support library for Software Center


# URPM support library ########################################################
%package -n %{lib_name}-urpm
Summary: URPM support library for Software Center
Group: System/Libraries

Requires: perl-URPM

%description
URPM support library for Software Center


# Core library ################################################################
%package -n %{lib_name}-core
Summary: Core library for Software Center
Group: System/Libraries

BuildRequires: polkit-qt5-1-devel

Requires: %{lib_name}-rpm == %{EVRD}
Requires: %{lib_name}-urpm == %{EVRD}

%description
Core library for Software Center


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
    -DCMAKE_INSTALL_LIBDIR="%{_lib}" \
    -DAPP_GIT_VERSION="%{git_revision}"

# Donot use macros makeinstall_std because it generates unstripped binaries
make -j4 DESTDIR="%{buildroot}" install/strip



# Files ######################################################################
%files
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/*
%{_datadir}/%{name}-%{version}/images/*
%{_datadir}/%{name}-%{version}/translations/rsc_*.qm
%{_datadir}/%{name}-%{version}/ui/*


%files -n %{lib_name}-rpm
%{_libdir}/libsoftwarecenterrpm.so


%files -n %{lib_name}-urpm
%{_libdir}/libsoftwarecenterurpm.so
%{_datadir}/%{name}-%{version}/urpm/*


%files -n %{lib_name}-core
%{_libdir}/libsoftwarecenter.so


%files pkhelper
%{_bindir}/%{name}-helper
/etc/dbus-1/system.d/com.rosalinux.softwarecenter.conf
/usr/share/dbus-1/system-services/com.rosalinux.softwarecenter.service
/usr/share/polkit-1/actions/com.rosalinux.softwarecenter.policy


%files notifier
%{_bindir}/%{name}-notifier
%{_datadir}/%{name}-%{version}/notifier/*
%{_datadir}/%{name}-%{version}/translations/notifier_*.qm


%files updater
/etc/systemd/system/rosa-software-center-updater.service
/etc/systemd/system/rosa-software-center-updater.timer
%{_bindir}/%{name}-updater.sh

