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

%define _host_vendor mandriva

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

%define __find_requires %{rpmdir}/mandriva/find-requires %{?buildroot:%{buildroot}} %{?_target_cpu:%{_target_cpu}}
%define __find_provides %{rpmdir}/mandriva/find-provides

%define rpmversion	4.4.8
%define poptver		1.10.8
%define perlmoduleversion	0.66
%define srcver		%rpmversion
%define libpoptver	0
%define libver		4.4
%define release			    %mkrel 22
%define perlmodulerelease   %mkrel 44
%define poptrelease		%{release}

%define libpoptname  %mklibname popt %{libpoptver}
%define librpmname   %mklibname rpm  %{libver}
%define libpoptnamedevel  %mklibname -d popt
%define librpmnamedevel   %mklibname -d rpm

%define buildpython 1

%define buildnptl 0

%if %{mdkversion} >= 200710
# MDV 2007.1 builds with --hash-style=gnu by default
%define rpmsetup_version 1.34
%endif

%define builddebug 0
%{?_with_debug:%define builddebug 1}

%{?_with_python:%define buildpython 1}
%{?_without_python:%define buildpython 0}

%{?_with_nptl:%define buildnptl 1}
%{?_without_nptl:%define buildnptl 0}

Summary:	The RPM package management system
Name:		rpm
Version:	%{rpmversion}
Release:	%{release}
Group:		System/Configuration/Packaging

Source:		ftp://ftp.jbj.org/pub/rpm-%{libver}.x/rpm-%{srcver}.tar.bz2

# Add some undocumented feature to gendiff
Patch17:	rpm-4.2-gendiff-improved.patch

# (gb) fix built-in zlib dependencies
Patch1:		rpm-4.4.6-deps.patch

# (gb) use shared libraries
Patch2:		rpm-4.4.6-no-static.patch

# (gb) force generation of PIC code for static libs that can be built into a DSO (zlib, file)
Patch3:		rpm-4.4.6-pic.patch

# (pixel) resurrected patch. useful when used together with "private" in macros.cdb
Patch13:	rpm-4.4.8-global-RPMLOCK.patch

# if %post of foo-2 fails,
# or if %preun of foo-1 fails,
# or if %postun of foo-1 fails,
# => foo-1 is not removed, so we end up with both packages in rpmdb
# this patch makes rpm ignore the error in those cases
# failing %pre must still make the rpm install fail (#23677)
#
# (nb: the exit code for pretrans/posttrans & trigger/triggerun/triggerpostun
#       scripts is ignored with or without this patch)
Patch22:        rpm-4.4.6-non-pre-scripts-dont-fail.patch

# (fredl) add loging facilities through syslog
Patch31:	rpm-4.4.3-syslog.patch

# Check amd64 vs x86_64, these arch are the same
Patch44:	rpm-4.4.1-amd64.patch

# Backport from 4.2.1 provides becoming obsoletes bug (fpons)
Patch49:	rpm-4.4.3-provides-obsoleted.patch

# Introduce new ppc32 arch. Fix ppc64 bi-arch builds. Fix ppc builds on newer CPUs.
Patch56:	rpm-4.4.6-ppc32.patch

# ok for this
Patch63:	rpm-4.4.6-dont-install-delta-rpms.patch

# This patch ask to read /usr/lib/rpm/vendor/rpmpopt too
Patch64:    rpm-4.4.1-morepopt.patch

# Being able to read old rpm (build with rpm v3)
# See https://bugzilla.redhat.com/bugzilla/show_bug.cgi?id=127113#c12
Patch68:    rpm-4.4.1-region_trailer.patch

# In original rpm, -bb --short-circuit does not work and run all stage
# From popular request, we allow to do this
# http://qa.mandriva.com/show_bug.cgi?id=15896
Patch70:	rpm-4.4.1-bb-shortcircuit.patch

# http://www.redhat.com/archives/rpm-list/2005-April/msg00131.html
# http://www.redhat.com/archives/rpm-list/2005-April/msg00132.html
Patch71:    rpm-4.4.4-ordererase.patch

# File conflicts when rpm -i
# https://bugzilla.redhat.com/bugzilla/show_bug.cgi?id=151609
Patch72:    rpm-4.4.1-fileconflicts.patch

# Allow to set %_srcdefattr for src.rpm
Patch77:    rpm-source-defattr.patch

# Do not use futex, but fcntl
Patch78:    rpm-4.4.6-fcntl.patch

Patch82:    rpm-4.4.3-ordering.patch

# don't conflict for doc files from colored packages
# (to be able to install lib*-devel together with lib64*-devel even if they have conflicting manpages)
Patch83: rpm-4.2.3-no-doc-conflicts.patch

# Fix http://qa.mandriva.com/show_bug.cgi?id=19392
Patch84: rpm-4.4.4-rpmqv-ghost.patch

# Install perl module in vendor directory
Patch85: rpm-4.4.4-perldirs.patch

# Use temporary table for Depends DB (Olivier Thauvin upstream)
Patch86: rpm-4.4.6-depsdb.patch

# Currently we prefer to disable dependencies over parents directory
Patch87: rpm-4.4.6-no-dirnames-dep.patch

# rpm 4.4.6 killed SOURCEPACKAGE, but this was announce lately, and will
# break all older tools that was using it (mdv 2006, 2005) which need this
# tag to know it is possible to rebuild a src.rpm
# This patch readd the tag into src.rpm
Patch88: rpm-4.4.6-SOURCEPACKAGE.patch

# make rpmdb cpp compliant (sptutle)
# reported upstream, I hope to see this include
Patch89: rpm-4.4.6-rpmdb.h-cpp-fix.patch

# avoids taking into account duplicates in file list when checking
# for unpackaged files
Patch91: rpm-4.4.6-check-dupl-files.patch

# with tar >= 1.15.91, one needs the --wildcard option to list *.spec
# files (for rpm -ta)
Patch92: rpm-4.4.6-newtar.patch

# This patch adds again a workaround to allow rpm to read/install
# rpm v3 - Internal format is likely the same into rpm v4, data is
# just organised in another way

Patch94: rpm-4.4.6-rpmv3-support.patch

# fix free on invalid pointer after displaying "Unable to open temp file"
Patch98: rpm-4.4.6-fix-free-on-bad-pointer.patch

# without this patch, when pkg rpm-build is not installed,
# using rpm -bs t.spec returns: "t.spec: No such file or directory"
Patch100: rpm-4.4.6-fix-error-message-rpmb-not-installed.patch

# librpm uses bavail ie "free blocks avail to non-superuser"
# that's ok, it will help keeping some free space, even for root
# but when bavail == 0, librpm thinks statfs failed, and do not check
# so setting bavail to 1 when bavail it is 0
# (no package should fit in one block!)
Patch107: rpm-4.4.8-do-check-free-size-when-bavail-is-0.patch

Patch108: rpm-4.4.6-use-dgettext-instead-of-gettext-to-allow-use-of-multilibs.patch

Patch109: rpm-build-expand-field-for-single-token.patch

Patch111: rpm-check-file-trim-double-slash-in-buildroot.patch

Patch112: rpm-dont-use-rpmio-to-read-file-for-script.patch

# Patch from cvs
# using _docdir_fmt for doc directory
Patch113: rpm-4.4.8-macro_doc_fmt.patch

Patch114: rpm-read-vendor-macros.patch

Patch115: rpm-4.4.8-dont-clean-buildroot-in-install.patch

# Fix #31287, rpm -V do not use same space count
Patch116: rpm-qv-use-same-indentation.patch

# if file exists and is not yet in db, rpm don't check and replace it
Patch117: rpm-dont-replace-config-not-in-db.patch

Patch118: rpm-4.4.8-lowercase-os-for-platform.patch

# HAVE_LOCALE_H is used by system.h, ensure it is defined properly
# (the issue only occurs when compiling without __OPTIMIZE__ (ie -O2)
#  otherwise libintl.h do include locale.h)
# nb: this issue is fixed in cvs HEAD
Patch119: rpm-4.4.8-fix-build-without-O2.patch

Patch120: rpm-4.4.8-fix-segfault-for-old-pkg-with-Postin-but-no-Postinprog.patch

# important patch fixing parse_hdlist (and so genhdlist2) on heavy loaded boxes
# (without this patch it timeouts after a read miss of 1 second (even a pipe),
# and there is no way we can retry since we would need to backtrack the fd)
Patch121: rpm-4.4.8-raise-read-timeout-to-60secs.patch

# this handles buggy rpm ftp://ftp.free.fr/mirrors/plf.zarb.org/mandriva/2007.1/free/release/binary/x86_64/lib64spectrum2-0.2.2-4plf.x86_64.rpm
# which has only 7 DIRNAMES/BASENAMES entries, but more FILELINKTOS entries (#32102)
# a better fix may be to cleanup the mess when reading the header?
Patch122: rpm-4.4.8-do-not-crash-when-FILELINKTOS-has-more-entries-than-DIRNAMES.patch

# from rpm.org 4.4.2.2: make find-lang --with-gnome picks up omf files (rhbz#251400)
Patch123: rpm-4.4.8-find-lang-omf-files.patch

# [pixel] without this patch, "rpm -e" or "rpm -U" will need to stat(2) every dirnames of
# files from the package (eg COPYING) in the db. This is quite costly when not in cache 
# (eg on a test here: >300 stats, and so 3 seconds after a "echo 3 > /proc/sys/vm/drop_caches")
# this breaks urpmi test case test_rpm_i_fail('gd') in superuser--file-conflicts.t,
# but this is bad design anyway
Patch124: rpm-4.4.8-speedup-by-not-checking-same-files-with-different-paths-through-symlink.patch

# patch from popt cvs (removes N_ from popt.h) (fixes #31397)
Patch125: popt-fix-N_.patch

# allow to use "linux32 rpm -bb" instead of "linux32 rpm -bb --target x86_64"
Patch126: rpm-4.4.8-use-etc-platform32-when-linux32.patch

# make "rpm -bb --quiet" quiet as should be 
# (without this patch, the option is simply ignored in rpmcliAllPoptTable)
Patch127: rpm-4.4.8-handle-rpmbuild--quiet.patch

# fix rpm -K segfaulting on corrupted header (#33735)
Patch128: rpm-4.4.8-fix-rpm-K-segfault-on-corrupted-header.patch

# if "a" suggests "b", rpm rightfully allows to remove "b"
# but rpm must not put in cache that "b" can be removed,
# because if "c" requires "b", rpm must not allow to remove "b"
# (#34342)
Patch129: rpm-4.4.8-do-not-cache-unsatisfied-suggest.patch

#(peroyvind): Fix usage of more recent lzma utils
Patch130:	rpm-4.5-lzma-fixes.patch

License:	GPL
BuildRequires:	autoconf >= 2.57
BuildRequires:	doxygen
BuildRequires:	zlib-devel
BuildRequires:  bzip2-devel
BuildRequires:	automake >= 1.8
BuildRequires:	elfutils-devel
BuildRequires:	sed >= 4.0.3
BuildRequires:	libbeecrypt-devel
BuildRequires:	ed, gettext-devel
BuildRequires:  libsqlite3-devel
BuildRequires:  neon0.26-devel
BuildRequires:  rpm-mandriva-setup-build %{?rpmsetup_version:>= %{rpmsetup_version}}
BuildRequires:  readline-devel
BuildRequires:	ncurses-devel
BuildRequires:  openssl-devel >= 0.9.8
BuildRequires:	perl-devel
BuildRequires:  liblua-devel
# Need for doc
BuildRequires:	graphviz
BuildRequires:	tetex
%if %buildpython
BuildRequires:	python-devel
%endif
%if %buildnptl
# BuildRequires:	nptl-devel
%endif

Requires:	bzip2 >= 0.9.0c-2
Requires:	lzma
Requires:	cpio
Requires:	gawk
Requires:	glibc >= 2.1.92
Requires:	mktemp
Requires:	popt = %{poptver}-%{poptrelease}
Requires:	setup >= 2.2.0-8mdk
Requires:	rpm-mandriva-setup >= 1.42
Requires:	update-alternatives
Requires:	%librpmname = %version-%release
Conflicts:	patch < 2.5
Conflicts:	menu < 2.1.5-29mdk
Conflicts:	locales < 2.3.1.1
Conflicts:	man-pages-fr < 0.9.7-16mdk
Conflicts:	man-pages-pl < 0.4-9mdk
Conflicts:	perl-URPM < 1.63-3mdv2008.0
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
URL:            http://rpm5.org/
Requires(pre):		rpm-helper >= 0.8
Requires(pre):		coreutils
Requires(postun):	rpm-helper >= 0.8

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
Requires:	rpm = %{version}-%{release}
Requires:	%libpoptnamedevel = %{poptver}-%{poptrelease}
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
Requires:	unzip
Requires:	elfutils
Requires:	rpm = %{version}-%{release}
Requires:	rpm-mandriva-setup-build %{?rpmsetup_version:>= %{rpmsetup_version}}

%description build
This package contains scripts and executable programs that are used to
build packages using RPM.

%if %buildpython
%package -n python-rpm
Summary:	Python bindings for apps which will manipulate RPM packages
Group:		Development/Python
Requires:	python >= %{pyver}
Requires:	rpm = %{version}-%{release}
Obsoletes:  rpm-python < %version-%release
Provides:   rpm-python = %version-%release

%description -n python-rpm
The rpm-python package contains a module which permits applications
written in the Python programming language to use the interface
supplied by RPM (RPM Package Manager) libraries.

This package should be installed if you want to develop Python
programs that will manipulate RPM packages and databases.
%endif

%package -n popt-data
Summary: popt static data
Group:		System/Libraries
Version:	%{poptver}
Release:    %{poptrelease}

%description -n popt-data
This package contains popt data files like locales.

%package -n %libpoptname
Summary:	A C library for parsing command line parameters
Group:		System/Libraries
Version:	%{poptver}
Release:	%{poptrelease}
Requires:   popt-data >= %{poptver}
Provides:   lib%{name} = %{poptver}-%{poptrelease}
Provides:   popt = %{poptver}-%{poptrelease}
Obsoletes:  popt <= 1.8.3

%description -n %libpoptname
Popt is a C library for parsing command line parameters.  Popt was
heavily influenced by the getopt() and getopt_long() functions, but it
improves on them by allowing more powerful argument expansion.  Popt
can parse arbitrary argv[] style arrays and automatically set
variables based on command line arguments.  Popt allows command line
arguments to be aliased via configuration files and includes utility
functions for parsing arbitrary strings into argv[] arrays using
shell-like rules.

%package -n %libpoptnamedevel
Summary:	A C library for parsing command line parameters
Group:		Development/C
Version:	%{poptver}
Release:	%{poptrelease}
Requires:	%libpoptname = %{poptver}-%{poptrelease}
Provides:   popt-devel = %{poptver}-%{poptrelease}
Provides:   libpopt-devel = %{poptver}-%{poptrelease}
Obsoletes:  popt-devel <= 1.8.3
Obsoletes:  %{_lib}popt0-devel

%description -n %libpoptnamedevel
Popt is a C library for parsing command line parameters.  Popt was
heavily influenced by the getopt() and getopt_long() functions, but it
improves on them by allowing more powerful argument expansion.  Popt
can parse arbitrary argv[] style arrays and automatically set
variables based on command line arguments.  Popt allows command line
arguments to be aliased via configuration files and includes utility
functions for parsing arbitrary strings into argv[] arrays using
shell-like rules.

Install popt-devel if you're a C programmer and you'd like to use its
capabilities.

%define		perlmodule	RPM
%package -n perl-%perlmodule
Summary:	Perl bindings for RPM
Group:		Development/Perl
Version:	%perlmoduleversion
Release:	%perlmodulerelease

%description -n perl-%perlmodule
The RPM Perl module provides an object-oriented interface to querying both
the installed RPM database as well as files on the filesystem.

%prep
%setup -q -n %name-%srcver

%patch1 -p1 -b .deps

%patch2 -p1 -b .no-static

%patch3 -p1 -b .pic

#%patch13 -p1 -b .lock

%patch17 -p0 -b .improved

%patch22 -p1 -b .fail

%patch31 -p0 -b .syslog

%patch44 -p1 -b .amd64

%patch49 -p0 -b .provides

%patch56 -p0 -b .ppc32

%patch63 -p0 -b .dont-install-delta-rpms

%patch64 -p0 -b .morepopt

%patch68 -p0 -b .region_trailer

#%patch69 -p0 -b .trans

%patch70 -p0 -b .shortcircuit

%patch71 -p0  -b .ordererase

%patch72 -p0  -b .fileconflicts

%patch77 -p0  -b .srcdefattr

%if %buildnptl
%else
%patch78 -p0  -b .fcntl
%endif

%patch82 -p0 -b .ordering

%patch83 -p1 -b .no-doc-conflicts

%patch84 -p0 -b .poptQVghost

%patch85 -p0 -b .perldirs

%patch86 -p0 -b .depsdb

%patch87 -p0 -b .no-dirname-dep

%patch88 -p0 -b .sourcepackage

%patch89 -p0 -b .cpp-compliant

%patch91 -p0 -b .check-dupl-files

%patch92 -p0 -b .newtar

%patch94 -p1 -b .rpmv3-support

%patch98 -p1 -b .free

%patch100 -p1 -b .rpmb-missing

%patch107 -p1

%patch108 -p1

# rpm now check there is only one token per field
# too bad, the check is performed before macro expansion...
%patch109 -p0 -b .singletoken

# Fix diff issue when buildroot contains some "//"
%patch111 -p0 -b .trim-slash

# Fix strange issue making %pre/post/... -f not working
%patch112 -p0 -b .build-no-rpmio

%patch113 -p0 -b .docdir-macros

%patch114 -p0 -b .read-our-macros

%patch115 -p0 -b .noclean

%patch116 -p0 -b .rpmVspace

%patch117 -p0 -b .rpmnew

%patch118 -p0 -b .lowercaseos

%patch119 -p1
%patch120 -p1
%patch121 -p1 -b .timeout
%patch122 -p1

%patch123 -p1
%patch124 -p1

cd popt
%patch125 -p0 -b .N_
cd ..

%patch126 -p1 -b .linux32

%patch127 -p1 -b .quiet

%patch128 -p1
%patch129 -p1

%patch130 -p0 -b .lzmafix

%build

for dir in . popt file zlib db/dist; do
    (
    cd $dir
    libtoolize --force
    aclocal
    automake -a
    autoconf
    )
done

# rpm takes care of --libdir but explicitelly setting --libdir on
# configure breaks make install, but this does not matter.
# --build, we explictly set 'mandriva' as our config subdir and 
# _host_vendor are 'mandriva'
%if %builddebug
RPM_OPT_FLAGS=-g
%endif
CFLAGS="$RPM_OPT_FLAGS -fPIC" CXXFLAGS="$RPM_OPT_FLAGS -fPIC" \
    ./configure \
        --build=%{_target_cpu}-%{_host_vendor}-%{_target_os}%{?_gnu} \
        --prefix=%{_prefix} \
        --sysconfdir=%{_sysconfdir} \
        --localstatedir=%{_localstatedir} \
        --mandir=%{_mandir} \
        --infodir=%{_infodir} \
        --enable-nls \
        --without-javaglue \
%if %builddebug
        --enable-debug \
%endif
%if %buildnptl
        --enable-posixmutexes \
%else
        --with-mutex=UNIX/fcntl \
%endif
%if %buildpython
        --with-python=%{pyver} \
%else
        --without-python \
%endif
        --with-glob \
        --without-selinux \
        --with-apidocs 

# We should use the zlib provided with rpm:
# 21:17 < Nanar> why using ../../zlib in file/ instead system library ?
# 21:38 < jbj> Nanar: zlib modified to make *.rpm packages rsync friendly.
#              See https://svn.uhulinux.hu/packages/dev/zlib/patches/02-rsync.patch
# 21:38 < jbj> rip if you don't want to be rsync friendly. <shrug>
%make -C zlib AM_CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="-fPIC"

%make

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=%buildroot install

# We put a popt copy in /%_lib for application in /bin
# This is not for rpm itself as it requires all rpmlib
# from /usr/%_lib
mkdir -p $RPM_BUILD_ROOT/%{_lib}
mv $RPM_BUILD_ROOT%{_libdir}/libpopt.so.* $RPM_BUILD_ROOT/%{_lib}
ln -s ../../%{_lib}/libpopt.so.0 $RPM_BUILD_ROOT%{_libdir}
ln -sf libpopt.so.0 $RPM_BUILD_ROOT%{_libdir}/libpopt.so

rm -f $RPM_BUILD_ROOT%{_prefix}/lib/rpmpopt
ln -s rpm/rpmpopt-%{rpmversion} $RPM_BUILD_ROOT%{_prefix}/lib/rpmpopt

%ifarch ppc powerpc
ln -sf ppc-mandriva-linux $RPM_BUILD_ROOT%{rpmdir}/powerpc-mandriva-linux
%endif

#mv -f $RPM_BUILD_ROOT/%{rpmdir}/rpmdiff $RPM_BUILD_ROOT/%{_bindir}

# Save list of packages through cron
mkdir -p ${RPM_BUILD_ROOT}/etc/cron.daily
install -m 755 scripts/rpm.daily ${RPM_BUILD_ROOT}/etc/cron.daily/rpm

mkdir -p ${RPM_BUILD_ROOT}/etc/logrotate.d
install -m 644 scripts/rpm.log ${RPM_BUILD_ROOT}/etc/logrotate.d/rpm

mkdir -p $RPM_BUILD_ROOT/etc/rpm/
cat << E_O_F > $RPM_BUILD_ROOT/etc/rpm/macros.cdb
%%__dbi_cdb      %%{nil}
%%__dbi_other    %%{?_tmppath:tmpdir=%%{_tmppath}} usedbenv create \
                 mpool mp_mmapsize=8Mb mp_size=512kb verify
E_O_F

mkdir -p $RPM_BUILD_ROOT/var/lib/rpm
for dbi in \
	Basenames Conflictname Dirnames Group Installtid Name Providename \
	Provideversion Removetid Requirename Requireversion Triggername \
	Packages __db.001 __db.002 __db.003 __db.004
do
    touch $RPM_BUILD_ROOT/var/lib/rpm/$dbi
done

find apidocs -type f | xargs perl -p -i -e "s@$RPM_BUILD_DIR/%{name}-%{rpmversion}@@g"

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
  rm -f  .%{_libdir}/python*/site-packages/poptmodule.{a,la}
  rm -f  .%{_libdir}/python*/site-packages/rpmmodule.{a,la}
  rm -f  .%{rpmdir}/{Specfile.pm,cpanflute2,cpanflute,sql.prov,sql.req,tcl.req}
  rm -f  .%{rpmdir}/{config.site,cross-build,rpmdiff.cgi}
  rm -f  .%{rpmdir}/trpm
  rm -f  .%{_bindir}/rpmdiff
)

%{rpmdir}/%{_host_vendor}/find-lang.pl $RPM_BUILD_ROOT %{name}
%{rpmdir}/%{_host_vendor}/find-lang.pl $RPM_BUILD_ROOT popt

%check

#make -C popt check-TESTS

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

%post -n %librpmname -p /sbin/ldconfig
%postun -n %librpmname -p /sbin/ldconfig

%post -n %libpoptname -p /sbin/ldconfig
%postun -n %libpoptname -p /sbin/ldconfig

%define	rpmattr		%attr(0755, rpm, rpm)

%files -f %{name}.lang
%defattr(-,root,root)
%doc GROUPS CHANGES doc/manual/[a-z]*
%attr(0755,rpm,rpm) /bin/rpm
%attr(0755, rpm, rpm) %{_bindir}/rpm2cpio
%attr(0755, rpm, rpm) %{_bindir}/gendiff
%attr(0755, rpm, rpm) %{_bindir}/rpmdb
%attr(0755, rpm, rpm) %{_bindir}/rpm[eiukqv]
%attr(0755, rpm, rpm) %{_bindir}/rpmsign
%attr(0755, rpm, rpm) %{_bindir}/rpmquery
%attr(0755, rpm, rpm) %{_bindir}/rpmverify

%dir %{_localstatedir}/spool/repackage
%dir %{rpmdir}
%dir /etc/rpm
%config(noreplace) /etc/rpm/macros
%config(noreplace) /etc/rpm/macros.cdb
%dir /etc/rpm/macros.d
%attr(0755, rpm, rpm) %{rpmdir}/config.guess
%attr(0755, rpm, rpm) %{rpmdir}/config.sub
#%attr(0755, rpm, rpm) %{rpmdir}/convertrpmrc.sh
%attr(0755, rpm, rpm) %{rpmdir}/rpmdb_*
%attr(0644, rpm, rpm) %{rpmdir}/macros
%attr(0755, rpm, rpm) %{rpmdir}/mkinstalldirs
%attr(0755, rpm, rpm) %{rpmdir}/rpm.*
%attr(0755, rpm, rpm) %{rpmdir}/rpm[deiukqv]
%attr(0644, rpm, rpm) %{rpmdir}/rpmpopt*
%attr(0644, rpm, rpm) %{rpmdir}/rpmrc

%{_prefix}/lib/rpmpopt
%rpmattr	%{rpmdir}/rpm2cpio.sh
%rpmattr	%{rpmdir}/tgpg

%ifarch %{ix86}
%attr(   -, rpm, rpm) %{rpmdir}/i*86-*
#%attr(   -, rpm, rpm) %{rpmdir}/k6*
%attr(   -, rpm, rpm) %{rpmdir}/athlon*
%attr(   -, rpm, rpm) %{rpmdir}/pentium*
%endif
%ifarch alpha
%attr(   -, rpm, rpm) %{rpmdir}/alpha*
%endif
%ifarch %{sunsparc}
%attr(   -, rpm, rpm) %{rpmdir}/sparc*
%endif
%ifarch ppc powerpc
%attr(   -, rpm, rpm) %{rpmdir}/ppc-*
%attr(   -, rpm, rpm) %{rpmdir}/ppc32-*
%attr(   -, rpm, rpm) %{rpmdir}/ppc64-*
%attr(   -, rpm, rpm) %{rpmdir}/powerpc-*
%endif
%ifarch ppc powerpc ppc64
%attr(   -, rpm, rpm) %{rpmdir}/ppc*series-*
%endif
%ifarch ppc64
%attr(   -, rpm, rpm) %{rpmdir}/ppc-*
%attr(   -, rpm, rpm) %{rpmdir}/ppc32-*
%attr(   -, rpm, rpm) %{rpmdir}/ppc64-*
%endif
%ifarch ia64
%attr(   -, rpm, rpm) %{rpmdir}/ia64-*
%endif
%ifarch x86_64
%attr(   -, rpm, rpm) %{rpmdir}/amd64-*
#%attr(   -, rpm, rpm) %{rpmdir}/x86_64-*
%attr(   -, rpm, rpm) %{rpmdir}/ia32e-*
%endif
%attr(   -, rpm, rpm) %{rpmdir}/noarch*

%{_prefix}/src/rpm/RPMS/*
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
%dir %{_prefix}/src/rpm
%dir %{_prefix}/src/rpm/BUILD
%dir %{_prefix}/src/rpm/SPECS
%dir %{_prefix}/src/rpm/SOURCES
%dir %{_prefix}/src/rpm/SRPMS
%dir %{_prefix}/src/rpm/RPMS
%rpmattr	%{_bindir}/rpmbuild
%rpmattr	%{_prefix}/lib/rpm/brp-*
%rpmattr	%{_prefix}/lib/rpm/check-files
%rpmattr	%{_prefix}/lib/rpm/debugedit
%rpmattr	%{_prefix}/lib/rpm/executabledeps.sh
%rpmattr	%{_prefix}/lib/rpm/find-debuginfo.sh
%rpmattr	%{_prefix}/lib/rpm/find-lang.sh
%rpmattr	%{_prefix}/lib/rpm/find-prov.pl
%rpmattr	%{_prefix}/lib/rpm/find-provides
%rpmattr	%{_prefix}/lib/rpm/find-provides.perl
%rpmattr	%{_prefix}/lib/rpm/find-req.pl
%rpmattr	%{_prefix}/lib/rpm/find-requires
%rpmattr	%{_prefix}/lib/rpm/find-requires.perl
%rpmattr	%{_prefix}/lib/rpm/getpo.sh
%rpmattr	%{_prefix}/lib/rpm/http.req
%rpmattr	%{_prefix}/lib/rpm/javadeps.sh
%rpmattr	%{_prefix}/lib/rpm/libtooldeps.sh
%rpmattr	%{_prefix}/lib/rpm/magic
%rpmattr	%{_prefix}/lib/rpm/magic.mgc
%rpmattr	%{_prefix}/lib/rpm/magic.mime
%rpmattr	%{_prefix}/lib/rpm/magic.mime.mgc
%rpmattr	%{_prefix}/lib/rpm/perldeps.pl
%rpmattr	%{_prefix}/lib/rpm/perl.prov
%rpmattr	%{_prefix}/lib/rpm/perl.req
%rpmattr	%{_prefix}/lib/rpm/pkgconfigdeps.sh
%rpmattr    %{_prefix}//lib/rpm/php.prov
%rpmattr    %{_prefix}//lib/rpm/php.req
%rpmattr    %{_prefix}//lib/rpm/symclash.py
%rpmattr    %{_prefix}//lib/rpm/symclash.sh

%rpmattr	%{_prefix}/lib/rpm/rpm[bt]
%rpmattr	%{_prefix}/lib/rpm/rpmdeps
#%rpmattr	%{_prefix}/lib/rpm/trpm
%rpmattr	%{_prefix}/lib/rpm/u_pkg.sh
%rpmattr	%{_prefix}/lib/rpm/vpkg-provides.sh
%rpmattr	%{_prefix}/lib/rpm/vpkg-provides2.sh
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
%{_libdir}/librpmdb-%{libver}.so
%{_libdir}/librpmio-%{libver}.so
%{_libdir}/librpmbuild-%{libver}.so

%files -n %librpmnamedevel
%defattr(-,root,root)
#%doc apidocs/html
%{_includedir}/rpm
%{_libdir}/librpm.a
%{_libdir}/librpm.la
%{_libdir}/librpm.so
%{_libdir}/librpmdb.a
%{_libdir}/librpmdb.la
%{_libdir}/librpmdb.so
%{_libdir}/librpmio.a
%{_libdir}/librpmio.la
%{_libdir}/librpmio.so
%{_libdir}/librpmbuild.a
%{_libdir}/librpmbuild.la
%{_libdir}/librpmbuild.so
%{_mandir}/man3/RPM*

%files -n popt-data -f popt.lang
%defattr(-,root,root)

%files -n %libpoptname
%defattr(-,root,root)
/%{_lib}/libpopt.so.*
%{_libdir}/libpopt.so.*

%files -n %libpoptnamedevel
%defattr(-,root,root)
%{_libdir}/libpopt.a
%{_libdir}/libpopt.la
%{_libdir}/libpopt.so
%{_includedir}/popt.h
%{_mandir}/man3/popt.3*

%files -n perl-%perlmodule
%defattr(-,root,root)
%doc perl/Changes
%{perl_vendorarch}/%{perlmodule}.pm
%{perl_vendorarch}/auto/%{perlmodule}

