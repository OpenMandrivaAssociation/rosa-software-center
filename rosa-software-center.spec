# TODO: help
# Constants ###################################################################
%define git_version git20130321

# TODO: There are no special macros for Qt5 for now, so, the paths are hardcoded for now
%define qt5_path /usr/lib/qt5


# Package #####################################################################
Name: rosa-software-center
Version: 0.0.0
Release: 0.%{git_version}.2
Summary: Software Center 
License: GPLv3+
Vendor: ROSA
Packager: Dmitry Ashkadov <dmitry.ashkadov@rosalab.ru>
Group: System/Configuration/Packaging
URL: http://www.rosalab.ru

# Sources #####################################################################
Source0: rosa-software-center-%{version}-%{git_version}.tar.gz

Source100: rosa-software-center.rpmlintrc

# Requires ####################################################################
BuildRequires: cmake
BuildRequires: qmake5
BuildRequires: qt5-devel

Requires: %{_lib}qt5gui5-x11
Requires: qt5-desktop-components


%description
Software Center 


# Preparation #################################################################
%prep
%setup -c


# Build #######################################################################
%build
# there is no 'cmake_qt5' macro => use standard macro 'cmake'
%cmake -DCMAKE_PREFIX_PATH=%{qt5_path} -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTS:BOOL=OFF

%makeinstall_std

# Files ######################################################################
%files -f build/install_manifest.txt

