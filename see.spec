#
# Conditional build:
%bcond_without	static_libs	# don't build static library
#
Summary:	Simple ECMAScript Engine
Summary(pl.UTF-8):	Prosty "silnik" ECMAScriptu
Name:		see
Version:	3.0.1376
Release:	1
License:	BSD-like
Group:		Libraries
Source0:	http://www.adaptive-enterprises.com.au/~d/software/see/%{name}-%{version}.tar.gz
# Source0-md5:	b67a8ff3e5e987328540fd4c01323700
Patch0:		%{name}-no_static.patch
URL:		http://www.adaptive-enterprises.com.au/~d/software/see
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	libltdl-devel
BuildRequires:	gc-devel
BuildRequires:	perl-base
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SEE is a library that provides an ECMAScript (JavaScript)
run-time environment.

%description -l pl.UTF-8
SEE jest biblioteką udostępniającą środowisko uruchomieniowe
ECMAScriptu (JavaScriptu).

%package devel
Summary:	Header files for SEE library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki SEE
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gc-devel

%description devel
Header files for SEE library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki SEE.

%package static
Summary:	Static SEE library
Summary(pl.UTF-8):	Statyczna biblioteka SEE
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static SEE library.

%description static -l pl.UTF-8
Statyczna biblioteka SEE.

%prep
%setup -q
%patch -P0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%{__autoheader}
%configure \
	CPPFLAGS="$CPPFLAGS -I/usr/include/gc" \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/see-shell
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%doc doc/USAGE.html
%attr(755,root,root) %{_bindir}/libsee-config
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/see

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
%endif
