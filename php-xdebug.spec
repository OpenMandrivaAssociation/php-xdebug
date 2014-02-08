%define modname xdebug
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A29_%{modname}.ini

Summary:	Provides functions for function traces and profiling for PHP5
Name:		php-%{modname}
Version:	2.2.1
Release:	2
Group:		Development/PHP
License:	BSD-like
URL:		http://www.xdebug.org/
Source0:	http://www.xdebug.org/files/%{modname}-%{version}.tgz
Source1:	%{modname}.ini
Patch0:		xdebug-2.2.1-fmtstr.diff
Requires:	gdb
BuildRequires:	php-devel >= 3:5.2.0
Epoch:		2

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

%setup -q -n %{modname}-%{version}
[ "../package*.xml" != "/" ] && mv ../package*.xml .
%patch0 -p0

cp %{SOURCE1} %{inifile}

# lib64 fix
perl -pi -e "s|/usr/lib|%{_libdir}|g" %{inifile}

%build
%serverbuild

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
gcc $CFLAGS %{ldflags} -o debugclient main.c usefulstuff.c -lnsl

popd

%install

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d
install -d %{buildroot}%{_bindir}

install -m0644 %{inifile} %{buildroot}%{_sysconfdir}/php.d/%{inifile}
install -m0755 %{soname} %{buildroot}%{_libdir}/php/extensions/
install -m0755 debugclient/debugclient %{buildroot}%{_bindir}/

%post
/bin/systemctl daemon-reload >/dev/null 2>&1 || :

%postun
if [ "$1" = "0" ]; then
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%files 
%doc CREDITS LICENSE NEWS README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_bindir}/debugclient
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}


%changelog
* Mon Jul 16 2012 Oden Eriksson <oeriksson@mandriva.com> 2:2.2.1-1mdv2012.0
+ Revision: 809921
- fix build
- 2.2.1

* Wed May 02 2012 Oden Eriksson <oeriksson@mandriva.com> 2:2.2.0-0.0.RC2.1
+ Revision: 794979
- grr...
- 2.2.0RC2
- rebuild for php-5.4.x

* Thu Mar 22 2012 Oden Eriksson <oeriksson@mandriva.com> 2:2.1.4-1
+ Revision: 786010
- 2.1.4

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 2:2.1.2-4
+ Revision: 761128
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 2:2.1.2-3
+ Revision: 696380
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 2:2.1.2-2
+ Revision: 695325
- rebuilt for php-5.3.7

* Mon Aug 08 2011 Oden Eriksson <oeriksson@mandriva.com> 2:2.1.2-1
+ Revision: 693640
- 2.1.2

* Thu May 05 2011 Oden Eriksson <oeriksson@mandriva.com> 2:2.1.1-2
+ Revision: 667768
- mass rebuild

* Mon Apr 04 2011 Oden Eriksson <oeriksson@mandriva.com> 2:2.1.1-1
+ Revision: 650139
- 2.1.1

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 2:2.1.0-6
+ Revision: 646564
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 2:2.1.0-5mdv2011.0
+ Revision: 629756
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 2:2.1.0-4mdv2011.0
+ Revision: 628058
- ensure it's built without automake1.7

* Tue Nov 23 2010 Oden Eriksson <oeriksson@mandriva.com> 2:2.1.0-3mdv2011.0
+ Revision: 600190
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 2:2.1.0-2mdv2011.0
+ Revision: 588729
- rebuild

* Tue Jul 13 2010 Oden Eriksson <oeriksson@mandriva.com> 2:2.1.0-1mdv2011.0
+ Revision: 552149
- 2.1.0

* Wed Apr 07 2010 Oden Eriksson <oeriksson@mandriva.com> 2:2.1.0-0.1.RC1.1mdv2010.1
+ Revision: 532603
- fix release
- 2.1.0RC1

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 2:2.1.0-0.0.beta3.2mdv2010.1
+ Revision: 514717
- rebuilt for php-5.3.2

* Mon Mar 01 2010 Oden Eriksson <oeriksson@mandriva.com> 2:2.1.0-0.0.beta3.1mdv2010.1
+ Revision: 512920
- 2.1.0beta3

* Sun Feb 21 2010 Oden Eriksson <oeriksson@mandriva.com> 2:2.1.0-0.0.beta2.2mdv2010.1
+ Revision: 509098
- rebuild

* Tue Feb 16 2010 Oden Eriksson <oeriksson@mandriva.com> 2:2.1.0-0.0.beta2.1mdv2010.1
+ Revision: 506545
- 2.1.0beta2

* Tue Jan 05 2010 Oden Eriksson <oeriksson@mandriva.com> 2:2.1.0-0.0.beta1.1mdv2010.1
+ Revision: 486480
- 2.1.0beta1

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 2:2.0.5-6mdv2010.1
+ Revision: 485271
- rebuilt for php-5.3.2RC1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 2:2.0.5-5mdv2010.1
+ Revision: 468098
- rebuilt against php-5.3.1

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 2:2.0.5-4mdv2010.0
+ Revision: 451228
- rebuild

* Sun Jul 19 2009 Raphaël Gertz <rapsys@mandriva.org> 2:2.0.5-3mdv2010.0
+ Revision: 397291
- Rebuild

* Thu Jul 16 2009 Raphaël Gertz <rapsys@mandriva.org> 2:2.0.5-2mdv2010.0
+ Revision: 396628
- New xdebug configuration file
  Rebuild

* Tue Jul 14 2009 Oden Eriksson <oeriksson@mandriva.com> 2:2.0.5-1mdv2010.0
+ Revision: 395913
- 2.0.5

* Mon Jun 29 2009 Oden Eriksson <oeriksson@mandriva.com> 2:2.0.5-0.20090611.2mdv2010.0
+ Revision: 390443
- rebuild

* Mon Jun 15 2009 Oden Eriksson <oeriksson@mandriva.com> 2:2.0.5-0.20090611.1mdv2010.0
+ Revision: 385999
- use latest cvs snap, should work with php-5.3.x

* Wed May 13 2009 Oden Eriksson <oeriksson@mandriva.com> 2:2.0.4-5mdv2010.0
+ Revision: 375369
- rebuilt against php-5.3.0RC2

* Sun Mar 01 2009 Oden Eriksson <oeriksson@mandriva.com> 2:2.0.4-4mdv2009.1
+ Revision: 346706
- rebuilt for php-5.2.9

* Tue Feb 17 2009 Oden Eriksson <oeriksson@mandriva.com> 2:2.0.4-3mdv2009.1
+ Revision: 341519
- rebuilt against php-5.2.9RC2

* Thu Jan 01 2009 Oden Eriksson <oeriksson@mandriva.com> 2:2.0.4-2mdv2009.1
+ Revision: 321968
- rebuild

* Wed Dec 31 2008 Oden Eriksson <oeriksson@mandriva.com> 2:2.0.4-1mdv2009.1
+ Revision: 321649
- 2.0.4
- update the xdebug.ini file a bit
- use %%ldflags (if supported)

* Fri Dec 05 2008 Oden Eriksson <oeriksson@mandriva.com> 2:2.0.3-5mdv2009.1
+ Revision: 310229
- rebuilt against php-5.2.7

* Fri Sep 12 2008 Oden Eriksson <oeriksson@mandriva.com> 2:2.0.3-4mdv2009.0
+ Revision: 284187
- fix #34206 (Invalid dependency between php-apc and php-xdebug)

* Tue Jul 15 2008 Oden Eriksson <oeriksson@mandriva.com> 2:2.0.3-3mdv2009.0
+ Revision: 235886
- rebuild

* Fri May 02 2008 Oden Eriksson <oeriksson@mandriva.com> 2:2.0.3-2mdv2009.0
+ Revision: 200122
- rebuilt against php-5.2.6

* Thu Apr 10 2008 Oden Eriksson <oeriksson@mandriva.com> 2:2.0.3-1mdv2009.0
+ Revision: 192544
- 2.0.3

* Mon Feb 04 2008 Oden Eriksson <oeriksson@mandriva.com> 2:2.0.2-2mdv2008.1
+ Revision: 161932
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Mon Nov 12 2007 Oden Eriksson <oeriksson@mandriva.com> 2:2.0.2-1mdv2008.1
+ Revision: 108121
- 2.0.2

* Sun Nov 11 2007 Oden Eriksson <oeriksson@mandriva.com> 2:2.0.1-2mdv2008.1
+ Revision: 107582
- restart apache if needed

* Sun Oct 21 2007 Oden Eriksson <oeriksson@mandriva.com> 2:2.0.1-1mdv2008.1
+ Revision: 100929
- 2.0.1

* Sat Sep 01 2007 Oden Eriksson <oeriksson@mandriva.com> 2:2.0.0-2mdv2008.0
+ Revision: 77468
- rebuilt against php-5.2.4

* Thu Jul 19 2007 Oden Eriksson <oeriksson@mandriva.com> 2:2.0.0-1mdv2008.0
+ Revision: 53458
- 2.0.0
- use the new %%serverbuild macro
- remove old html docs

* Thu Jun 14 2007 Oden Eriksson <oeriksson@mandriva.com> 2:2.0.0-0.20070517.1mdv2008.0
+ Revision: 39394
- use distro conditional -fstack-protector

* Mon May 21 2007 Oden Eriksson <oeriksson@mandriva.com> 2:2.0.0-0.20070517.0mdv2008.0
+ Revision: 29171
- new snap (20070517)

* Wed May 02 2007 Oden Eriksson <oeriksson@mandriva.com> 2:2.0.0-0.20070428.0mdv2008.0
+ Revision: 20521
- new snap (20070428)

