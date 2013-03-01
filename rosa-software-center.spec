# TODO: help
# Constants ###################################################################
%define git_version git20130301

# TODO: There are no special macros for Qt5 for now, so, the paths are hardcoded for now
%define qt5_path /usr/lib/qt5


# Package #####################################################################
Name: rosa-software-center
Version: 0.0.0
Release: 0.%{git_version}.1
Summary: Software Center 
License: GPLv2+
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

Requires: qt5-desktop-components


%description
Software Center 


# Preparation #################################################################
%prep
%setup -c


# Build #######################################################################
echo "Configuring..."

mkdir -p build
cd build

# TODO: from rpm macros
export CFLAGS="${CFLAGS:--O2 -Wa,--compress-debug-sections -gdwarf-4 -fvar-tracking-assignments -frecord-gcc-switches -Wstrict-aliasing=2 -pipe -Wformat -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2 -fstack-protector --param=ssp-buffer-size=4 -fPIC}"
export CXXFLAGS="${CXXFLAGS:--O2 -Wa,--compress-debug-sections -gdwarf-4 -fvar-tracking-assignments -frecord-gcc-switches -Wstrict-aliasing=2 -pipe -Wformat -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2 -fstack-protector --param=ssp-buffer-size=4 -fPIC}"
export FFLAGS="${FFLAGS:--O2 -Wa,--compress-debug-sections -gdwarf-4 -fvar-tracking-assignments -frecord-gcc-switches -Wstrict-aliasing=2 -pipe -Wformat -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2 -fstack-protector --param=ssp-buffer-size=4 -fPIC}" 
export LDFLAGS="$LDFLAGS -Wl,--as-needed -Wl,--no-undefined -Wl,-z,relro -Wl,-O1 -Wl,--build-id -Wl,--enable-new-dtags -Wl,--hash-style=gnu"

# 'cmake' macro isn't God mode (: => use normal mode
cmake .. \
    -DCMAKE_INSTALL_PREFIX="%{buildroot}/usr" \
    -DCMAKE_PREFIX_PATH=%{qt5_path} \
    -DCMAKE_BUILD_TYPE=Release \
    -DBUILD_SHARED_LIBS:BOOL=ON \
    -DBUILD_TESTS:BOOL=OFF \
    -DLIBRARY_INSTALL_DIR=%{_lib} 

echo "Building..."

make VERBOSE=1 install

chmod 0755 %{buildroot}/usr/%{_lib}/*.so*

# make file list
sed -e "s|%{buildroot}||g" ./install_manifest.txt > ./filelist.txt

# Files ######################################################################
%files -f build/filelist.txt

