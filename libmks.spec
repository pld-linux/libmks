#
# Conditional build:
%bcond_without	apidocs		# API documentation
#
Summary:	Library for Mouse, Keyboard and Screen to QEMU
Summary(pl.UTF-8):	Biblioteka myszy, klawiatury i ekranu dla QEMU
Name:		libmks
Version:	0.1.5
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	https://download.gnome.org/sources/libmks/0.1/%{name}-%{version}.tar.xz
# Source0-md5:	ea5da476c3867832e971617964dcab8b
URL:		https://gitlab.gnome.org/GNOME/libmks
%{?with_apidocs:BuildRequires:	gi-docgen}
BuildRequires:	glib2-devel >= 1:2.75.0
BuildRequires:	gtk4-devel >= 4.11
BuildRequires:	libepoxy-devel
BuildRequires:	meson >= 0.62.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.029
BuildRequires:	tar >= 1:1.22
BuildRequires:	vala >= 2:0.44
BuildRequires:	xz
Requires:	glib2 >= 1:2.75.0
Requires:	gtk4 >= 4.11
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This library provides a "Mouse, Keyboard, and Screen" to QEMU using
the D-Bus device support in QEMU and GTK 4.

%description -l pl.UTF-8
Ta biblioteka udostępnia mysz, klawiaturę i ekran (Mouse, Keyboard,
Screen) dla QEMU przy użyciu urządzenia D-Bus w QEMU i GTK 4.

%package devel
Summary:	Header files for libmks library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libmks
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.75.0
Requires:	gtk4-devel >= 4.11

%description devel
Header files for libmks library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libmks.

%package -n vala-libmks
Summary:	Vala API for libmks library
Summary(pl.UTF-8):	API języka Vala do biblioteki libmks
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
# with gtk4 binding
Requires:	vala >= 2:0.44
BuildArch:	noarch

%description -n vala-libmks
Vala API for libmks library.

%description -n vala-libmks -l pl.UTF-8
API języka Vala do biblioteki libmks.

%package apidocs
Summary:	API documentation for libmks library
Summary(pl.UTF-8):	Dokumentacja API biblioteki libmks
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for libmks library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libmks.

%prep
%setup -q

%build
%meson build \
	%{?with_apidocs:-Ddocs=true} \
	-Dinstall-tools=true \
	-Dintrospection=enabled

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%if %{with apidocs}
install -d $RPM_BUILD_ROOT%{_gidocdir}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/libmks1 $RPM_BUILD_ROOT%{_gidocdir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc NEWS README.md
%attr(755,root,root) %{_bindir}/mks
%attr(755,root,root) %{_bindir}/mks-connect
%attr(755,root,root) %{_libdir}/libmks-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmks-1.so.0
%{_libdir}/girepository-1.0/Mks-1.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmks-1.so
%{_includedir}/libmks-1
%{_datadir}/gir-1.0/Mks-1.gir
%{_pkgconfigdir}/libmks-1.pc

%files -n vala-libmks
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/libmks-1.deps
%{_datadir}/vala/vapi/libmks-1.vapi

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gidocdir}/libmks1
%endif
