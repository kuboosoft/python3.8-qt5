Summary: PyQt5 is Python bindings for Qt5
Name:    python3.8-qt5
Version: 5.14.2
Release: 3%{?dist}

License: GPLv3
Url:     http://www.riverbankcomputing.com/software/pyqt/
Source0: https://files.pythonhosted.org/packages/4d/81/b9a66a28fb9a7bbeb60e266f06ebc4703e7e42b99e3609bf1b58ddd232b9/PyQt5-%{version}.tar.gz


## upstreamable patches
Patch0: python-qt5_sipdir.patch
# support newer Qt5 releases
Patch1: PyQt5-Timeline.patch

BuildRequires: chrpath
BuildRequires: findutils
BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(dbus-python)
BuildRequires: pkgconfig(phonon4qt5)
BuildRequires: pkgconfig(Qt5Core) >= 5.5

BuildRequires: pkgconfig(Enginio)

BuildRequires: pkgconfig(Qt5Bluetooth)
BuildRequires: pkgconfig(Qt5DBus)
BuildRequires: pkgconfig(Qt5Designer)
BuildRequires: pkgconfig(Qt5Gui)
BuildRequires: pkgconfig(Qt5Location)
BuildRequires: pkgconfig(Qt5Multimedia) pkgconfig(libpulse-mainloop-glib)
BuildRequires: pkgconfig(Qt5Nfc)
BuildRequires: pkgconfig(Qt5Network) pkgconfig(Qt5OpenGL)
BuildRequires: pkgconfig(Qt5Positioning)
BuildRequires: pkgconfig(Qt5Quick) pkgconfig(Qt5QuickWidgets)
#BuildRequires: pkgconfig(Qt5Script)
BuildRequires: pkgconfig(Qt5Sensors)
BuildRequires: pkgconfig(Qt5SerialPort)
BuildRequires: pkgconfig(Qt5Sql) pkgconfig(Qt5Svg) pkgconfig(Qt5Test)
BuildRequires: pkgconfig(Qt5X11Extras)
BuildRequires: pkgconfig(Qt5Xml) pkgconfig(Qt5XmlPatterns)
BuildRequires: pkgconfig(Qt5WebChannel)
BuildRequires: pkgconfig(Qt5WebSockets)


BuildRequires: python3.8-devel 
BuildRequires: python3.8-dbus
BuildRequires: sip
BuildRequires: python3.8-sip


%description
%{summary}.


%prep
%setup -n PyQt5-%{version}%{?snap:.%{snap}}

#patch0 -p1
#patch1 -p1

%build

#PATH=%{_qt5_bindir}:$PATH ; export PATH

## see also https://www.riverbankcomputing.com/static/Docs/PyQt5/installation.html
  python3.8 configure.py \
   --assume-shared \
   --confirm-license \
   --qsci-api --qsci-api-destdir=%{_qt5_datadir}/qsci \
   --sip='/usr/bin/sip' \
   --no-designer-plugin \
   --no-qml-plugin \
   --qmake=%{_qt5_qmake} \
   --dbus=%{_includedir}/dbus-1.0/ \
   QMAKE_CFLAGS_RELEASE="%{optflags}" \
   QMAKE_CXXFLAGS_RELEASE="%{optflags} `pkg-config --cflags dbus-python`" \
   QMAKE_LFLAGS_RELEASE="%{?__global_ldflags}"
    
%make_build V=0


%install


# Python 3 build:

# INSTALL_ROOT is needed for the QtDesigner module, the other Makefiles use DESTDIR
%make_install INSTALL_ROOT=%{buildroot} -j1 V=0

  # Fix conflicts with python-pyqt5
  mv %{buildroot}/usr/bin/{,python3.8-}pyuic5
  mv %{buildroot}/usr/bin/{,python3.8-}pylupdate5
  mv %{buildroot}/usr/bin/{,python3.8-}pyrcc5


# ensure .so modules are executable for proper -debuginfo extraction
find %{buildroot} -type f -name '*.so' | xargs chmod a+rx


%files
%{_bindir}/python3.8-pylupdate5
%{_bindir}/python3.8-pyrcc5
%{_bindir}/python3.8-pyuic5
%{_libdir}/python3.8/site-packages/PyQt5-5.14.2.dist-info/
%{_libdir}/python3.8/site-packages/PyQt5/
%{_libdir}/python3.8/site-packages/dbus/mainloop/pyqt5.so     
%exclude /usr/share/qt5/qsci/api/python/PyQt5.api
%exclude /usr/share/sip/



%changelog
