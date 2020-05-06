# WARNING: This package is synced with Fedora and Mageia

# (ngompa): This is primarily for the znver1 patch, as it's a pain to rediff...
%global _default_patch_fuzz 2

%ifos linux
# Get rid of any -gnu/-gnueabi suffix for platform names
# to get traditional directory names
%ifarch %{x86_64}
%define _target_platform x86_64-%{_vendor}-linux
%else
%ifarch %{aarch64}
%define _target_platform aarch64-%{_vendor}-linux
%else
%define _target_platform %{_target_cpu}-%{_vendor}-linux
%endif
%endif
%endif

%define lib64arches %{x86_64} %{aarch64} %{riscv64}

%ifarch %lib64arches
%define _lib lib64
%else
%define _lib lib
%endif

%define _prefix /usr
%define _libdir %{_prefix}/%{_lib}
%define _bindir %{_prefix}/bin
%define _sysconfdir /etc
%define _datadir /usr/share
%define _defaultdocdir %{_datadir}/doc
%define _localstatedir /var
%define _infodir %{_datadir}/info

%if %{?mklibname:0}%{?!mklibname:1}
%define mklibname(ds)  %{_lib}%{1}%{?2:%{2}}%{?3:_%{3}}%{-s:-static}%{-d:-devel}
%endif

%if %{?distsuffix:0}%{?!distsuffix:1}
%define distsuffix .omv
%endif

%if %{?_real_vendor:0}%{?!_real_vendor:1}
%define _real_vendor openmandriva
%endif

%if %{?pyver:0}%{?!pyver:1}
%define pyver %(python -V 2>&1 | cut -f2 -d" " | cut -f1,2 -d".")
%endif

# If they aren't provided by a system installed macro, define them
%{!?__python3: %global __python3 /usr/bin/python3}

%{!?py3_build: %global py3_build LDSHARED="%{__cc} -pthread -shared %{optflags}" CFLAGS="%{optflags}" %{__python3} setup.py build}
%{!?py3_install: %global py3_install %{__python3} setup.py install -O1 --skip-build --root %{buildroot}}

%{!?python3_sitearch: %global python3_sitearch %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

%define __find_requires %{rpmhome}/%{_real_vendor}/find-requires %{?buildroot:%{buildroot}} %{?_target_cpu:%{_target_cpu}}
%define __find_provides %{rpmhome}/%{_real_vendor}/find-provides

# run internal testsuite?
## TODO: Enable by default once tests exec failures are fixed
%bcond_with check
# build with plugins?
%bcond_without plugins
# build with new db format
%bcond_with ndb
# build with openmp support?
## TODO: Enable by default once mock+ABF are fixed
%bcond_with openmp

# Define directory which holds rpm config files, and some binaries actually
# NOTE: it remains */lib even on lib64 platforms as only one version
#       of rpm is supported anyway, per architecture
%define rpmhome /usr/lib/rpm

%global snapver %{nil}
%if "%{snapver}" != ""
%global srcver %{version}%{?snapver:-%{snapver}}
%define srcdir %{?snapver:testing}%{!?snapver:%{name}-%(v=%{version}; echo ${v%.*}.x)}
%else
%global srcver %{version}
%define srcdir %{name}-%(v=%{version}; echo ${v%.*}.x)
%endif
%global libmajor	9
%global librpmname      %mklibname rpm  %{libmajor}
%global librpmnamedevel %mklibname -d rpm
%global librpmsign      %mklibname rpmsign %{libmajor}
%global librpmbuild     %mklibname rpmbuild %{libmajor}

%global rpmsetup_version 0.4.0

Summary:	The RPM package management system
Name:		rpm
Epoch:		2
Version:	4.15.1
%if "%{snapver}" != ""
Release:	0.%{snapver}.1
%else
Release:	13
%endif
Group:		System/Configuration/Packaging
Url:		http://www.rpm.org/
Source0:	http://ftp.rpm.org/releases/%{srcdir}/%{name}-%{srcver}.tar.bz2
# extracted from http://pkgs.fedoraproject.org/cgit/redhat-rpm-config.git/plain/macros:
Source1:	macros.filter
Source2:	rpm.rpmlintrc
#
# Fedora patches
#

# https://github.com/rpm-software-management/rpm/pull/473
Patch6:	0001-find-debuginfo.sh-decompress-DWARF-compressed-ELF-se.patch

# https://github.com/rpm-software-management/rpm/pull/997
Patch7:		https://github.com/rpm-software-management/rpm/pull/997/commits/4976a071b41ce71a281e9f28a7904172a3a24c85.patch

# These are not yet upstream
Patch906:	rpm-4.7.1-geode-i686.patch
# Probably to be upstreamed in slightly different form
Patch907:	rpm-4.15.x-ldflags.patch

Patch912:	0001-Revert-Improve-ARM-detection.patch

#
# End of FC patches
#

#
# Upstream patches not carried by FC:
#

#
# Mageia patches
#

# In original rpm, -bb --short-circuit does not work and run all stage
# From popular request, we allow to do this
# http://qa.mandriva.com/show_bug.cgi?id=15896
Patch70:	rpm-4.15.0-bb-shortcircuit.patch

# don't conflict for doc files
# (to be able to install lib*-devel together with lib64*-devel even if they have conflicting manpages)
Patch83:	rpm-4.12.0-no-doc-conflicts.patch

# Fix http://qa.mandriva.com/show_bug.cgi?id=19392
# (is this working??)
Patch84:	rpm-4.15.0-rpmqv-ghost.patch

# [Dec 2008] macrofiles from rpmrc does not overrides MACROFILES anymore
# Upstream 4.11 will have /usr/lib/rpm/macros.d:
Patch144:	rpm-4.9.0-read-macros_d-dot-macros.patch

# without this patch, "#%%define foo bar" is surprisingly equivalent to "%%define foo bar"
# with this patch, "#%%define foo bar" is a fatal error
# Bug still valid => Send upstream for review.
Patch145:	rpm-forbid-badly-commented-define-in-spec.patch

# (nb: see the patch for more info about this issue)
#Patch151: rpm-4.6.0-rc1-protect-against-non-robust-futex.patch

#
# Merge mageia's perl.prov improvements back into upstream:
#
# making sure automatic provides & requires for perl package are using the new
# macro %%perl_convert_version:
Patch162:	use_perl_convert_version.diff

#
# Merge mageia's find-requires.sh improvements back into upstream:
#
# (pt) generate ELF provides for libraries, not only for executables
Patch180:	elf_libs_req.diff
# [Suse]add --assumeexec option for previous patch:
Patch181:	assumeexec.diff
# (Martin Whitaker) disable the systemd-inhibit plugin when systemd-logind is not running (mga#20016):
Patch182:	systemd-inhibit-requires-logind.patch

# (tv) Commit 816c7cf3fdae5c45de02a42a2245549778e2ca80 defaults to ignoring autodeps from docfile,
# which break perl autodeps from *META*:
Patch200:	dont-filter-autodeps-from-doc-by-default.patch

# Various arch enabling:
Patch3003:	rpm_arm_mips_isa_macros.patch


# Mageia patches that are easier to rediff on top of FC patches:
#---------------------------------------------------------------
# (tv) merge mga stuff from rpm-setup:
# (for spec-helper)
Patch4000:	rpm-4.15.0-find-debuginfo__mga-cfg.diff

#
# OpenMandriva patches
#

#
# Upstream patches not carried by Fedora or Mageia
#

# Improvements to pythondistdeps generator
Patch1001:	0001-scripts-pythondistdeps-Match-python-version-if-minor.patch
Patch1002:	0002-scripts-pythondistdeps-Use-rich-deps-for-semanticall.patch
Patch1003:	0003-scripts-pythondistdeps-Handle-compatible-release-ope.patch
Patch1004:	0004-scripts-pythondistdeps-Handle-version-ending-with.patch
Patch1005:	0005-scripts-pythondistdeps-Only-add-setuptools-requireme.patch
Patch1006:	0006-scripts-pythondistdeps-Only-print-rich-dep-list-when.patch
Patch1007:	0007-Python-dist-deps-Put-bounded-requirements-into-paren.patch

#
# Patches proposed upstream
#

# Add support for %%optional
# From: https://github.com/rpm-software-management/rpm/pull/417
Patch5001:	rpm-4.15.x-omv-optional-filelist-tag.patch
# Add znver1 as an x86_64 superset
Patch5006:	rpm-4.15.x-omv-znver1-arch.patch
# Clarify ARM architecture macro and add aarch64 macro
Patch5007:	rpm-4.15.x-omv-clarify-arm-macro.patch
# Add RISC-V architecture macros
Patch5008:	rpm-4.15.x-omv-riscv-arch-macro.patch

#
# OpenMandriva specific patches
#

# Default to keeping a patch backup file for gendiff
# and follow file naming conventions
Patch6004:	rpm-4.15.x-omv-patch-gendiff.patch
# Default to i686 targets on 32bit i686+ machines
Patch6005:	rpm-4.14-omv-i386-to-i686.patch
Patch6007:	riscv64-optflags.patch
Patch6008:	rpm-4.15.x-rosa-dont-require-contiguous-sighdr.patch
# Run the debuginfo generator after, not before, other postprocessing scripts
# have run.
# This is important to make sure spec-helper's fix_file_permissions (which
# makes sure library files are executable) is run before find-debuginfo
# (which only looks at executable files) decides what files (not) to split.
# This shrinks OpenJDK by 400 MB -- and certainly can't hurt other packages
# that install libraries with odd permissions.
Patch6009:	rpm-4.15.1-macros-run-debuginfo-after-other-scripts.patch


# Partially GPL/LGPL dual-licensed and some bits with BSD
# SourceLicense: (GPLv2+ and LGPLv2+ with exceptions) and BSD
License:	GPLv2+

BuildRequires:	autoconf
BuildRequires:	bison
BuildRequires:	pkgconf
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(bzip2)
BuildRequires:	pkgconfig(liblzma) >= 5
BuildRequires:	pkgconfig(libzstd)
BuildRequires:	automake
BuildRequires:	doxygen
BuildRequires:	pkgconfig(libelf)
BuildRequires:	binutils-devel
BuildRequires:	gettext-devel
BuildRequires:	db-devel >= 18.1
BuildRequires:	pkgconfig(neon)
BuildRequires:	pkgconfig(popt)
BuildRequires:	magic-devel
BuildRequires:	rpm-%{_real_vendor}-setup-build %{?rpmsetup_version:>= %{rpmsetup_version}}
BuildRequires:	readline-devel
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(libssl)
BuildRequires:	pkgconfig(lua) >= 5.3
BuildRequires:	pkgconfig(libcap)
BuildRequires:	acl-devel
BuildRequires:	pkgconfig(libarchive) >= 3.4.0
BuildRequires:	pkgconfig(python3)
%if %{with check}
# for testsuite:
BuildRequires:	eatmydata
BuildRequires:	fakechroot
BuildRequires:	gnupg2
%endif
%ifarch riscv64
BuildRequires:	atomic-devel
BuildRequires:	clang
%endif

Requires:	bzip2 >= 0.9.0c-2
Requires:	xz
Requires:	zstd
Requires:	cpio
Requires:	gawk
Requires:	coreutils
Requires:	setup >= 2.9.1
Requires:	rpm-%{_real_vendor}-setup >= %{rpmsetup_version}
Requires:	%{librpmname} = %{epoch}:%{version}-%{release}

# This is a completely different implementation of RPM, replacing rpm5
Conflicts:	rpm < %{epoch}:%{version}-%{release}

# Weakly depend on stuff that used to be in main rpm package
Recommends:	rpm-plugin-audit
Recommends:	rpm-plugin-syslog
Recommends:	rpm-plugin-ima
Recommends:	rpm-plugin-systemd-inhibit

%description
The RPM Package Manager (RPM) is a powerful command line driven
package management system capable of installing, uninstalling,
verifying, querying, and updating software packages.  Each software
package consists of an archive of files along with information about
the package like its version, a description, etc.

%package -n %{librpmname}
Summary:	Libraries for manipulating RPM packages
Group:		System/Libraries
License:	GPLv2+ and LGPLv2+ with exceptions
Provides:	librpm = %{version}-%{release}
Provides:	rpm-libs = %{version}-%{release}
# librpm5 is gone...
Obsoletes:	%{_lib}rpm5.4

%description -n %{librpmname}
This package contains the RPM shared libraries.

%package -n %{librpmbuild}
Summary:	Libraries for building and signing RPM packages
Group:		System/Libraries
License:	GPLv2+ and LGPLv2+ with exceptions
Obsoletes:	rpm-build-libs < %{version}-%{release}
Provides:	rpm-build-libs%{?_isa} = %{version}-%{release}

%description -n %{librpmbuild}
This package contains the RPM shared libraries for building and signing
packages.

%package -n %{librpmnamedevel}
Summary:	Development files for applications which will manipulate RPM packages
Group:		Development/C
License:	GPLv2+ and LGPLv2+ with exceptions
Requires:	rpm = %{epoch}:%{version}-%{release}
Provides:	librpm-devel = %{version}-%{release}
Provides:	rpm-devel = %{version}-%{release}
Requires:	pkgconfig(popt)
Requires:	%{librpmname} = %{epoch}:%{version}-%{release}
Requires:	%{librpmbuild} = %{epoch}:%{version}-%{release}
Requires:	%{librpmsign} = %{epoch}:%{version}-%{release}
# We don't provide this anymore...
Obsoletes:	%{_lib}rpm-static-devel < 2:4.14-0

%description -n %{librpmnamedevel}
This package contains the RPM C library and header files.  These
development files will simplify the process of writing programs that
manipulate RPM packages and databases. These files are intended to
simplify the process of creating graphical package managers or any
other tools that need an intimate knowledge of RPM packages in order
to function.

This package should be installed if you want to develop programs that
will manipulate RPM packages and databases.

%package  -n %{librpmsign}
Summary:	Libraries for building and signing RPM packages
Group:		System/Libraries
License:	GPLv2+ and LGPLv2+ with exceptions

%description -n %{librpmsign}
This package contains the RPM shared libraries for building and signing
packages.

%package build
Summary:	Scripts and executable programs used to build packages
Group:		System/Configuration/Packaging
Provides:	perl-generators = %{version}-%{release}
Requires:	autoconf
Requires:	automake
%ifarch %{riscv}
Requires:	atomic-devel
%endif
Requires:	clang
Requires:	file
# We need cputoolize & amd64-* alias to x86_64-* in config.sub
Requires:	libtool-base
Requires:	patch
Requires:	diffutils
Requires:	make
Requires:	tar >= 3.3.2
Requires:	unzip
# Versioned requirement for Patch 400
Requires:	elfutils >= 0.167-2
# FIXME inherited from Mageia, which in turn inherited them from Mandriva
# Nobody knows why -- but probably it's urpmi? Let's see if anything breaks
# without those deps...
#Requires:	perl(CPAN::Meta) >= 2.112.150
#Requires:	perl(ExtUtils::MakeMaker) >= 6.570_700
#Requires:	perl(YAML::Tiny)
Requires:	rpm = %{epoch}:%{version}-%{release}
Requires:	rpm-%{_real_vendor}-setup-build %{?rpmsetup_version:>= %{rpmsetup_version}}
Requires:	%{librpmbuild} = %{epoch}:%{version}-%{release}
# For pythondistdeps generator
Requires:	python-pkg-resources
# Drop until urpmi->dnf transition is complete
%ifarch %{ix86} %{x86_64}
Requires:	rpmlint-%{_target_vendor}-policy >= 0.3.32
Requires:	dwz
Requires:	openmandriva-repos-pkgprefs
%endif
Requires:	spec-helper >= 0.31.12
Requires:	pkgconf
Requires:	systemd-macros
Requires:	go-srpm-macros
Requires:	rpm-helper
Conflicts:	rpm-build < %{epoch}:%{version}-%{release}

%description build
The rpm-build package contains the scripts and executable programs
that are used to build packages using the RPM Package Manager.

%package sign
Summary:	Package signing support
Group:		System/Base

%description sign
This package contains support for digitally signing RPM packages.

%package -n python-%{name}
Summary:	Python 3 bindings for apps which will manipulate RPM packages
Group:		Development/Python
Requires:	rpm = %{epoch}:%{version}-%{release}
Obsoletes:	python-%{name} < %{epoch}:%{version}-%{release}
# Python 2 subpackage is gone
Obsoletes:	python2-%{name} < 2:4.15.1-0

%description -n python-%{name}
The python-rpm package contains a module that permits applications
written in the Python programming language to use the interface
supplied by RPM Package Manager libraries.

This package should be installed if you want to develop Python 3
programs that will manipulate RPM packages and databases.

%package apidocs
Summary:	API documentation for RPM libraries
Group:		Documentation
BuildArch:	noarch

%description apidocs
This package contains API documentation for developing applications
that will manipulate RPM packages and databases.

%package	cron
Summary:	Create daily logs of installed packages
Group:		System/Base
BuildArch:	noarch
Requires:	crontabs
Requires:	logrotate
Requires:	rpm = %{epoch}:%{version}-%{release}
# Incompatible with rpm5
Conflicts:	rpm < 2:4.14.0-0

%description cron
This package contains a cron job which creates daily logs of installed
packages on a system.

%if %{with plugins}
%package plugin-audit
Summary:	Rpm plugin for logging audit events on package operations
Group:		System/Base
BuildRequires:	pkgconfig(audit)
Requires:	%{librpmname}%{?_isa} = %{epoch}:%{version}-%{release}
# Incompatible with rpm5
Conflicts:	rpm < 2:4.14.0-0

%description plugin-audit
Rpm plugin for libaudit support

%package plugin-syslog
Summary:	Rpm plugin for syslog functionality
Group:		System/Base
Requires:	%{librpmname}%{?_isa} = %{epoch}:%{version}-%{release}
# Incompatible with rpm5
Conflicts:	rpm < 2:4.14.0-0

%description plugin-syslog
This plugin exports RPM actions to the system log.

%package plugin-systemd-inhibit
Summary:	Rpm plugin for systemd inhibit functionality
Group:		System/Base
BuildRequires:	pkgconfig(dbus-1)
Requires:	%{librpmname}%{?_isa} = %{epoch}:%{version}-%{release}
# Incompatible with rpm5
Conflicts:	rpm < 2:4.14.0-0

%description plugin-systemd-inhibit
This plugin blocks systemd from entering idle, sleep or shutdown while an rpm
transaction is running using the systemd-inhibit mechanism.

%package plugin-ima
Summary:	Rpm plugin for IMA file signatures
Group:		System/Base
Requires:	%{librpmname}%{?_isa} = %{epoch}:%{version}-%{release}
# Incompatible with rpm5
Conflicts:	rpm < 2:4.14.0-0

%description plugin-ima
This plugin adds support for enforcing and verifying IMA file signatures
in an rpm.

%package plugin-prioreset
Summary:	Rpm plugin for resetting scriptlet priorities for SysV init
Group:		System/Base
Requires:	%{librpmname}%{?_isa} = %{epoch}:%{version}-%{release}
# Incompatible with rpm5
Conflicts:	rpm < 2:4.14.0-0

%description plugin-prioreset
%{summary}

Useful on legacy SysV init systems if you run rpm transactions with
nice/ionice priorities. Should not be used on systemd systems.

%endif # with plugins

%prep
%autosetup -n %{name}-%{srcver} -p1

# Get rid of _python_bytecompile_extra
# https://fedoraproject.org/wiki/Changes/No_more_automagic_Python_bytecompilation
sed -i -e '/^%%_python_bytecompile_extra/d' platform.in

%build
%define _disable_ld_no_undefined 1

%ifarch %{riscv}
# Temporary hardcode, to change defaults on RISC-V
export CC=%{_bindir}/clang
export CXX=%{_bindir}/clang++
%endif

%set_build_flags

autoreconf -i -f

%configure \
    --localstatedir=%{_var} \
    --sharedstatedir=%{_var}/lib \
    --with-vendor=%{_real_vendor} \
    --with-external-db \
    --with-lua \
    --without-selinux \
    --with-cap \
    --with-acl \
    %{?with_ndb: --with-ndb} \
    %{!?with_openmp: --disable-openmp} \
    --enable-python \
    --with-crypto=openssl

%make_build
cd python
%py3_build
cd -

%install
%make_install

# Add legacy symlink to rpm...
mkdir -p %{buildroot}/bin
ln -sr %{buildroot}/%{_bindir}/rpm %{buildroot}/bin/rpm

# We need to build with --enable-python for the self-test suite, but we
# actually package the bindings built with setup.py (#531543#c26)
rm -rf $RPM_BUILD_ROOT/%{python_sitearch}
cd python
%py3_install
cd -

# Save list of packages through cron
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/cron.daily
install -m 755 scripts/rpm.daily ${RPM_BUILD_ROOT}%{_sysconfdir}/cron.daily/rpm

mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d
install -m 644 scripts/rpm.log ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d/rpm

mkdir -p $RPM_BUILD_ROOT/var/lib/rpm
for dbi in \
	Basenames Conflictname Dirnames Group Installtid Name Obsoletename \
	Packages Providename Requirename Triggername Sha1header Sigmd5 \
	__db.001 __db.002 __db.003 __db.004 __db.005 __db.006 __db.007 \
	__db.008 __db.009
do
    touch $RPM_BUILD_ROOT/var/lib/rpm/$dbi
done

test -d doc-copy || mkdir doc-copy
rm -rf doc-copy/*
ln -f doc/manual/* doc-copy/
rm -f doc-copy/Makefile*

mkdir -p $RPM_BUILD_ROOT/var/spool/repackage

mkdir -p %{buildroot}%{rpmhome}/macros.d
install %{SOURCE1} %{buildroot}%{rpmhome}/macros.d
mkdir -p %{buildroot}%{_sysconfdir}/rpm/macros.d
cat > %{buildroot}%{_sysconfdir}/rpm/macros <<EOF
# Put your own system macros here
# usually contains

# Set this one according your locales
# %%_install_langs

EOF

# Fix up and add platform targets
cd %{buildroot}%{rpmhome}/platform

# There's a difference between *-linux and *-linux-gnux32... So got to add %%{_gnu} to target_platform
sed -i -e 's,^%%_target_platform.*,&%%{_gnu},' *-linux/macros

# We don't target pre-eabi ARM...
sed -i -e 's,-gnu$,-gnueabi,g' arm*-linux/macros
sed -i -e 's,-gnueabi$,-gnueabihf,g' arm*h*-linux/macros

# Add x32 ABI...
cp -a x86_64-linux x32-linux
sed -i -e 's,-gnu,-gnux32,g' x32-linux/macros

# Add RISC-V...
cp -a i686-linux riscv32-linux
sed -i -e 's,i386,riscv32,g;s, -march=i686,,g;s,x86,riscv,g' riscv32-linux/macros
cp -a x86_64-linux riscv64-linux
sed -i -e 's,x86_64,riscv64,g;s,x86,riscv,g' riscv64-linux/macros

# Add ARMv8 (aarch64 in 32-bit mode)
cp -a armv7hnl-linux armv8hnl-linux
sed -i -e 's,v7,v8,g' armv8hnl-linux/macros
cp -a armv7l-linux armv8l-linux
sed -i -e 's,v7,v8,g' armv8l-linux/macros

# Add ZNVER1 (Ryzen/EPYC)
cp -a x86_64-linux znver1-linux
# Overriding %_target_cpu doesn't seem to work, so we set %_target_platform
sed -i -e 's,%%{_target_cpu}-%%{_vendor},x86_64-%%{_vendor},g' znver1-linux/macros
sed -i -e '/^%%_target_platform/i%%_target_cpu		x86_64' znver1-linux/macros
sed -i -e '/^%%optflags/d' znver1-linux/macros
# And ZNVER1 in 32-bit mode...
cp -a athlon-linux znver1_32-linux
# Overriding %_target_cpu doesn't seem to work, so we set %_target_platform
sed -i -e 's,%%{_target_cpu}-%%{_vendor},i686-%%{_vendor},g' znver1_32-linux/macros
sed -i -e '/^%%_target_platform/i%%_target_cpu		i686' znver1_32-linux/macros
sed -i -e '/^%%optflags/d' znver1_32-linux/macros

# Let's create some crosscompile targets for MUSL based systems...
for arch in aarch64 armv7hl armv7hnl armv8hnl i686 x86_64 znver1 x32 riscv32 riscv64; do
	cp -a $arch-linux $arch-linuxmusl
	sed -i -e 's,-gnu,-musl,g' $arch-linuxmusl/macros
	# FIXME this is not very nice... It's a workaround for
	# not being able to set _target_os in platform macros
	sed -i -e 's,%%{_target_os},linux,g' $arch-linuxmusl/macros
done

# We may want to crosscompile to Android as well...
# Different targets here because Android doesn't use ARM32 hardfloat ABIs
for arch in aarch64 armv7l armv8l i686 x86_64 znver1 riscv32 riscv64; do
	cp -a $arch-linux $arch-android
	sed -i -e 's,-gnu,-android,g' $arch-android/macros
	# FIXME this is not very nice... It's a workaround for
	# not being able to set _target_os in platform macros
	sed -i -e 's,%%{_target_os},linux,g' $arch-android/macros
done
# FIXME this is not very nice... It's a workaround for
# not being able to set _target_cpu in platform macros
sed -i -e 's,%%{_target_cpu},x86_64,g' x32-*/macros

# And let's not force developers of cross-platform applications
# to keep a copy of Windoze around just because they want to
# compile for it...
cp -a x86_64-linux x86_64-mingw32
cp -a i686-linux i686-mingw32
sed -i -e 's,linux,mingw32,g;s,-gnu,%%{nil},g' *-mingw32/macros
sed -i -e 's,openmandriva,w64,g' x86_64-mingw32/macros
# Not a typo -- it's weird, but the correct triplet for
# Windoze 32 is actually i686-w64-mingw32, not the more
# logical i686-w32-mingw32. The -w32- vs -w64- seems to
# be only about telling the difference between the
# original mingw32 and its 64-bit capable fork.
sed -i -e 's,openmandriva,w64,g' i686-mingw32/macros
cd -

%find_lang %{name}

find $RPM_BUILD_ROOT -name "*.la" -delete

%if %{with check}
%check
# https://github.com/rpm-software-management/rpm/issues/741
eatmydata make check || (cat tests/rpmtests.log; exit 0)
%endif

%post -p <lua>
pkgs = posix.stat("/var/lib/rpm/Packages")
if not pkgs then
    os.execute("/bin/rpm --initdb")
end

%triggerun -- rpm < 1:5.4.15-45
rm -rf /usr/lib/rpm/*-mandrake-* ||:
rm -rf /usr/lib/rpm/*-%{_real_vendor}-* ||:

%define rpmattr %attr(0755, rpm, rpm)

%files -f %{name}.lang
%doc COPYING
%doc doc/manual/[a-z]*
%attr(-,rpm,rpm) /bin/rpm
%attr(0755,rpm,rpm) %{_bindir}/rpm
%attr(0755, rpm, rpm) %{_bindir}/rpm2cpio
%attr(0755, rpm, rpm) %{_bindir}/rpm2archive
%attr(0755, rpm, rpm) %{_bindir}/gendiff
%attr(0755, rpm, rpm) %{_bindir}/rpmdb
%attr(0755, rpm, rpm) %{_bindir}/rpmkeys
%attr(0755, rpm, rpm) %{_bindir}/rpmgraph
%{_bindir}/rpmquery
%{_bindir}/rpmverify

%dir %{_localstatedir}/spool/repackage
%dir %{rpmhome}
%dir /etc/rpm
%config(noreplace) /etc/rpm/macros
%dir /etc/rpm/macros.d
%attr(0755, rpm, rpm) %{rpmhome}/config.guess
%attr(0755, rpm, rpm) %{rpmhome}/config.sub
%attr(0755, rpm, rpm) %{rpmhome}/rpmdb_*
%attr(0644, rpm, rpm) %{rpmhome}/macros
%rpmhome/macros.d
%attr(0755, rpm, rpm) %{rpmhome}/mkinstalldirs
%attr(0755, rpm, rpm) %{rpmhome}/rpm.*
%attr(0644, rpm, rpm) %{rpmhome}/rpmpopt*
%attr(0644, rpm, rpm) %{rpmhome}/rpmrc
%attr(0755, rpm, rpm) %{rpmhome}/elfdeps
%attr(0755, rpm, rpm) %{rpmhome}/script.req

%rpmattr %{rpmhome}/rpm2cpio.sh
%rpmattr %{rpmhome}/tgpg

%dir %attr(   -, rpm, rpm) %{rpmhome}/fileattrs
%attr(0644, rpm, rpm) %{rpmhome}/fileattrs/*.attr

%attr(   -, rpm, rpm) %{rpmhome}/platform/

%{_mandir}/man8/rpm.8*
%{_mandir}/man8/rpmdb.8*
%{_mandir}/man8/rpmgraph.8*
%{_mandir}/man8/rpmkeys.8*
%{_mandir}/man8/rpm2cpio.8*
%{_mandir}/man8/rpm-misc.8*
%{_mandir}/man1/*.1*
%lang(fr) %{_mandir}/fr/man[18]/*.[18]*
%lang(ja) %{_mandir}/ja/man[18]/*.[18]*
%lang(ko) %{_mandir}/ko/man[18]/*.[18]*
%lang(pl) %{_mandir}/pl/man[18]/*.[18]*
%lang(ru) %{_mandir}/ru/man[18]/*.[18]*
%lang(sk) %{_mandir}/sk/man[18]/*.[18]*

%attr(0755, rpm, rpm) %dir %_localstatedir/lib/rpm

%define rpmdbattr %attr(0644, rpm, rpm) %verify(not md5 size mtime) %ghost %config(missingok,noreplace)

%rpmdbattr /var/lib/rpm/Basenames
%rpmdbattr /var/lib/rpm/Conflictname
%rpmdbattr /var/lib/rpm/__db.0*
%rpmdbattr /var/lib/rpm/Dirnames
%rpmdbattr /var/lib/rpm/Group
%rpmdbattr /var/lib/rpm/Installtid
%rpmdbattr /var/lib/rpm/Name
%rpmdbattr /var/lib/rpm/Obsoletename
%rpmdbattr /var/lib/rpm/Packages
%rpmdbattr /var/lib/rpm/Providename
%rpmdbattr /var/lib/rpm/Provideversion
%rpmdbattr /var/lib/rpm/Removetid
%rpmdbattr /var/lib/rpm/Requirename
%rpmdbattr /var/lib/rpm/Requireversion
%rpmdbattr /var/lib/rpm/Sha1header
%rpmdbattr /var/lib/rpm/Sigmd5
%rpmdbattr /var/lib/rpm/Triggername

%files -n %librpmname
%{_libdir}/librpm.so.%{libmajor}
%{_libdir}/librpm.so.%{libmajor}.*
%{_libdir}/librpmio.so.%{libmajor}
%{_libdir}/librpmio.so.%{libmajor}.*
%if %{with plugins}
%dir %{_libdir}/rpm-plugins

%files plugin-audit
%{_libdir}/rpm-plugins/audit.so

%files plugin-syslog
%{_libdir}/rpm-plugins/syslog.so

%files plugin-systemd-inhibit
%{_libdir}/rpm-plugins/systemd_inhibit.so
%{_mandir}/man8/rpm-plugin-systemd-inhibit.8*

%files plugin-ima
%{_libdir}/rpm-plugins/ima.so

%files plugin-prioreset
%{_libdir}/rpm-plugins/prioreset.so
%endif # with plugins

%files -n %librpmbuild
%{_libdir}/librpmbuild.so.%{libmajor}
%{_libdir}/librpmbuild.so.%{libmajor}.*

%files -n %librpmsign
%{_libdir}/librpmsign.so.%{libmajor}
%{_libdir}/librpmsign.so.%{libmajor}.*

%files build
%doc doc-copy/*
%rpmattr %{_bindir}/rpmbuild
%rpmattr %{_bindir}/rpmspec
%rpmattr %{_prefix}/lib/rpm/brp-*
%rpmattr %{_prefix}/lib/rpm/check-files
%rpmattr %{_prefix}/lib/rpm/debugedit
%rpmattr %{_prefix}/lib/rpm/sepdebugcrcfix
%rpmattr %{_prefix}/lib/rpm/*.prov
%rpmattr %{_prefix}/lib/rpm/find-debuginfo.sh
%rpmattr %{_prefix}/lib/rpm/find-lang.sh
%rpmattr %{_prefix}/lib/rpm/find-provides
%rpmattr %{_prefix}/lib/rpm/find-requires
%rpmattr %{_prefix}/lib/rpm/perl.req
%rpmattr %{_prefix}/lib/rpm/check-buildroot
%rpmattr %{_prefix}/lib/rpm/check-prereqs
%rpmattr %{_prefix}/lib/rpm/check-rpaths
%rpmattr %{_prefix}/lib/rpm/check-rpaths-worker
%rpmattr %{_prefix}/lib/rpm/libtooldeps.sh
%rpmattr %{_prefix}/lib/rpm/ocaml-find-provides.sh
%rpmattr %{_prefix}/lib/rpm/ocaml-find-requires.sh
%rpmattr %{_prefix}/lib/rpm/pkgconfigdeps.sh
%rpmattr %{_prefix}/lib/rpm/pythondeps.sh
%rpmattr %{_prefix}/lib/rpm/pythondistdeps.py*
%exclude %{_prefix}/lib/rpm/__pycache__
%rpmattr %{_prefix}/lib/rpm/rpmdeps

%{_mandir}/man8/rpmbuild.8*
%{_mandir}/man8/rpmdeps.8*
%{_mandir}/man8/rpmspec.8*

%files sign
%{_bindir}/rpmsign
%{_mandir}/man8/rpmsign.8*

%files -n python-%{name}
%{python3_sitearch}/%{name}/
%{python3_sitearch}/%{name}-%{version}*.egg-info

%files -n %librpmnamedevel
%{_libdir}/librp*[a-z].so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/%{name}/

%files apidocs
%doc COPYING
%doc doc/librpm/html/*

%files cron
%config(noreplace) /etc/cron.daily/rpm
%config(noreplace) /etc/logrotate.d/rpm
