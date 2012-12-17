%define		rname	binutils

Summary:	GNU Binary Utility Development Utilities
Name:		cross_avr_binutils
Version:	2.23.1
Release:	1
License:	GPL
Group:		Development/Tools
#Source0:	http://www.kernel.org/pub/linux/devel/binutils/binutils-%{version}.tar.bz2
Source0:	http://ftp.gnu.org/gnu/binutils/binutils-%{version}.tar.bz2
# Source0-md5:	33adb18c3048d057ac58d07a3f1adb38
Patch0:		binutils-avr.patch
URL:		http://sources.redhat.com/binutils/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gcc
BuildRequires:	perl-tools-pod
BuildRequires:	texinfo
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		target		avr
%define		arch		%{_prefix}/%{target}
%define		_noautochrpath	.*
%define		debug_package	%{nil}

%description
A set of programs to assemble and manipulate binary and object files.

%prep
%setup -qn %{rname}-%{version}
%patch0 -p0

%build
install -d obj-%{target}
cd obj-%{target}

CFLAGS="-O2"			\
LDFLAGS="%{rpmldflags}"		\
../configure			\
	--build=%{_build}	\
	--host=%{_host}		\
	--target=%{target}	\
	--infodir=%{_infodir}	\
	--libdir=%{_libdir}	\
	--libexecdir=%{_libdir} \
	--mandir=%{_mandir}	\
	--prefix=%{_prefix}	\
	--disable-debug		\
	--disable-nls		\
	--disable-shared	\
	--with-lib-path=%{_libdir}	\
	--with-sysroot=%{arch}	\
	--with-tooldir=%{_prefix}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

cd obj-%{target}
%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_infodir}/standards.info*

# remove these man pages unless we cross-build for win*/netware platforms.
# however, this should be done in Makefiles.
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/{dlltool,nlmconv,windres}.1
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/%{target}-*
%attr(755,root,root) %{arch}/bin/*
%dir %{arch}
%dir %{arch}/bin
%dir %{arch}/lib
%{arch}/lib/ldscripts
%{_mandir}/man1/%{target}-*.1*

