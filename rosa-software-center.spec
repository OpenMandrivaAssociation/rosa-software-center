# Please update git_revision and increment release number (first number separated by point)
# Constants ###################################################################
%define git_revision bce670b

# TODO: There are no special macros for Qt5 for now, so, the paths are hardcoded for now
%define qt5_path /usr/lib/qt5


# Package #####################################################################
Name: rosa-software-center
Version: 0.0.0
Release: 8.%{git_revision}
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
BuildRequires: qmake5
BuildRequires: qt5-devel
BuildRequires: qt5-linguist-tools
BuildRequires: intltool
BuildRequires: polkit-qt5-1-devel

Requires: %{_lib}qt5gui5-x11
Requires: qt5-desktop-components
Requires: %{_lib}polkit-qt5-core-1_1


%description
Software Center 


# Preparation #################################################################
%prep
%setup -c


# Build #######################################################################
%build
# there is no 'cmake_qt5' macro => use standard macro 'cmake'
%cmake -DCMAKE_PREFIX_PATH=%{qt5_path} \
    -DCMAKE_BUILD_TYPE=Release \
    -DBUILD_TESTING=OFF \
    -DCMAKE_INSTALL_LIBDIR="%{_lib}" \
    -DAPP_GIT_VERSION="%{git_revision}"

# Donot use macros makeinstall_std because it generates unstripped binaries
make -j4 DESTDIR="%{buildroot}" install/strip

# Files ######################################################################
%files -f build/install_manifest.txt

