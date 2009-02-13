# Do not change this spec directly but in the svn
# $Id: rpm.spec 134789 2007-03-27 15:13:43Z nanardon $

%define lib64arches	x86_64 ppc64 sparc64

%ifarch %lib64arches
    %define _lib lib64
%else
    %define _lib lib
%endif

%define _prefix /usr
%define _libdir %_prefix/%_lib
%define _bindir %_prefix/bin
%define _sysconfdir /etc
%define _datadir /usr/share
%define _defaultdocdir %_datadir/doc
%define _localstatedir /var
%define _infodir %_datadir/info

# Define directory which holds rpm config files, and some binaries actually
# NOTE: it remains */lib even on lib64 platforms as only one version
#       of rpm is supported anyway, per architecture
%define rpmdir %{_prefix}/lib/rpm

%if %{?mklibname:0}%{?!mklibname:1}
%define mklibname(ds)  %{_lib}%{1}%{?2:%{2}}%{?3:_%{3}}%{-s:-static}%{-d:-devel}
%endif

%if %{?distsuffix:0}%{?!distsuffix:1}
%define distsuffix mdv
%endif

%if %{?mkrel:0}%{?!mkrel:1}
%define mkrel(c:) %{-c: 0.%{-c*}.}%{1}%{?distsuffix:%distsuffix}%{?!distsuffix:mdv}%{?mandriva_release:%mandriva_release}%{?subrel:.%subrel}
%endif

%if %{?pyver:0}%{?!pyver:1}
%define pyver %(python -V 2>&1 | cut -f2 -d" " | cut -f1,2 -d".")
%endif

%if %_vendor == Mandriva
%define __find_requires %{rpmdir}/mandriva/find-requires %{?buildroot:%{buildroot}} %{?_target_cpu:%{_target_cpu}}
%define __find_provides %{rpmdir}/mandriva/find-provides
%endif

%define rpmversion	4.6.0
%define srcver		%rpmversion
%define libver		4.6
%define release			    %manbo_mkrel 1
%define librpmname   %mklibname rpm  %{libver}
%define librpmnamedevel   %mklibname -d rpm

%define buildpython 1

%if %_vendor == Mandriva
%if %{mdkversion} >= 200710
# MDV 2007.1 builds with --hash-style=gnu by default
%define rpmsetup_version 1.34
%endif
%endif

%define builddebug 0
%{?_with_debug:%define builddebug 1}

%{?_with_python:%define buildpython 1}
%{?_without_python:%define buildpython 0}

Summary:	The RPM package management system
Name:		rpm
Epoch:		1
Version:	%{rpmversion}
Release:	%{release}
Group:		System/Configuration/Packaging

Source:		http://www.rpm.org/releases/rpm-%{libver}.x/rpm-%{srcver}.tar.bz2

# Add some undocumented feature to gendiff
Patch17:	rpm-4.4.2.2-gendiff-improved.patch

# if %post of foo-2 fails,
# or if %preun of foo-1 fails,
# or if %postun of foo-1 fails,
# => foo-1 is not removed, so we end up with both packages in rpmdb
# this patch makes rpm ignore the error in those cases
# failing %pre must still make the rpm install fail (#23677)
#
# (nb: the exit code for pretrans/posttrans & trigger/triggerun/triggerpostun
#       scripts is ignored with or without this patch)
Patch22:        rpm-4.6.0-rc1-non-pre-scripts-dont-fail.patch

# (fredl) add loging facilities through syslog
Patch31:	rpm-4.6.0-rc1-syslog.patch

# part of Backport from 4.2.1 provides becoming obsoletes bug (fpons)
# (is it still needed?)
Patch49:	rpm-4.6.0-rc1-provides-obsoleted.patch

# - force /usr/lib/rpm/manbo/rpmrc instead of /usr/lib/rpm/<vendor>/rpmrc
# - read /usr/lib/rpm/manbo/rpmpopt (not only /usr/lib/rpm/rpmpopt)
Patch64:    rpm-4.6.0-rc2-manbo-rpmrc-rpmpopt.patch

# In original rpm, -bb --short-circuit does not work and run all stage
# From popular request, we allow to do this
# http://qa.mandriva.com/show_bug.cgi?id=15896
Patch70:	rpm-4.6.0-rc1-bb-shortcircuit.patch

# http://www.redhat.com/archives/rpm-list/2005-April/msg00131.html
# http://www.redhat.com/archives/rpm-list/2005-April/msg00132.html
# is this useful? "at least erasure ordering is just as non-existent as it was in 4.4.x" says Panu
Patch71:    rpm-4.6.0-ordererase.patch

# don't conflict for doc files
# (to be able to install lib*-devel together with lib64*-devel even if they have conflicting manpages)
Patch83: rpm-4.6.0-no-doc-conflicts.patch

# Fix http://qa.mandriva.com/show_bug.cgi?id=19392
# (is this working??)
Patch84: rpm-4.4.2.2-rpmqv-ghost.patch

# Fix diff issue when buildroot contains some "//"
Patch111: rpm-check-file-trim-double-slash-in-buildroot.patch

# [Dec 2008] macrofiles from rpmrc does not overrides MACROFILES anymore
Patch114: rpm-4.6.0-rc1-read-macros_d-dot-macros.patch

# remove unused skipDir functionality that conflicts with patch124 below
Patch1124: rpm-4.6.0-rc1-revert-unused-skipDir-functionality.patch

# [pixel] without this patch, "rpm -e" or "rpm -U" will need to stat(2) every dirnames of
# files from the package (eg COPYING) in the db. This is quite costly when not in cache 
# (eg on a test here: >300 stats, and so 3 seconds after a "echo 3 > /proc/sys/vm/drop_caches")
# this breaks urpmi test case test_rpm_i_fail('gd') in superuser--file-conflicts.t,
# but this is bad design anyway
Patch124: rpm-4.6.0-rc1-speedup-by-not-checking-same-files-with-different-paths-through-symlink.patch

# [from SuSE] handle "Suggests" via RPMTAG_SUGGESTSNAME
Patch133: rpm-4.6.0-rc1-weakdeps.patch

# (from Turbolinux) remove a wrong check in case %_topdir is /RPM (ie when it is short)
Patch135: rpm-4.4.2.3-rc1-fix-debugedit.patch

# convert data in the header to a specific encoding which used in the selected locale.
Patch137: rpm-4.6.0-rc1-headerIconv.patch

Patch140: rpm-russian-translation.patch

# Mandriva does not need the (broken) ldconfig hack since it uses filetriggers
Patch141: rpm-4.6.0-rc1-drop-skipping-ldconfig-hack.patch

# without this patch, "#%define foo bar" is surprisingly equivalent to "%define foo bar"
# with this patch, "#%define foo bar" is a fatal error
Patch145: rpm-forbid-badly-commented-define-in-spec.patch

# cf http://wiki.mandriva.com/en/Rpm_filetriggers
Patch146: rpm-4.6.0-rc1-filetriggers.patch

# add two fatal errors (during package build)
Patch147: rpm-rpmbuild-check-useless-tags-in-non-existant-binary-packages.patch

# (nb: see the patch for more info about this issue)
Patch151: rpm-4.6.0-rc1-protect-against-non-robust-futex.patch

Patch152: rpm-4.6.0-rc1-fix-nss-detection.patch

Patch157: introduce-_after_setup-which-is-called-after-setup.patch
Patch158: introduce-_patch-and-allow-easy-override-when-the-p.patch
Patch159: introduce-apply_patches-and-lua-var-patches_num.patch

#Patch1001: rpm-4.6.0-rc1-new-liblzma.patch

# default behaviour in rpm-jbj >= 4.4.6
Patch1005: rpm-allow-conflicting-ghost-files.patch

# (nb: see the patch for more info about this issue)
Patch1006: rpm-4.6.0-rc1-compat-PayloadIsLzma.patch

Patch1007: rpm-4.6.0-rc3-xz-support.patch

# Prevents $DOCDIR from being wiped out when using %%doc <fileinbuilddir>,
# as this breaks stuff that installs files to $DOCDIR during %%install
Patch1008: rpm-4.6.0-rc3-no_rm_-rf_DOCDIR.patch

# Turbolinux patches
Patch2000: rpm-4.6.0-rc1-serial-tag.patch
# re-enable "copyright" tag (Kiichiro, 2005)
Patch2001: rpm-4.6.0-rc1-copyright-tag.patch
# add writeHeaderListTofile function into rpm-python (needed by "buildman" build system) (Toshihiro, 2003)
Patch2002: rpm-4.6.0-rc1-python-writeHdlist.patch
# Crusoe CPUs say that their CPU family is "5" but they have enough features for i686.
Patch2003: rpm-4.4.2.3-rc1-transmeta-crusoe-is-686.patch

# The following patch is unneeded for Mandriva, but Turbolinux has it and it can't hurt much
#
# This patch fixes the problem when the post-scripts launched by rpm-build. 
# The post-scripts launched by rpm-build works in LANG environment. If LANG is
# other locale except C, then some commands launched by post-scripts will not
# display characters which you expected.
Patch2005: rpm-4.6.0-rc1-buildlang.patch

License:	GPL
BuildRequires:	autoconf >= 2.57
BuildRequires:	zlib-devel
BuildRequires:  bzip2-devel
BuildRequires:	liblzma-devel >= 4.999.6-0.alpha.5
BuildRequires:	automake >= 1.8
BuildRequires:	elfutils-devel
BuildRequires:	sed >= 4.0.3
BuildRequires:	libbeecrypt-devel
BuildRequires:	ed, gettext-devel
BuildRequires:  libsqlite3-devel
BuildRequires:  db4.6-devel
BuildRequires:  neon-devel
BuildRequires:	popt-devel
BuildRequires:	nss-devel
BuildRequires:	magic-devel
%if %_vendor == Mandriva
BuildRequires:  rpm-mandriva-setup-build %{?rpmsetup_version:>= %{rpmsetup_version}}
%endif
BuildRequires:  readline-devel
BuildRequires:	ncurses-devel
BuildRequires:  openssl-devel >= 0.9.8
BuildRequires:  lua-devel
# Need for doc
#BuildRequires:	graphviz
BuildRequires:	tetex
%if %buildpython
BuildRequires:	python-devel
%endif

Requires:	bzip2 >= 0.9.0c-2
Requires:	lzma
Requires:	cpio
Requires:	gawk
Requires:	glibc >= 2.1.92
Requires:	mktemp
Requires:	setup >= 2.2.0-8mdk
Requires:	rpm-manbo-setup
%if %_vendor == Mandriva
Requires:	rpm-mandriva-setup >= 1.85
%endif
Requires:	update-alternatives
Requires:	%librpmname = %epoch:%version-%release
Conflicts:	patch < 2.5
Conflicts:	menu < 2.1.5-29mdk
Conflicts:	locales < 2.3.1.1
Conflicts:	man-pages-fr < 0.9.7-16mdk
Conflicts:	man-pages-pl < 0.4-9mdk
Conflicts:	perl-URPM < 1.63-3mdv2008.0
# rpm 4.6.0 dropped support for --repackage, so urpmi-recover can not work anymore:
Conflicts:	urpmi-recover
URL:            http://rpm.org/
%define         git_url        http://rpm.org/git/rpm.git
Requires(pre):		rpm-helper >= 0.8
Requires(pre):		coreutils
Requires(postun):	rpm-helper >= 0.8
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
RPM is a powerful command line driven package management system capable of
installing, uninstalling, verifying, querying, and updating software packages.
Each software package consists of an archive of files along with information
about the package like its version, a description, etc.

%package -n %librpmname
Summary: Library used by rpm
Group:		System/Libraries
Provides:   librpm = %version-%release

%description -n %librpmname
RPM is a powerful command line driven package management system capable of
installing, uninstalling, verifying, querying, and updating software packages.
This package contains common files to all applications based on rpm.

%package -n %librpmnamedevel
Summary:	Development files for applications which will manipulate RPM packages
Group:		Development/C
Requires:	rpm = %epoch:%{version}-%{release}
Provides:	librpm-devel = %version-%release
Provides:   	rpm-devel = %version-%release
Obsoletes:  	rpm-devel < 4.4.1
Obsoletes:      %{_lib}rpm4.4-devel
Obsoletes:      %{_lib}rpm4.2-devel

%description -n %librpmnamedevel
This package contains the RPM C library and header files.  These
development files will simplify the process of writing programs
which manipulate RPM packages and databases and are intended to make
it easier to create graphical package managers or any other tools
that need an intimate knowledge of RPM packages in order to function.

This package should be installed if you want to develop programs that
will manipulate RPM packages and databases.

%package build
Summary:	Scripts and executable programs used to build packages
Group:		System/Configuration/Packaging
Requires:	autoconf
Requires:	automake
Requires:	file
Requires:	gcc-c++
# We need cputoolize & amd64-* alias to x86_64-* in config.sub
Requires:	libtool-base >= 1.4.3-5mdk
Requires:	patch
Requires:	make
Requires:	tar
Requires:	unzip
Requires:	elfutils
Requires:	rpm = %epoch:%{version}-%{release}
%if %_vendor == Mandriva
Requires:	rpm-mandriva-setup-build %{?rpmsetup_version:>= %{rpmsetup_version}}
%endif

%description build
This package contains scripts and executable programs that are used to
build packages using RPM.

%if %buildpython
%package -n python-rpm
Summary:	Python bindings for apps which will manipulate RPM packages
Group:		Development/Python
Requires:	python >= %{pyver}
Requires:	rpm = %epoch:%{version}-%{release}
Obsoletes:  rpm-python < %epoch:%version-%release
Provides:   rpm-python = %version-%release

%description -n python-rpm
The rpm-python package contains a module which permits applications
written in the Python programming language to use the interface
supplied by RPM (RPM Package Manager) libraries.

This package should be installed if you want to develop Python
programs that will manipulate RPM packages and databases.
%endif

%prep
%setup -q -n %name-%srcver
%apply_patches

%build

autoreconf

%if %builddebug
RPM_OPT_FLAGS=-g
%endif
CFLAGS="$RPM_OPT_FLAGS -fPIC" CXXFLAGS="$RPM_OPT_FLAGS -fPIC" \
    %configure \
        --enable-nls \
        --enable-python \
        --enable-sqlite3 \
        --without-javaglue \
%if %builddebug
        --enable-debug \
%endif
	--with-external-db \
%if %buildpython
        --with-python=%{pyver} \
%else
        --without-python \
%endif
        --with-glob \
        --without-selinux \
        --without-apidocs 

%make

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=%buildroot install

%ifarch ppc powerpc
ln -sf ppc-mandriva-linux $RPM_BUILD_ROOT%{rpmdir}/powerpc-mandriva-linux
%endif

#mv -f $RPM_BUILD_ROOT/%{rpmdir}/rpmdiff $RPM_BUILD_ROOT/%{_bindir}

# Save list of packages through cron
mkdir -p ${RPM_BUILD_ROOT}/etc/cron.daily
install -m 755 scripts/rpm.daily ${RPM_BUILD_ROOT}/etc/cron.daily/rpm

mkdir -p ${RPM_BUILD_ROOT}/etc/logrotate.d
install -m 644 scripts/rpm.log ${RPM_BUILD_ROOT}/etc/logrotate.d/rpm

mkdir -p $RPM_BUILD_ROOT/var/lib/rpm
for dbi in \
	Basenames Conflictname Dirnames Group Installtid Name Providename \
	Provideversion Removetid Requirename Requireversion Triggername \
	Packages __db.001 __db.002 __db.003 __db.004
do
    touch $RPM_BUILD_ROOT/var/lib/rpm/$dbi
done

test -d doc-copy || mkdir doc-copy
rm -rf doc-copy/*
ln -f doc/manual/* doc-copy/
rm -f doc-copy/Makefile*

mkdir -p $RPM_BUILD_ROOT/var/spool/repackage

mkdir -p %buildroot%_sysconfdir/rpm/macros.d
cat > %buildroot%_sysconfdir/rpm/macros <<EOF
# Put your own system macros here
# usually contains 

# Set this one according your locales
# %%_install_langs

EOF

# Get rid of unpackaged files
(cd $RPM_BUILD_ROOT;
  rm -rf .%{_includedir}/beecrypt/
  rm -f  .%{_libdir}/libbeecrypt.{a,la,so*}
  rm -f  .%{_libdir}/python*/site-packages/rpmmodule.{a,la}
  rm -f  .%{rpmdir}/{Specfile.pm,cpanflute2,cpanflute,sql.prov,sql.req,tcl.req}
  rm -f  .%{rpmdir}/{config.site,cross-build,rpmdiff.cgi}
  rm -f  .%{rpmdir}/trpm
  rm -f  .%{_bindir}/rpmdiff
)

%if %_vendor == Mandriva
%{rpmdir}/%{_host_vendor}/find-lang.pl $RPM_BUILD_ROOT %{name}
%else
%find_lang %{name}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ -f /var/lib/rpm/Packages -a -f /var/lib/rpm/packages.rpm ]; then
    echo "
You have both
	/var/lib/rpm/packages.rpm	db1 format installed package headers
	/var/lib/rpm/Packages		db3 format installed package headers
Please remove (or at least rename) one of those files, and re-install.
"
    exit 1
fi

/usr/share/rpm-helper/add-user rpm $1 rpm /var/lib/rpm /bin/false

rm -rf /usr/lib/rpm/*-mandrake-*

%post
# nuke __db.00? when updating to this rpm
rm -f /var/lib/rpm/__db.00?

if [ ! -e /etc/rpm/macros -a -e /etc/rpmrc -a -f %{rpmdir}/convertrpmrc.sh ] 
then
	sh %{rpmdir}/convertrpmrc.sh 2>&1 > /dev/null
fi

if [ -f /var/lib/rpm/packages.rpm ]; then
    /bin/chown rpm.rpm /var/lib/rpm/*.rpm
elif [ ! -f /var/lib/rpm/Packages ]; then
    /bin/rpm --initdb
fi

%postun
/usr/share/rpm-helper/del-user rpm $1 rpm

%if %mdkversion < 200900
%post -n %librpmname -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %librpmname -p /sbin/ldconfig
%endif

%triggerpostun -- rpm < 1:4.4.2.3-11
if [ -f /etc/rpm/macros.cdb.rpmsave ]; then
   echo "warning: restoring /etc/rpm/macros.cdb from macros.cdb.rpmsave, please check you really need the changes"
   mv /etc/rpm/macros.cdb.rpmsave /etc/rpm/macros.cdb
fi

%define	rpmattr		%attr(0755, rpm, rpm)

%files -f %{name}.lang
%defattr(-,root,root)
%doc GROUPS CHANGES doc/manual/[a-z]*
%attr(0755,rpm,rpm) /bin/rpm
%attr(0755, rpm, rpm) %{_bindir}/rpm2cpio
%attr(0755, rpm, rpm) %{_bindir}/gendiff
%attr(0755, rpm, rpm) %{_bindir}/rpmdb
%attr(0755, rpm, rpm) %{_bindir}/rpmgraph
%attr(0755, rpm, rpm) %{_bindir}/rpmsign
%attr(0755, rpm, rpm) %{_bindir}/rpmquery
%attr(0755, rpm, rpm) %{_bindir}/rpmverify

%dir %{_localstatedir}/spool/repackage
%dir %{rpmdir}
%dir /etc/rpm
%config(noreplace) /etc/rpm/macros
%dir /etc/rpm/macros.d
%attr(0755, rpm, rpm) %{rpmdir}/config.guess
%attr(0755, rpm, rpm) %{rpmdir}/config.sub
#%attr(0755, rpm, rpm) %{rpmdir}/convertrpmrc.sh
%attr(0755, rpm, rpm) %{rpmdir}/rpmdb_*
%attr(0644, rpm, rpm) %{rpmdir}/macros
%attr(0755, rpm, rpm) %{rpmdir}/mkinstalldirs
%attr(0755, rpm, rpm) %{rpmdir}/rpm.*
%attr(0644, rpm, rpm) %{rpmdir}/rpmpopt*
%attr(0644, rpm, rpm) %{rpmdir}/rpmrc

%rpmattr	%{rpmdir}/rpm2cpio.sh
%rpmattr	%{rpmdir}/tgpg

%ifarch %{ix86} x86_64
%attr(   -, rpm, rpm) %{rpmdir}/platform/i*86-*
%attr(   -, rpm, rpm) %{rpmdir}/platform/athlon-*
%attr(   -, rpm, rpm) %{rpmdir}/platform/pentium*-*
%attr(   -, rpm, rpm) %{rpmdir}/platform/geode-*
%endif
%ifarch alpha
%attr(   -, rpm, rpm) %{rpmdir}/platform/alpha*
%endif
%ifarch %{sunsparc}
%attr(   -, rpm, rpm) %{rpmdir}/platform/sparc*
%endif
%ifarch ppc powerpc
%attr(   -, rpm, rpm) %{rpmdir}/platform/ppc-*
%attr(   -, rpm, rpm) %{rpmdir}/platform/ppc32-*
%attr(   -, rpm, rpm) %{rpmdir}/platform/ppc64-*
%attr(   -, rpm, rpm) %{rpmdir}/platform/powerpc-*
%endif
%ifarch ppc powerpc ppc64
%attr(   -, rpm, rpm) %{rpmdir}/platform/ppc*series-*
%endif
%ifarch ppc64
%attr(   -, rpm, rpm) %{rpmdir}/platform/ppc-*
%attr(   -, rpm, rpm) %{rpmdir}/platform/ppc32-*
%attr(   -, rpm, rpm) %{rpmdir}/platform/ppc64-*
%endif
%ifarch ia64
%attr(   -, rpm, rpm) %{rpmdir}/platform/ia64-*
%endif
%ifarch x86_64
%attr(   -, rpm, rpm) %{rpmdir}/platform/amd64-*
%attr(   -, rpm, rpm) %{rpmdir}/platform/x86_64-*
%attr(   -, rpm, rpm) %{rpmdir}/platform/ia32e-*
%endif
%attr(   -, rpm, rpm) %{rpmdir}/platform/noarch*

%{_mandir}/man[18]/*.[18]*
%lang(pl) %{_mandir}/pl/man[18]/*.[18]*
%lang(ru) %{_mandir}/ru/man[18]/*.[18]*
%lang(ja) %{_mandir}/ja/man[18]/*.[18]*
%lang(sk) %{_mandir}/sk/man[18]/*.[18]*
%lang(fr) %{_mandir}/fr/man[18]/*.[18]*
%lang(ko) %{_mandir}/ko/man[18]/*.[18]*

%config(noreplace,missingok)	/etc/cron.daily/rpm
%config(noreplace,missingok)	/etc/logrotate.d/rpm

%attr(0755, rpm, rpm)	%dir %_localstatedir/lib/rpm

%define	rpmdbattr %attr(0644, rpm, rpm) %verify(not md5 size mtime) %ghost %config(missingok,noreplace)

%rpmdbattr	/var/lib/rpm/Basenames
%rpmdbattr	/var/lib/rpm/Conflictname
%rpmdbattr	/var/lib/rpm/__db.0*
%rpmdbattr	/var/lib/rpm/Dirnames
%rpmdbattr	/var/lib/rpm/Group
%rpmdbattr	/var/lib/rpm/Installtid
%rpmdbattr	/var/lib/rpm/Name
%rpmdbattr	/var/lib/rpm/Packages
%rpmdbattr	/var/lib/rpm/Providename
%rpmdbattr	/var/lib/rpm/Provideversion
%rpmdbattr	/var/lib/rpm/Removetid
%rpmdbattr	/var/lib/rpm/Requirename
%rpmdbattr	/var/lib/rpm/Requireversion
%rpmdbattr	/var/lib/rpm/Triggername

%files build
%defattr(-,root,root)
%doc CHANGES
%doc doc-copy/*
%rpmattr	%{_bindir}/rpmbuild
%rpmattr	%{_prefix}/lib/rpm/brp-*
%rpmattr	%{_prefix}/lib/rpm/check-files
%rpmattr	%{_prefix}/lib/rpm/debugedit
%rpmattr	%{_prefix}/lib/rpm/find-debuginfo.sh
%rpmattr	%{_prefix}/lib/rpm/find-lang.sh
%rpmattr	%{_prefix}/lib/rpm/find-provides
%rpmattr	%{_prefix}/lib/rpm/find-requires
%rpmattr	%{_prefix}/lib/rpm/perldeps.pl
%rpmattr	%{_prefix}/lib/rpm/perl.prov
%rpmattr	%{_prefix}/lib/rpm/perl.req

%rpmattr	%{_prefix}/lib/rpm/check-buildroot
%rpmattr	%{_prefix}/lib/rpm/check-prereqs
%rpmattr	%{_prefix}/lib/rpm/check-rpaths
%rpmattr	%{_prefix}/lib/rpm/check-rpaths-worker
%rpmattr	%{_prefix}/lib/rpm/javadeps
%rpmattr	%{_prefix}/lib/rpm/libtooldeps.sh
%rpmattr	%{_prefix}/lib/rpm/macros.perl
%rpmattr	%{_prefix}/lib/rpm/macros.php
%rpmattr	%{_prefix}/lib/rpm/macros.python
%rpmattr	%{_prefix}/lib/rpm/mono-find-provides
%rpmattr	%{_prefix}/lib/rpm/mono-find-requires
%rpmattr	%{_prefix}/lib/rpm/osgideps.pl
%rpmattr	%{_prefix}/lib/rpm/pkgconfigdeps.sh
%rpmattr	%{_prefix}/lib/rpm/rpmdiff

%rpmattr	%{_prefix}/lib/rpm/rpmdeps
#%rpmattr	%{_prefix}/lib/rpm/trpm
%rpmattr    %{_prefix}/lib/rpm/pythondeps.sh

%{_mandir}/man8/rpmbuild.8*
%{_mandir}/man8/rpmdeps.8*

%if %buildpython
%files -n python-rpm
%defattr(-,root,root)
%{_libdir}/python*/site-packages/rpm
%endif

%files -n %librpmname
%defattr(-,root,root)
%{_libdir}/librpm-%{libver}.so
%{_libdir}/librpmio-%{libver}.so
%{_libdir}/librpmbuild-%{libver}.so

%files -n %librpmnamedevel
%defattr(-,root,root)
%{_includedir}/rpm
%{_libdir}/librpm.la
%{_libdir}/librpm.so
%{_libdir}/librpmio.la
%{_libdir}/librpmio.so
%{_libdir}/librpmbuild.la
%{_libdir}/librpmbuild.so
%{_libdir}/pkgconfig/rpm.pc
