# Conditional build:
%bcond_with	py3	# using python3 scripting

Summary:	Library to talk to FTDI's chips including the popular bitbang mode
Summary(pl.UTF-8):	Biblioteka do komunikacji z układami FTDI włącznie z trybem bitbang
Name:		libftdi1
Version:	1.2
Release:	1
License:	LGPL v2
Group:		Libraries
Source0:	http://www.intra2net.com/en/developer/libftdi1/download/%{name}-%{version}.tar.bz2
# Source0-md5:	89dff802d89c4c0d55d8b4665fd52d0b
URL:		http://www.intra2net.com/en/developer/libftdi1/
BuildRequires:	boost-devel >= 1.33
BuildRequires:	doxygen
BuildRequires:	libconfuse-devel
BuildRequires:	libusb-devel >= 1.0.0
BuildRequires:	pkgconfig
%if %{with py3}
BuildRequires:	python3-devel >= 3.3
%else
BuildRequires:	python-devel >= 2.6
%endif
BuildRequires:	rpmbuild(macros) >= 1.600
BuildRequires:	swig-python
BuildRequires:	swig-python >= 2.6
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
Requires:	libusb-compat-devel >= 0.1.0

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
License:	LGPL
Group:		Development/Libraries
Requires:	%{name}-c++-devel = %{version}-%{release}

%description c++-static
Static libftdipp1 library.

%description c++-static -l pl.UTF-8
Statyczna biblioteka libftdipp1.

%package -n python-libftdi1
Summary:	Python binding for libftdi1
Summary(pl.UTF-8):	Wiązanie Pythona do libftdi1
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python-libftdi1
Python binding for libftdi1.

%description -n python-libftdi1 -l pl.UTF-8
Wiązanie Pythona do libftdi1.

%prep
%setup -q
%if %{with py3}
sed -i -r "s#(find_package\s+\(\s+PythonLibs)(\s+\))#\1 3.3\2#g"  \
%else
sed -i -r "s#(find_package\s+\(\s+PythonLibs)(\s+\))#\1 2.6\2#g"  \
%endif
	python/CMakeLists.txt

%build
install -d build
cd build
%cmake \
%if %{with py3}
	-DPYTHON_EXECUTABLE=%{__python}3 \
%else
	-DPYTHON_EXECUTABLE=%{__python}2 \
%endif
	-DPYTHON_SITE_PACKAGE_PATH=%{py_sitescriptdir} \
	-DEXAMPLES=OFF \
	..
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__rm} -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR="$RPM_BUILD_ROOT"
##%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
##%py__postclean#

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	c++ -p /sbin/ldconfig
%postun	c++ -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog LICENSE README build/doc/html build/doc/man
%attr(755,root,root) %{_libdir}/libftdi1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libftdi1.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ftdi_eeprom
%attr(755,root,root) %{_bindir}/libftdi1-config
%attr(755,root,root) %{_libdir}/libftdi1.so
%dir %{_includedir}/libftdi1
%{_includedir}/libftdi1/ftdi.h
%{_pkgconfigdir}/libftdi1.pc
%dir %{_libdir}/cmake/libftdi1/
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
%attr(755,root,root) %ghost %{_libdir}/libftdipp1.so.2

%files c++-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libftdipp1.so
%{_includedir}/libftdi1/ftdi.hpp
%{_pkgconfigdir}/libftdipp1.pc

%files c++-static
%defattr(644,root,root,755)
%{_libdir}/libftdipp1.a

%files -n python-libftdi1
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/_ftdi1.so
%{py_sitedir}/ftdi1.py*
