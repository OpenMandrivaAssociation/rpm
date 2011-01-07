# kill of later, to workaround repsys issue
%{?!_rpmhome: %global _rpmhome /usr/lib/rpm}
%{?!_usrlibrpm: %global _usrlibrpm /usr/lib/rpm}

%bcond_with	bootstrap
%bcond_with	debug

%bcond_without	sqlite
%bcond_without	docs

#XXX: this macro is a bit awkward, better can be done!
%if %{with bootstrap}
%bcond_with	perl
%bcond_with	python
%else
%bcond_without	perl
%bcond_without	python
%endif

%bcond_with	notyet
%if %{with notyet}
%bcond_without	xar
%bcond_without	ruby
%bcond_without	js
%bcond_without	tcl
%bcond_without	embed
%else
%bcond_with	xar
%bcond_with	ruby
%bcond_with	js
%bcond_with	tcl
%bcond_with	embed
%endif

%if %{with debug}
%define	debugcflags	-g -O0
%endif

#%%include %{_sourcedir}/bootstrap.spec

%define	bdb		db51

%define libver		5.3
%define	minorver	7
%define	srcver		%{libver}.%{minorver}
#define	prereldate	20101229

%define librpmname	%mklibname rpm  %{libver}
%define librpmnamedevel	%mklibname -d rpm
%define	librpmstatic	%mklibname -d -s rpm

Summary:	The RPM package management system
Name:		rpm
Version:	%{libver}.%{minorver}
# Kill off %mkrel later, just for pushing through filter for now
Release:	%mkrel %{?prereldate:0.%{prereldate}.}2
Epoch:		1
Group:		System/Configuration/Packaging
URL:		http://rpm5.org/

# snapshot from rpm-5_3 branch: 'cvs -d :pserver:anonymous@rpm5.org:/cvs co -r rpm-5_3 rpm'
# tarball generated with './devtool tarball.xz'
Source0:	ftp://ftp.jbj.org/pub/rpm-%{libver}.x/rpm-%{srcver}.tar.xz
Source1:	bootstrap.spec
# Needed by rpmlint. Still required? If so, this file should rather be carried
# with rpmlint itself rather than requiring for rpm to carry...
Source2:	rpm-GROUPS
# These are a bit dated with a lot of redundant macros and many of them no
# of use at all anymore! Should ideally just contain the macros different
# from the default; _arch, optflags, _lib & _multilib*.
# stripping away the rest (along with os specificity) and create a resulting
# cpu-macros.tar.gz to push upstream woudl seem like a sane improvement.
Source3:	cpu-os-macros.tar.gz
# temporary workaround for segfault occuring with rpmdrake (#61658)
Patch1:		rpm-5.3.6-workaround-segfault-with-openmp.patch
# temporary workaround for #61746, uncertain about the *correct* fix for upstream
Patch2:		rpm-5.3.7-check-arch-tag-for-platform-score-if-no-match.patch
# do a quicker --rebuilddb at end of conversion
Patch3:		rpm-5.3.7-dbconvert-rebuilddb-nofsync.patch
License:	LGPLv2.1+
BuildRequires:	autoconf >= 2.57 bzip2-devel automake >= 1.8 elfutils-devel
BuildRequires:	sed >= 4.0.3 beecrypt-devel ed gettext-devel byacc
BuildRequires:	neon0.27-devel rpm-%{_target_vendor}-setup-build %{?rpmsetup_version:>= %{rpmsetup_version}}
BuildRequires:	readline-devel ncurses-devel openssl-devel
BuildRequires:	expat-devel liblzma-devel lua-devel pcre-devel
BuildRequires:	magic-devel popt-devel >= 1.15
BuildRequires:	cpuinfo-devel syck-devel keyutils-devel
BuildRequires:	libgomp-devel gnutls-devel gnupg2
# required by parts of test suite...
BuildRequires:	wget
# Should we prefer internal xar in stead? internal xar contains at least
# lzma/xz patches, what's the state of these and upstream?
# does internal xar contain any other rpm specific patches as well, or..?
%if %{with xar}
BuildRequires:	xar-devel
%endif
BuildRequires:	%{bdb}-devel
%if %{with perl}
BuildRequires:	perl-devel
%endif
%if %{with python}
BuildRequires:	python-devel
%endif
%if %{with js}
BuildRequires:	js-devel
%endif
%if %{with ruby}
BuildRequires:	ruby-devel
%endif
%if %{with tcl}
BuildRequires:	tcl
%endif
%if %{with docs}
BuildRequires:	doxygen graphviz tetex
%endif
%if %{with sqlite}
BuildRequires:	sqlite3-devel
%endif
Requires:	cpio gawk mktemp rpm-%{_target_vendor}-setup >= 1.42 update-alternatives
Requires:	%{bdb}_recover
Requires(post):	%{bdb}-utils which sed
Requires:	%{librpmname} = %{EVRD}
Requires(pre):	rpm-helper >= 0.8
Requires(pre):	coreutils
Requires(postun):rpm-helper >= 0.8

%description
RPM is a powerful command line driven package management system capable of
installing, uninstalling, verifying, querying, and updating software packages.
Each software package consists of an archive of files along with information
about the package like its version, a description, etc.

%package -n	%{librpmname}
Summary:	Libraries used by rpm
Group:		System/Libraries
# Forcing upgrades of anything else linked against it as rpmdb is incompatible
# with older versions (#61658, comment #136)
#Conflicts:	librpm < 5.3

%description -n	%{librpmname}
RPM is a powerful command line driven package management system capable of
installing, uninstalling, verifying, querying, and updating software packages.
This package contains common files to all applications based on rpm.

%package -n	%{librpmnamedevel}
Summary:	Development files for applications which will manipulate RPM packages
Group:		Development/C
Requires:	%{librpmname} = %{EVRD}
Provides:	librpm-devel = %{EVRD}
Provides:	rpm-devel = %{EVRD}
Obsoletes:	%{_lib}rpm4.4-devel

%description -n %{librpmnamedevel}
This package contains the RPM C library and header files. These
development files will simplify the process of writing programs
which manipulate RPM packages and databases and are intended to make
it easier to create graphical package managers or any other tools
that need an intimate knowledge of RPM packages in order to function.

This package should be installed if you want to develop programs that
will manipulate RPM packages and databases.

%package -n	%{librpmstatic}
Summary:	Static libraries for rpm development
Group:		Development/C
Requires:	%{librpmnamedevel} = %{EVRD}

%description -n %{librpmstatic}
Static libraries for rpm development.

%package	build
Summary:	Scripts and executable programs used to build packages
Group:		System/Configuration/Packaging
Requires:	autoconf
Requires:	automake
Requires:	file
Requires:	gcc-c++
Requires:	libtool-base
Requires:	patch >= 2.5.9-7
Requires:	make
Requires:	unzip
Requires:	elfutils
Requires:	rpm = %{EVRD}
Requires:	rpm-%{_target_vendor}-setup-build

%description	build
This package contains scripts and executable programs that are used to
build packages using RPM.

%if %{with python}
%package -n	python-rpm
Summary:	Python bindings for apps which will manipulate RPM packages
Group:		Development/Python

%description -n	python-rpm
The rpm-python package contains a module which permits applications
written in the Python programming language to use the interface
supplied by RPM (RPM Package Manager) libraries.

This package should be installed if you want to develop Python
programs that will manipulate RPM packages and databases.
%endif

%if %{with perl}
%define	perlmod	RPM
%package -n	perl-%{perlmod}
Summary:	Perl bindings for RPM
Group:		Development/Perl
Conflicts:	perl-RPM4

%description -n perl-%{perlmod}
The RPM Perl module provides an object-oriented interface to querying both
the installed RPM database as well as files on the filesystem.
%endif

%if %{with docs}
%package 	apidocs
Summary:	API documentation for RPM
Group:		Books/Computer books
BuildArch:	noarch

%description	apidocs
This package contains the RPM API documentation generated in HTML format.
%endif

%prep
%setup -q -n rpm-%{srcver}
%patch1 -p1 -b .openmp~
%patch2 -p1 -b .platform_arch~
%patch3 -p1 -b .nofsync~
mkdir -p cpu-os-macros
tar -zxf %{SOURCE3} -C cpu-os-macros

# Needed by rpmlint.
cp %{SOURCE2} GROUPS

%build
export CPPFLAGS="-DXP_UNIX=1"
%configure2_5x	--enable-nls \
		--with-pic \
%if %{with debug}
		--enable-debug \
		--with-valgrind \
%endif
		--enable-posixmutexes \
%if %{with python}
		--with-python=%{python_version} \
%if %{with embed}
		--with-pythonembed=external \
%endif
%else
		--without-python \
%endif
%if %{with perl}
		--with-perl=vendor \
%if %{with embed}
		--with-perlembed=external \
%endif
%else
		--without-perl \
%endif
%if %{with js}
		--with-js=external \
%else
		--without-js \
%endif
%if %{with ruby}
		--with-ruby=external \
%if %{with embed}
		--with-rubyembed=external \
%endif
%endif
%if %{with tcl}
		--with-tcl=external \
%endif
		--with-glob \
		--without-selinux \
%if %{with docs}
		--with-apidocs \
%endif
		--with-libelf \
		--with-popt=external \
		--with-xz=external \
		--with-bzip2=external \
		--with-lua=external \
		--with-pcre=external \
		--with-cpuinfo=external \
		--with-syck=external \
		--with-file=external \
		--with-path-magic=%{_datadir}/misc/magic.mgc \
		--with-sqlite=external \
		--with-beecrypt=external \
		--with-usecrypto=beecrypt \
		--with-keyutils=external \
		--with-neon=external \
		--enable-openmp \
%if %{with xar}
		--with-xar=%{_includedir}/xar \
%endif
		--with-db \
		--with-db-sql \
		--without-db-tools-integrated \
%if %{with sqlite}
		--with-sqlite \
%else
		--without-sqlite \
%endif
%if 0
		--with-extra-path-macros=%{_usrlibrpm}/macros.d/mandriva \
%else
		--with-extra-path-macros=%{_usrlibrpm}/platform/%%{_target}/macros:%{_usrlibrpm}/%{_target_vendor}/platform/%%{_target}/macros:%{_sysconfdir}/rpm/macros.d/*.macros:%{_usrlibrpm}/macros.d/mandriva \
%endif
		--with-vendor=mandriva \
		--enable-build-warnings
# XXX: Making ie. a --with-pre-macros option might be more aestethic and easier
# of use to others if pushed back upstream?
# For our case, this is only used to define _prefer_target_cpu before any other
# macros so that rpm knows about this for libcpuinfo when loading macros, but
# could perhaps be useful to others, ie. for defining a _target_vendor earlier,
# so that vendor specific macros to load could be defined at runtime rather
# than compile time.. Sounds convenient if LSB certification is done on a specific
# set of binaries (does it..?) wrt. Manbo Labs.
echo '#define PREMACROFILES "%{_sysconfdir}/rpm/premacros.d/*.macros"' >> config.h
%make
# TODO: incomplete, likely just a matter of adding the corresponding files to
# files section, perhaps making a noarch -doc subpackage as well?
%if %{with docs}
%make apidocs
%endif

%check
# TODO: this should rather be set by 'check' Makefile target, and fixing up
# the check suite so that we can just do 'make check'
export LD_LIBRARY_PATH=$(for d in `find -type d -name .libs|grep -v tests`; do echo -n `pwd`/$d:; done)
%if %{with perl}
make -C perl test
%endif
%if %{with js}
# XXX: run js unit tests as well?
%endif

%install
rm -rf %{buildroot}
%makeinstall_std

# XXX: why isn't this installed by 'make install'?
install -m755 scripts/symclash.* %{buildroot}%{_rpmhome}

# XXX: doubt this is of still use..? feels dirty ;p
%ifarch ppc powerpc
ln -sf ppc-%{_target_vendor}-linux %{buildroot}%{_rpmhome}/powerpc-%{_target_vendor}-linux
%endif

# Save list of packages through cron
# FIXME: will result in conflicts with parallel cooker package...
install -m755 scripts/rpm.daily -D %{buildroot}%{_sysconfdir}/cron.daily/rpm
install -m644 scripts/rpm.log -D %{buildroot}%{_sysconfdir}/logrotate.d/rpm

# TODO: I suspect that this dirty workaround shouldn't be needed
test -d doc-copy || mkdir doc-copy
rm -rf doc-copy/*
ln -f doc/manual/* doc-copy/
rm -f doc-copy/Makefile*

mkdir -p %{buildroot}/var/spool/repackage

mkdir -p %{buildroot}%{_sysconfdir}/%{name}/{pre,}macros.d

# actual usefulness of this seems rather dubious with macros.d now...
cat > %{buildroot}%{_sysconfdir}/%{name}/macros <<EOF
# Put your own system macros here
# usually contains 

# Set this one according your locales
# %%_install_langs

EOF

cat > %{buildroot}%{_sysconfdir}/%{name}/premacros.d/cpuinfo_target.macros <<EOF
# This sets which of the available architectures to prefer when building
# packages with libcpuinfo support enabled.
%%_prefer_target_cpu     x86_64 i586
EOF

# Get rid of unpackaged files
# XXX: is there any of these we might want to keep?
for f in %{py_platsitedir}/poptmodule.{a,la} %{py_platsitedir}/rpmmodule.{a,la} \
	%{_rpmhome}/{Specfile.pm,cpanflute2,cpanflute,sql.prov,sql.req,tcl.req} \
	%{_rpmhome}/{config.site,cross-build,rpmdiff.cgi} \
	%{_rpmhome}/trpm %{_bindir}/rpmdiff; do
	rm -f %{buildroot}$f
done

%find_lang %{name}

%define	rpmdbattr %attr(0644, rpm, rpm) %verify(not md5 size mtime) %ghost %config(missingok,noreplace)
mkdir -p %{buildroot}/var/lib/rpm/{log,tmp}
for dbi in `./rpm --macros macros/macros --eval %_dbi_tags_4|tr : ' '` Seqno; do
    touch %{buildroot}/var/lib/rpm/$dbi
    echo "%rpmdbattr /var/lib/rpm/$dbi" >> %{name}.lang
done
for i in {0..9}; do
    touch %{buildroot}/var/lib/rpm/__db.00$i
    echo "%rpmdbattr /var/lib/rpm/__db.00$i" >> %{name}.lang
done

install -m755 find-provides find-requires %{buildroot}/%{_rpmhome}
install -d %{buildroot}/bin
# FIXME: considering that most libraries dynamically linked against is located
# in /usr/lib*, this doesn't make much sense unless we either statically link
# against them (Ark Linux actually does this) or move the libraries to /lib*,
# neither being very attractive options, not to mention maintenance headaches
# spread across these library packages...
# So moving rpm back to /usr/bin probably makes the most sense...
# An optional, "minimal" rpm-static package with /bin/rpm could perhaps be done
# if anyone expresses actual interest in this...
mv %{buildroot}%{_bindir}/rpm %{buildroot}/bin/rpm

cp -r cpu-os-macros %{buildroot}%{_usrlibrpm}/platform
install -d %{buildroot}%{_docdir}/rpm
cp -r apidocs/html %{buildroot}%{_docdir}/rpm

%pre
# XXX: really sceptical about rpm actually requiring or even using it's own
# dedicated user for any purpose (and there's no suid/guid no binaries either), really
# smells like an old suid/guid relic of the past...
/usr/share/rpm-helper/add-user rpm $1 rpm /var/lib/rpm /bin/false

%post
if [ $1 -eq 1 ]; then
	touch /var/lib/rpm/.NOCONVERSION
else
	rm -f /var/lib/rpm/.NOCONVERSION
fi

%posttrans
# This script will check whether the database is converted or not, if not,
# it will convert it
if [ -f /var/lib/rpm/.NOCONVERSION ]; then
	echo "Won't invoke db conversion now as this doesn't seem to be an upgrade."
	echo "After all transactions has finished, please run %{_rpmhome}/dbconvert.sh"
else
	DBREBUILD=1 DBVERBOSE=0 %{_rpmhome}/dbconvert.sh
fi

%postun
/usr/share/rpm-helper/del-user rpm $1 rpm

%clean
# TODO: I *really* want for clean section to be implicit, ie. missing clean
# should be threated as below, in stead now you need to add this section which
# by default is a macro doing the same. Better behavior would be if an empty
# clean section would override the (desired) implicit clean macro to an empty
# one in stead which would be more intuitive/closer to "commonly"(?) expected
# behavior.
# the clean section can also be skipped by passing the appropriate argument
# to rpm which would be the more "correct" thing to do rather than commenting
# it out which many do and that is what I suspect might be related to the
# behavior currently implemented. (IIRC blame/discuss with cAos linux/michael
# jennings?)
rm -rf %{buildroot}

# TODO: review which files goes into what packages...?
%files -f %{name}.lang
%doc GROUPS CHANGES doc/manual/[a-z]*
%exclude %{_docdir}/rpm/html
# Are these attributes actually still sane? Smells deprecated/legacy...
%defattr(755, rpm, rpm, 755)
/bin/rpm
%{_bindir}/rpmconstant*
%{_bindir}/rpm2cpio*
#%{_rpmhome}/bin/grep
%{_rpmhome}/bin/mtree
%{_rpmhome}/bin/rpmspecdump
%{_rpmhome}/dbconvert.sh
%{_rpmhome}/rpm.*
%{_rpmhome}/rpm2cpio
%{_rpmhome}/rpmdb_loadcvt
%{_rpmhome}/tgpg

%dir %{_localstatedir}/lib/rpm
%dir %{_localstatedir}/lib/rpm/log
%dir %{_localstatedir}/lib/rpm/tmp


%defattr(0644, rpm, rpm, 755)
%{_rpmhome}/macros.d/*
%{_rpmhome}/cpuinfo.yaml
%{_rpmhome}/macros
%{_rpmhome}/rpmpopt
%{_rpmhome}/platform/*/macros
%config(noreplace) /var/lib/rpm/DB_CONFIG

%defattr(-,root,root)
%dir %{_localstatedir}/spool/repackage
%dir %{_rpmhome}
%dir %{_rpmhome}/bin
%dir %{_rpmhome}/platform/
%dir %{_rpmhome}/platform/*/
%dir %{_rpmhome}/macros.d
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/macros
%dir %{_sysconfdir}/%{name}/macros.d
%dir %{_sysconfdir}/%{name}/premacros.d
%{_sysconfdir}/%{name}/premacros.d/*

%{_mandir}/man[18]/*.[18]*
%lang(pl)	%{_mandir}/pl/man[18]/*.[18]*
%lang(ru)	%{_mandir}/ru/man[18]/*.[18]*
%lang(ja)	%{_mandir}/ja/man[18]/*.[18]*
%lang(sk)	%{_mandir}/sk/man[18]/*.[18]*
%lang(fr)	%{_mandir}/fr/man[18]/*.[18]*
%lang(ko)	%{_mandir}/ko/man[18]/*.[18]*
%exclude	%{_mandir}/man8/rpmbuild.8*
%exclude	%{_mandir}/man8/rpmdeps.8*

%config(noreplace,missingok)	/etc/cron.daily/rpm
%config(noreplace,missingok)	/etc/logrotate.d/rpm


%files build
%defattr(-,root,root)
%doc		CHANGES
%doc		doc-copy/*
%defattr(755, rpm, rpm)
%{_bindir}/gendiff
%{_bindir}/rpmbuild
%{_rpmhome}/bin/abi-compliance-checker.pl
%{_rpmhome}/bin/api-sanity-autotest.pl
%{_rpmhome}/bin/chroot
%{_rpmhome}/bin/cp
%{_rpmhome}/bin/dbsql
%{_rpmhome}/bin/debugedit
%{_rpmhome}/bin/find
%{_rpmhome}/bin/install-sh
%{_rpmhome}/bin/mkinstalldirs
%{_rpmhome}/bin/rpmcache
%{_rpmhome}/bin/rpmcmp
%{_rpmhome}/bin/rpmdeps
%{_rpmhome}/bin/rpmdigest
%{_rpmhome}/bin/rpmkey
%{_rpmhome}/bin/rpmrepo
%{_rpmhome}/bin/sqlite3
%if %{with xar}
%{_rpmhome}/bin/txar
%endif
%{_rpmhome}/bin/wget
%dir %{_rpmhome}/helpers
%{_rpmhome}/helpers/*
%dir %{_rpmhome}/qf
%{_rpmhome}/qf/*
%{_rpmhome}/vcheck
%{_rpmhome}/brp-*
%{_rpmhome}/check-files
#%%{_rpmhome}/cross-build
%{_rpmhome}/find-debuginfo.sh
%{_rpmhome}/find-lang.sh
%{_rpmhome}/find-prov.pl
%{_rpmhome}/find-provides
%{_rpmhome}/find-provides.perl
%{_rpmhome}/find-req.pl
%{_rpmhome}/find-requires
%{_rpmhome}/find-requires.perl
%{_rpmhome}/gem_helper.rb
%{_rpmhome}/getpo.sh
%{_rpmhome}/http.req
%{_rpmhome}/javadeps.sh
%{_rpmhome}/mono-find-provides
%{_rpmhome}/mono-find-requires
%{_rpmhome}/executabledeps.sh
%{_rpmhome}/libtooldeps.sh
%{_rpmhome}/osgideps.pl
%{_rpmhome}/perldeps.pl
%{_rpmhome}/perl.prov
%{_rpmhome}/perl.req
%{_rpmhome}/php.prov
%{_rpmhome}/php.req
%{_rpmhome}/pkgconfigdeps.sh
%{_rpmhome}/pythondeps.sh

%{_rpmhome}/symclash.*
%{_rpmhome}/u_pkg.sh
%{_rpmhome}/vpkg-provides.sh
%{_rpmhome}/vpkg-provides2.sh

%if %{with js}
%{_rpmhome}/bin/tjs
%endif
%attr(0644, rpm, rpm) %{_rpmhome}/macros.rpmbuild
%defattr(-, root, root)
%{_mandir}/man8/rpmbuild.8*
%{_mandir}/man8/rpmdeps.8*

%files -n %{librpmname}
%defattr(-,root,root)
%{_libdir}/librpm-%{libver}.so
%{_libdir}/librpmconstant-%{libver}.so
%{_libdir}/librpmdb-%{libver}.so
%{_libdir}/librpmio-%{libver}.so
%{_libdir}/librpmmisc-%{libver}.so
%{_libdir}/librpmbuild-%{libver}.so
%if %{with js}
#FIXME: lib64! why not just place in _libdir?
# at least this one is(/seems to be(?)) a "regular" & "unique" (without risk of
# any conflicts) shared library with "normal" soname, libtool versioning and all...
%{_rpmhome}/lib/librpmjsm.so.*
%{_rpmhome}/lib/rpmjsm.so
%endif
#%if %{with sqlite}
#%{_rpmhome}/libsql*.so.*
#%endif

%files -n %{librpmnamedevel}
%defattr(-,root,root)
#%doc apidocs/html
%{_includedir}/rpm
%{_libdir}/librpm.la
%{_libdir}/librpm.so
%{_libdir}/librpmconstant.la
%{_libdir}/librpmconstant.so
%{_libdir}/librpmdb.la
%{_libdir}/librpmdb.so
%{_libdir}/librpmio.la
%{_libdir}/librpmio.so
%{_libdir}/librpmmisc.la
%{_libdir}/librpmmisc.so
%{_libdir}/librpmbuild.la
%{_libdir}/librpmbuild.so
%{_libdir}/pkgconfig/rpm.pc

%if %{with js}
#FIXME: lib64!
%{_rpmhome}/lib/librpmjsm.la
%{_rpmhome}/lib/librpmjsm.so
%{_rpmhome}/lib/rpmjsm.la
%endif
%if %{with python}
# I *really* don't think rpm should have libtool create this one...
%{py_platsitedir}/rpm/*.la
%endif
#%if %{with sqlite}
#%{_rpmhome}/libsql*.la
#%{_rpmhome}/libsql*.so
#%endif


%files -n %{librpmstatic}
%defattr(-,root,root)
%{_libdir}/librpm.a
%{_libdir}/librpmconstant.a
%{_libdir}/librpmdb.a
%{_libdir}/librpmio.a
%{_libdir}/librpmmisc.a
%{_libdir}/librpmbuild.a

%if %{with js}
#FIXME: lib64!
%{_rpmhome}/lib/librpmjsm.a
%{_rpmhome}/lib/rpmjsm.a
%endif
%if %{with python}
# generate static library for python module..? prolly' not...
%{py_platsitedir}/rpm/*.a
%endif
#%if %{with sqlite}
#%{_rpmhome}/libsql*.a
#%endif

%if %{with perl}
%files -n perl-%{perlmod}
%defattr(-,root,root)
#%doc perl/Changes
%{_mandir}/man3/RPM*
%{perl_vendorarch}/%{perlmod}.pm
%dir %{perl_vendorarch}/%{perlmod}
%{perl_vendorarch}/%{perlmod}/*.pm
%{perl_vendorarch}/auto/%{perlmod}
%endif

%if %{with python}
%files -n python-rpm
%defattr(-,root,root)
%dir %{py_platsitedir}/rpm
%{py_platsitedir}/rpm/*.py
%{py_platsitedir}/rpm/*.so
%endif

%if %{with docs}
%files apidocs
%dir %{_docdir}/rpm/html
%{_docdir}/rpm/html/*
%endif
