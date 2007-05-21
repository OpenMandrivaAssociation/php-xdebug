%define snap 20070517

%define modname xdebug
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A29_%{modname}.ini

Summary:	Provides functions for function traces and profiling for PHP5
Name:		php-%{modname}
Version:	2.0.0
Release:	%mkrel 0.%{snap}.0
Group:		Development/PHP
License:	BSD-like
URL:		http://xdebug.org/
#Source0:	http://www.xdebug.org/files/%{modname}-%{version}.tar.bz2
Source0:	%{modname}-%{version}-%{snap}.tar.bz2
Source1:	%{modname}.ini
Source2:	xdebug-docs.tar.bz2
Requires:	gdb
BuildRequires:	php-devel >= 3:5.2.0
#BuildRequires:	edit-devel
#BuildRequires:	termcap-devel
Provides:	php5-xdebug
Obsoletes:	php5-xdebug
Conflicts:	php-apc php-dbg
Epoch:		2
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
The Xdebug extension helps you debugging your script by providing a lot of
valuable debug information.  The debug information that Xdebug can provide
includes the following: 

* stack and function traces in error messages with: 
  o full parameter display for user defined functions
  o function name, file name and line indications
  o support for member functions
* memory allocation
* protection for infinite recursions

Xdebug also provides: 

* profiling information for PHP scripts
* script execution analysis
* capabilities to debug your scripts interactively with a debug client

%prep

%setup -q -n %{modname} -a2
#[ "../package.xml" != "/" ] && mv ../package.xml .

cp %{SOURCE1} %{inifile}

# lib64 fix
perl -pi -e "s|/usr/lib|%{_libdir}|g" %{inifile}

%build

phpize
%configure2_5x \
    --enable-%{modname}=shared,%{_prefix}

%make
mv modules/*.so .

# make the debugclient
pushd debugclient
#sh ./buildconf
#    %%configure2_5x
#	--with-libedit
#    %%make

#  the autostuff is borked...
touch config.h
gcc %{optflags} -o debugclient main.c usefulstuff.c  -lnsl

popd

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d
install -d %{buildroot}%{_bindir}

install -m0644 %{inifile} %{buildroot}%{_sysconfdir}/php.d/%{inifile}
install -m0755 %{soname} %{buildroot}%{_libdir}/php/extensions/
install -m0755 debugclient/debugclient %{buildroot}%{_bindir}/

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc CREDITS Changelog LICENSE NEWS README xdebug-docs/*
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_bindir}/debugclient
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}
