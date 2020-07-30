#
# Conditional build:
%bcond_without	python2		# Python 2 module
%bcond_without	python3		# Python 3 module

Summary:	Library to talk to FTDI's chips including the popular bitbang mode
Summary(pl.UTF-8):	Biblioteka do komunikacji z układami FTDI włącznie z trybem bitbang
Name:		libftdi1
Version:	1.5
Release:	2
License:	LGPL v2
Group:		Libraries
#Source0Download: https://www.intra2net.com/en/developer/libftdi/download.php
Source0:	https://www.intra2net.com/en/developer/libftdi/download/%{name}-%{version}.tar.bz2
# Source0-md5:	f515d7d69170a9afc8b273e8f1466a80
Patch0:		%{name}-cmake.patch
URL:		https://www.intra2net.com/en/developer/libftdi/
BuildRequires:	boost-devel >= 1.33
BuildRequires:	cmake >= 2.6
BuildRequires:	doxygen
BuildRequires:	libconfuse-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libusb-devel >= 1.0.0
BuildRequires:	pkgconfig
%{?with_python2:BuildRequires:	python-devel >= 1:2.6}
%{?with_python3:BuildRequires:	python3-devel >= 1:3.3}
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	swig-python
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libftdi1 is a library (using libusb) to talk to FTDI's UART/FIFO chips
including the popular bitbang mode. The following chips are supported:
- FT4232H / FT2232H
- FT232R / FT245R
- FT2232L / FT2232D / FT2232C
- FT232BM / FT245BM (and the BL/BQ variants)
- FT8U232AM / FT8U245AM

%description -l pl.UTF-8
libftdi1 to korzystająca z libusb biblioteka, służąca do komunikacji z
układami FTDI typu UART/FIFO, włącznie z popularnym trybem bitbang.
Obsługiwane są układy:
- FT4232H / FT2232H
- FT232R / FT245R
- FT2232L / FT2232D / FT2232C
- FT232BM / FT245BM (wraz z wariantami BL/BQ)
- FT8U232AM / FT8U245AM

%package devel
Summary:	Header files for libftdi1 library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libftdi1
License:	LGPL v2
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libusb-devel >= 1.0.0

%description devel
Header files for libftdi1 library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libftdi1.

%package static
Summary:	Static libftdi1 library
Summary(pl.UTF-8):	Statyczna biblioteka libftdi1
License:	LGPL v2
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libftdi1 library.

%description static -l pl.UTF-8
Statyczna biblioteka libftdi1.

%package c++
Summary:	C++ wrapper for libftdi1
Summary(pl.UTF-8):	Interfejs C++ do libftdi1
License:	GPL v2 with linking exception
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description c++
libftdipp1 - C++ wrapper for libftdi1.

%description c++ -l pl.UTF-8
libftdipp1 - intefejs C++ do libftdi1.

%package c++-devel
Summary:	Header file for libftdipp1 library
Summary(pl.UTF-8):	Plik nagłówkowy biblioteki libftdipp1
License:	GPL v2 with linking exception
Group:		Development/Libraries
Requires:	%{name}-c++ = %{version}-%{release}
Requires:	%{name}-devel = %{version}-%{release}
Requires:	boost-devel >= 1.33
Requires:	libstdc++-devel

%description c++-devel
Header file for libftdipp1 library.

%description c++-devel -l pl.UTF-8
Plik nagłówkowy biblioteki libftdipp1.

%package c++-static
Summary:	Static libftdipp1 library
Summary(pl.UTF-8):	Statyczna biblioteka libftdipp1
License:	GPL v2 with linking exception
Group:		Development/Libraries
Requires:	%{name}-c++-devel = %{version}-%{release}

%description c++-static
Static libftdipp1 library.

%description c++-static -l pl.UTF-8
Statyczna biblioteka libftdipp1.

%package -n python-libftdi1
Summary:	Python 2 binding for libftdi1
Summary(pl.UTF-8):	Wiązanie Pythona 2 do libftdi1
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python-libftdi1
Python 2 binding for libftdi1.

%description -n python-libftdi1 -l pl.UTF-8
Wiązanie Pythona 2 do libftdi1.

%package -n python3-libftdi1
Summary:	Python 3 binding for libftdi1
Summary(pl.UTF-8):	Wiązanie Pythona 3 do libftdi1
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python3-libftdi1
Python 3 binding for libftdi1.

%description -n python3-libftdi1 -l pl.UTF-8
Wiązanie Pythona 3 do libftdi1.

%prep
%setup -q
%patch0 -p1

%build
install -d build-doc
cd build-doc
%cmake .. \
	-DDOCUMENTATION:BOOL=ON \
	-DEXAMPLES:BOOL=OFF \
	-DPYTHON_BINDINGS:BOOL=OFF
%{__make} docs
cd ..

%if %{with python2}
install -d build-py2
cd build-py2
%cmake .. \
	-DDOCUMENTATION:BOOL=OFF \
	-DEXAMPLES:BOOL=OFF \
	-DFTDIPP:BOOL=ON \
	-DPYTHON_BINDINGS:BOOL=ON \
	-DPYTHON_EXECUTABLE=%{__python}
%{__make}
cd ..
%endif

%if %{with python3}
install -d build-py3
cd build-py3
%cmake .. \
	-DDOCUMENTATION:BOOL=OFF \
	-DEXAMPLES:BOOL=OFF \
	-DPYTHON_BINDINGS:BOOL=ON \
	-DPYTHON_EXECUTABLE=%{__python3}
%{__make}
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python3}
%{__make} -C build-py3 install \
	DESTDIR="$RPM_BUILD_ROOT"
%py3_comp $RPM_BUILD_ROOT%{py3_sitedir}
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitedir}
%endif

%if %{with python2}
%{__make} -C build-py2 install \
	DESTDIR="$RPM_BUILD_ROOT"
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean
%endif

# packaged as %doc
%{__rm} $RPM_BUILD_ROOT%{_docdir}/example.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	c++ -p /sbin/ldconfig
%postun	c++ -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog LICENSE README build-doc/doc/html ftdi_eeprom/example.conf
%attr(755,root,root) %{_libdir}/libftdi1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libftdi1.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ftdi_eeprom
%attr(755,root,root) %{_bindir}/libftdi1-config
%attr(755,root,root) %{_libdir}/libftdi1.so
%{_includedir}/libftdi1
%{_pkgconfigdir}/libftdi1.pc
%dir %{_libdir}/cmake/libftdi1
%{_libdir}/cmake/libftdi1/*.cmake
%dir %{_datadir}/libftdi
%dir %{_datadir}/libftdi/examples
%{_datadir}/libftdi/examples/*.py

%files static
%defattr(644,root,root,755)
%{_libdir}/libftdi1.a

%files c++
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libftdipp1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libftdipp1.so.3

%files c++-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libftdipp1.so
%{_includedir}/libftdipp1
%{_pkgconfigdir}/libftdipp1.pc

%files c++-static
%defattr(644,root,root,755)
%{_libdir}/libftdipp1.a

%if %{with python2}
%files -n python-libftdi1
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/_ftdi1.so
%{py_sitedir}/ftdi1.py[co]
%endif

%if %{with python3}
%files -n python3-libftdi1
%defattr(644,root,root,755)
%attr(755,root,root) %{py3_sitedir}/_ftdi1.so
%{py3_sitedir}/ftdi1.py
%{py3_sitedir}/__pycache__/ftdi1.cpython-*.py[co]
%endif
