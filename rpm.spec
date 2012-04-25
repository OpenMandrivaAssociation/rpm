%bcond_with	bootstrap
%bcond_with	debug

%bcond_without	ossp-uuid
%bcond_without	augeas

#XXX: this macro is a bit awkward, better can be done!
%if %{with bootstrap}
%bcond_with	perl
%bcond_with	python
%bcond_with	tcl
%bcond_with	squirrel
%bcond_with	embed
%bcond_with	docs
%bcond_with	sqlite
%else
%bcond_without	perl
%bcond_without	python
%bcond_without	tcl
%bcond_without	squirrel
%bcond_without	embed
%bcond_without	docs
# use what's in berkeley db
%bcond_with	sqlite
%endif

%bcond_with	notyet
%if %{with notyet}
%bcond_without	xar
%bcond_without	ruby
%bcond_without	js
%else
%bcond_with	xar
%bcond_with	ruby
%bcond_with	js
%endif

%if %{with debug}
%global	debugcflags	%{debugcflags} -g3 -O0
%endif

#include %%{_sourcedir}/bootstrap.spec

%define	bdb		db52

%define libver		5.4
%define	minorver	8
%define	srcver		%{libver}.%{minorver}
#define	prereldate	20110712

%define librpmname	%mklibname rpm %{libver}
%define librpmnamedevel	%mklibname -d rpm
%define	librpmstatic	%mklibname -d -s rpm

Summary:	The RPM package management system
Name:		rpm
Epoch:		1
Version:	%{libver}.%{minorver}
Release:	%{?prereldate:0.%{prereldate}.}1
License:	LGPLv2.1+
Group:		System/Configuration/Packaging
URL:		http://rpm5.org/
# snapshot from rpm-5_4 branch: 'cvs -d :pserver:anonymous@rpm5.org:/cvs co -r rpm-5_4 rpm'
# tarball generated with './devtool tarball.xz'
Source0:	ftp://ftp.jbj.org/pub/rpm-%{libver}.x/%{name}-%{srcver}.tar.gz
#Source1:	bootstrap.spec
# These are a bit dated with a lot of redundant macros and many of them no
# of use at all anymore! Should ideally just contain the macros different
# from the default; _arch, optflags, _lib & _multilib*.
# stripping away the rest (along with os specificity) and create a resulting
# cpu-macros.tar.gz to push upstream would seem like a sane improvement.
Source2:	rpm.rpmlintrc
Source3:	cpu-os-macros.tar.gz
Source4:	legacy_compat.macros
# already merged upstream
Patch0:		rpm-5.3.8-set-default-bdb-log-dir.patch
# TODO: should be disable for cooker, packaging needs to be fixed (enable for legacy compatibility)
Patch1:		rpm-5.3.8-dependency-whiteout.patch
# TODO: make conditional & disabled through macro by default (enable for legacy compatibility)
Patch2:		rpm-5.3.8-non-pre-scripts-dont-fail.patch
Patch3:		rpm-5.3.8-no-doc-conflicts.patch
# if distsuffix is defined, use it for disttag (from Anssi)
Patch4:		rpm-5.3.8-disttag-distsuffix-fallback.patch
# ugly hack to workaround disttag/distepoch pattern matching issue to buy some
# time to come up with better pattern fix..
Patch5:		rpm-5.3.8-distepoch-pattern-hack.patch
# fixes a typo in russian translation (#62333)
Patch11:	rpm-5.3.8-fix-russian-typo.patch
# temporary workaround for issues with file triggers firing multiple times and
# a huge memleak...
Patch15:	rpm-5.3.8-fire-file-triggers-only-once.patch
Patch19:	rpm-5.3.10-doxygen-1.7.4-bug.patch
Patch20:	rpm-5.3.11-fix-syslog-b0rkage.patch
Patch21:	rpm-5.3.12-change-dep-loop-errors-to-warnings.patch
Patch22:	rpm-5.3.12-55810-rpmevrcmp-again-grf.patch
Patch28:	rpm-5.4.4-merge-find-lang.sh-changes-from-rpm.org.patch
Patch29:	rpm-5.4.4-add-_specfile-macro.patch
Patch30:	rpm-5.4.4-fix-rpm-qf-on-non-packaged-files.patch
Patch31:	rpm-5.4.4-fix-rpm_qa-pattern.patch
# uhm.. broken?
Patch32:	rpm-5.4.4-really-always-invoke-clean-at-end.patch
Patch33:	rpm-5.4.4-fix-mdvbz62979.patch
# This patch adds support for untangling dependency loops with prioritized removal
# of dependencies from loops. It's very crude for now and certainly needs some obvious
# improvement, but it'll fix the most common scenario giving issues where ie.
# Requires(post) has been used and shouldn't introduce any regressions..
# REF: http://rpm5.org/community/rpm-devel/4633.html
Patch34:	rpm-5.4.4-use-dependency-type-for-ordering.patch
Patch35:	rpm-5.4.4-find_lang-with-html.patch
Patch36:	rpm-5.4.4-find_lang-support-multiple-names.patch
Patch37:	rpm-5.4.5-avoid-dependencies-on-self.patch
Patch38:	rpm-5.4.4-find_lang-handle-man-pages-already-compressed.patch
Patch39:	rpm-5.4.4-find-debuginfo-drop-useless-sort.patch
Patch40:	rpm-5.4.4-pkgconfigdeps-check-path.patch
Patch41:	rpm-5.4.4-merge-manbo-macros.patch
Patch42:	rpm-5.4.4-glob-wildcards-for-loading-macro-files.patch
Patch43:	rpm-5.4.4-merge-common-rpm-mandriva-setup-macros.patch
Patch44:	rpm-5.4.4-use-xz-payload.patch
Patch45:	rpm-5.4.4-merge-rpm-mandriva-setup-build-macros.patch
Patch46:	rpm-5.4.4-allow-installation-of-repackaged-rpms.patch
Patch47:	rpm-5.4.4-fix-removal-of-overlapping-dependencies.patch
Patch48:	rpm-5.4.8-dont-show-suggests-with-requires.patch
# syncing debugedit commits from rpm.org
Patch49:	rpm-5.4.4-debugedit-whitespace-fixups.patch
Patch50:	rpm-5.4.4-debugedit-recompute-build-id-only-on-dwarf-change.patch
Patch51:	rpm-5.4.4-debugedit-fix-incorrect-error-messages-regarding_-b-and_-d.patch
Patch52:	rpm-5.4.4-debugedit-remove-unused-variable.patch
Patch53:	rpm-5.4.4-debugedit-bail-out-of-debuginfo-if-stabs-format-encountered.patch
Patch54:	rpm-5.4.4-debugedit-add-dwarf4-support.patch
# backport from HEAD
Patch55:	rpm-5.4.4-find-debuginfo-strip-reloc-debug-sections.patch
Patch56:	rpm-5.4.4-fix-scripts-breaking-when-RPM_BUILD_ROOT-contains-spaces.patch
Patch57:	rpm-5.4.4-create-gdb-index-from-find-debuginfo-if-possible.patch
Patch58:	rpm-5.4.4-use-dwarf4-debug-format.patch
Patch59:	rpm-5.4.4-compress-debug-sections.patch
Patch60:	rpm-5.4.4-find-debuginfo-add-missing-partial-strip.patch
Patch61:	rpm-5.4.4-fix-same-package-with-epoch-possible-to-upgrade.patch
Patch62:	rpm-5.4.4-fix-_sys_macros_dir-path.patch
Patch63:	rpm-5.4.4-strip-buildroot-away-from-duplicate-files-list.patch
Patch64:	rpm-5.4.4-duplicate_files_terminate_build.patch
Patch65:	rpm-5.4.4-unpackaged_subdirs_terminate_build.patch
# mdvbz#64898
Patch66:	rpm-5.4.4-rpmbuild-withoutclean.patch
Patch67:	rpm-5.4.4-find-debuginfo-avoid-excessive-output-from-eu-strip.patch
# mdvbz#64914
Patch68:	rpm-5.4.4-enable-rpmgio-net-transport.patch
# no sense in having an additional dependency on 'pkgconfig' on all packages that
# have a pkgconfig file, it's not needed for them to be made useful and anything
# actuallly using pkgconfig for this purpose will pull it in as a dependency anyways...
Patch69:	rpm-5.4.4-drop-useless-auto-generated-pkgconfig-dependency.patch
# drop dependencies such as /bin/sh which will always be satisfied by glibc's dependency on
# bash, and also on /sbin/ldconfig which always will be satisfied by glibc
Patch70:	rpm-5.4.4-drop-base-dependencies.patch
Patch71:	rpm-5.4.4-fix-rpmconstant-to-always-use-LC_CTYPE-C-for-case-conversion.patch
# from rpm.org
Patch72:	rpm-5.4.4-debugedit-recognize-debug_macro-section.patch
# from rpm.org
Patch73:	rpm-5.4.4-add-_build_pkgcheck.patch
# $RPM_BUILD_DIR isn't necessarily the same as $PWD, it's %%{_builddir}, not
# %%{_builddir}/%%{?buildsubdir}, messing up paths in debug packages created..
Patch74:	rpm-5.4.4-pass-_builddir-properly-to-find-debuginfo.patch
Patch75:	rpm-5.4.4-srcdefattr.patch
Patch76:	rpm-5.4.4-files-listed-twice-terminates-build.patch
Patch77:	rpm-5.4.7-use-bdb-5.2.patch
Patch78:	rpm-5.4.4-ruby1.9-fixes.patch
# mdvbz#65269
Patch79:	rpm-5.4.4-dont-consider-ranged-dependencies-as-overlapping-for-removal.patch
Patch81:	rpm-5.4.5-libsql-conditional.patch
Patch83:	rpm-5.4.5-kmod-deps-xz-support.patch
Patch84:	rpm-5.4.5-enable-internal-dependency-generator.patch
Patch85:	rpm-5.4.5-fix-removal-of-overlapping-dependencies-for-internal-dependency-generator.patch
# this updates to using the dependency generator shipped with mono, it has some
# issues which makes me cautious about actually merging it with rpm5 upstream,
# but we'll anyways use it as is for now to prevent any potential regressions
# by switching to the internal dependency generator
Patch86:	rpm-5.4.5-update-mono-dependency-generator.patch
Patch87:	rpm-5.4.5-dont-generate-php-dependencies-only-when-executable.patch
Patch88:	rpm-5.4.5-patchset_16004.patch
Patch89:	rpm-5.4.5-patchset_16005.patch
Patch90:	rpm-5.4.5-patchset_16022.patch
Patch91:	rpm-5.4.5-update-rpmfc-when-removing-dependencies-on-self.patch
Patch92:	rpm-5.4.5-rpmfc-extract-dependencies-for-all-files.patch
Patch93:	rpm-5.4.5-rubygems-add-missing-newline.patch
Patch94:	rpm-5.4.5-generate-haskell-dependencies.patch
Patch95:	rpm-5.4.5-drop-some-interpreter-deps.patch
Patch96:	rpm-5.4.5-fix-elf-interpreter-resolving-breaking-uclibc-deps.patch
Patch97:	rpm-5.4.5-set-proper-file-color-for-scripts-using-env-in-shellbang.patch
Patch98:	rpm-5.4.5-update-rpmfc-when-removing-overlapping-dependencies.patch
Patch99:	rpm-5.4.5-python-export-spec-macros.patch
Patch100:	rpm-5.4.5-do-not-merge-script-dependencies-with-non-script-dependencies.patch
Patch101:	rpm-5.4.5-font-provides.patch
Patch102:	rpm-5.4.7-kmod-dependencies.patch
Patch103:	rpm-5.4.5-desktop-provides.patch
Patch104:	rpm-5.4.5-skip-dependencies-for-character-devices.patch
Patch105:	rpm-5.4.5-rpmfc-use-strlen-not-sizeof.patch
Patch106:	rpm-5.4.5-break-out-of-elf-link-loop.patch
Patch107:	rpm-5.4.5-rpmfc-apply-python-coloring-from-magic.patch
Patch108:	rpm-5.4.5-fix-pythonegg-deps-for-egg-metadata-in-directories.patch
Patch109:	rpm-5.4.5-fix-generation-of-uclibc-deps-on-non-lib64.patch
Patch110:	rpm-5.4.7-only-generate-devel-deps-for-symlinks-start-with-lib.patch
Patch111:	rpm-5.4.7-keep-loading-script-macros.patch
Patch112:	rpm-5.4.7-use-gnu-hash-style-by-default-and-drop-rtld-dep.patch
Patch113:	rpm-5.4.8-add-distepoch-rpmlib-feature.patch
Patch114:	rpm-5.4.7-dont-add-versioneddependency-rpmlib-feature-dependency.patch
Patch115:	rpm-5.4.7-rpmfc-fix-invalid-free-if-not-_defaultdocdir-set.patch
Patch116:	rpm-5.4.7-dont-try-generate-rpmfc-dependencies-from-doc-files.patch
Patch117:	rpm-5.4.7-only-generate-ruby-and-python-deps-for-executables-and-modules.patch
Patch118:	rpm-5.4.7-dont-generate-soname-provides-for-dsos-with-no-soname.patch
Patch119:	rpm-5.4.7-fix-generation-of-ruby-abi-provides.patch
Patch120:	rpm-5.4.7-print-name-of-files-removed-dependencies-are-generated-from.patch
Patch121:	rpm-5.4.7-always-choose-equal-only-deps-when-overlapping.patch
Patch122:	rpm-5.4.7-rpmfc-strdup-EVR-in-overlap-removal.patch
Patch123:	rpm-5.4.7-rpmds-dont-try-fopen-empty-filenames.patch
Patch124:	rpm-5.4.7-change-to-debuginfo-suffix.patch
# crash reproducable with 'rpm -qa --triggers'
Patch125:	rpm-5.4.7-hdrfmt-fix-unitialized-argv-element.patch
Patch126:	rpm-5.4.7-add-filetriggers-regex-matching-support.patch
Patch127:	rpm-5.4.7-add-matches-as-arguments-to-triggers.patch
Patch128:	rpm-5.4.7-dont-consider-trigger-dependencies-as-overlapping.patch
Patch129:	rpm-5.4.7-fix-minor-memleaks.patch
Patch130:	rpm-5.4.7-mire-fix-strings-lacking-null-terminator.patch
Patch131:	rpm-5.4.8-dlopen-embedded-interpreters.patch
Patch132:	rpm-5.4.7-rpmpython-fix-input.patch
Patch133:	rpm-5.4.7-generate-devel-provides-outside-of-libdirs.patch
Patch134:	rpm-5.4.7-actually-perform-linking-against-internal-lua.patch
Patch135:	rpm-5.4.7-no-seqid_init-on-rdonly-database.patch
Patch136:	rpm-5.4.7-add-support-for-using-rpmdsMerge-with-filepath-tags.patch
Patch137:	rpm-5.4.7-avoid-double-slash-in-path-for-dirname-filetrigger-matching.patch
Patch138:	rpm-5.4.7-trigtrans.patch
Patch139:	rpm-5.3.12-fix-verify-segfault.patch
Patch140:	rpm-5.4.7-rpmv3-support.patch
Patch141:	rpm-5.4.7-revert-hash-instead-of-truncation.patch
# MD rediffed from upstream
Patch142:	rpm-5.4.7_typelib.patch
Patch143:	rpm-5.4.7-mono-find-requires-strip-newlines.patch
Patch144:	rpm-5.4.8-URPM-build-fix.patch

BuildRequires:	autoconf >= 2.57
BuildRequires:	bzip2-devel
BuildRequires:	automake >= 1.8
BuildRequires:	elfutils-devel
BuildRequires:	sed >= 4.0.3
BuildRequires:	beecrypt-devel >= 4.2.1-8
BuildRequires:	ed
BuildRequires:	gettext-devel
BuildRequires:	byacc
BuildRequires:	pkgconfig(neon)
BuildRequires:	rpm-%{_target_vendor}-setup-build
BuildRequires:	readline-devel
BuildRequires:	ncurses-devel
BuildRequires:	pkgconfig(libssl)
BuildRequires:	pkgconfig(libcrypto)
BuildRequires:	pkgconfig(liblzma)
BuildRequires:	pkgconfig(libpcre)
BuildRequires:	pkgconfig(libpcreposix)
BuildRequires:	acl-devel
BuildRequires:	magic-devel
BuildRequires:	pkgconfig(popt) >= 1.15
BuildRequires:	libxml2-devel >= 2.7.8-9
# we're now building with internal..
#BuildRequires:	pkgconfig(lua)
# needed by internal lua
BuildRequires:	expat-devel
%ifarch %{ix86} x86_64 ppc ppc64 ia64
BuildRequires:	pkgconfig(libcpuinfo) 
%endif
BuildRequires:	syck-devel
BuildRequires:	keyutils-devel
BuildRequires:	gomp-devel
BuildRequires:	pkgconfig(gnutls)
BuildRequires:	gnupg2
# required by parts of test suite...
BuildRequires:	wget
# Should we prefer internal xar in stead? internal xar contains at least
# lzma/xz patches, what's the state of these and upstream?
# does internal xar contain any other rpm specific patches as well, or..?
%if %{with xar}
BuildRequires:	xar-devel
%endif
BuildRequires:	%{bdb}-devel >= 5.2.36-3
# required by test suite
BuildRequires:	%{bdb}-utils
%if %{with perl}
BuildRequires:	perl-devel
%endif
%if %{with python}
BuildRequires:	python-devel
%endif
%if %{with js}
BuildRequires:	pkgconfig(mozjs185)
%endif
%if %{with ruby}
BuildRequires:	ruby-devel
%endif
%if %{with tcl}
BuildRequires:	tcl-devel
%endif
%if %{with squirrel}
BuildRequires:	squirrel-devel
%endif
%if %{with docs}
BuildRequires:	doxygen
BuildRequires:	graphviz
BuildRequires:	texlive
%endif
%if %{with sqlite}
BuildRequires:	pkgconfig(sqlite3)
%endif
%if %{with ossp-uuid}
BuildRequires:	pkgconfig(ossp-uuid)
%endif
%if %{with augeas}
BuildRequires:	pkgconfig(augeas)
%endif
BuildRequires:	spec-helper >= 0.31.12
BuildRequires:	stdc++-static-devel >= 4.6.2-8
BuildRequires:	elfutils >= 0.153
BuildRequires:	libtool >= 2.4.2-3
Requires:	cpio
Requires:	gawk
Requires:	mktemp
Requires:	update-alternatives
Requires:	%{bdb}_recover
Suggests:	%{bdb}-utils
Requires:	%{librpmname} = %{EVRD}
Conflicts:	rpm-build < 1:5.3.10-0.20110422.3
Requires(pre):	coreutils
%rename		rpmconstant
%rename		multiarch-utils
%rename		rpm-manbo-setup
%rename		rpm-%{_target_vendor}-setup
Obsoletes:	haskell-macros < 6.4-5

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
Conflicts:	librpm < 5.3
Conflicts:	%{_lib}db5.1 < 5.1.25
Conflicts:	%{_lib}elfutils1 < 0.152
Conflicts:	%{_lib}beecrypt7 < 4.2.1

%description -n	%{librpmname}
RPM is a powerful command line driven package management system capable of
installing, uninstalling, verifying, querying, and updating software packages.
This package contains common files to all applications based on rpm.

%package -n	%{librpmnamedevel}
Summary:	Development files for applications which will manipulate RPM packages
Group:		Development/C
Requires:	%{librpmname} = %{EVRD}
Provides:	rpm-devel = %{EVRD}
%rename		%{_lib}rpmconstant-devel
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
Requires:	libtool-base >= 2.4.2-3
Requires:	patch >= 2.5.9-7
Requires:	make
Requires:	unzip
Requires:	elfutils >= 0.152-4
Requires:	rpm = %{EVRD}
Requires:	rpm-%{_target_vendor}-setup-build
Requires:	spec-helper >= 0.31.12
Requires:	rpmlint-%{_target_vendor}-policy >= 0.3.2
Requires:	python-rpm = %{EVRD}
Requires:	perl-RPM = %{EVRD}
Conflicts:	rpmlint < 1.4-4
Conflicts:	multiarch-utils < 1:5.3.10
Conflicts:	rpm < 1:5.4.4-32
Obsoletes:	rpm5-manbo-setup
%rename		rpm-manbo-setup-build

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
Obsoletes:	perl-RPM4
Requires:	perl-IO-String

%description -n perl-%{perlmod}
The RPM Perl module provides an object-oriented interface to querying both
the installed RPM database as well as files on the filesystem.
%endif

%if %{with ruby}
%package -n	rpm-rubyembed
Summary:	Ruby embedding module for rpm
Group:		Development/Ruby
Requires:	ruby(abi)

%description -n rpm-rubyembed
This package provides embedded ruby interpreter support for RPM.
%endif

%if %{with tcl}
%package -n	rpm-tclembed
Summary:	Tcl embedding module for rpm
Group:		Development/Other
Requires:	tcl

%description -n rpm-tclembed
This package provides embedded Tcl interpreter support for RPM.
%endif

%if %{with squirrel}
%package -n	rpm-squirrelembed
Summary:	Squirrel embedding module for rpm
Group:		Development/Other
Requires:	squirrel

%description -n rpm-squirrelembed
This package provides embedded Squirrel interpreter support for RPM.
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
%setup -q
%patch111 -p1 -b .script_macros~
# These patches has been commited hastily upstream for review,
# keeping them around here for now untill finished...
%if 0
%patch0 -p1 -b .set_lg_dir~
%patch1 -p1 -b .dep_whiteout~
%endif
%patch2 -p1 -b .scriptlet~
%patch3 -p1 -b .doc_conflicts~
%patch11 -p1 -b .ru~
%if 0
%patch4 -p1 -b .distsuffix~
%patch5 -p1 -b .distpatt~
%patch15 -p1 -b .trigger_once~
%endif
%patch19 -p1 -b .doxygen~
%patch20 -p1 -b .syslog~
#%%patch21 -p1 -b .loop_warnings~
#%%patch22 -p1 -b .55810~
#patch27 -p1 -b .mdv~
%patch28 -p1 -b .rpmorg~
%patch29 -p1 -b .specfile~
%patch30 -p1 -b .qf_non~
%patch31 -p1 -b .rpm_qa~
#%%patch32 -p1 -b .clean~
%patch33 -p1 -b .mdvbz62979~
%patch34 -p1 -b .ordering~
%patch35 -p1 -b .html~
%patch36 -p1 -b .multi~
%patch37 -p1 -b .drop_deps~
%patch38 -p1 -b .man_comp~
%patch39 -p1 -b .no_sort~
%patch40 -p1 -b .pc_paths~
%patch41 -p1 -b .manbo~
%patch42 -p1 -b .glob~
%patch43 -p1 -b .common~
%patch44 -p1 -b .payload~
%patch45 -p1 -b .build~
%patch46 -p1 -b .repackage~
%patch47 -p1 -b .overlap~
%patch48 -p1 -b .suggests~
%patch49 -p1 -b .debugedit_whitespace~
%patch50 -p1 -b .debugedit_recompute~
%patch51 -p1 -b .debugedit_errormsgs~
%patch52 -p1 -b .debugedit_unused_var~
%patch53 -p1 -b .debugedit_stabs_fail~
%patch54 -p1 -b .debugedit_dwarf4~
%patch55 -p1 -b .strip_reloc_debug~
%patch56 -p1 -b .quotes~
%patch57 -p1 -b .gdb_index~
%patch58 -p1 -b .dwarf4~
%patch59 -p1 -b .compress_debug~
%patch60 -p1 -b .partial_strip~
%patch61 -p1 -b .epoch_cmp~
%patch62 -p1 -b ._sys_macros_dir~
%patch63 -p1 -b .buildroot_dups~
%patch64 -p1 -b .dups_terminate~
%patch65 -p1 -b .subdir_terminate~
%patch66 -p1 -b .withoutclean~
%patch67 -p1 -b .strip_silent~
%patch68 -p1 -b .rpmgio_ufdio~
%patch69 -p1 -b .oneshot~
%patch70 -p1 -b .drop_basedeps~
%patch71 -p1 -b .locale~
%patch72 -p1 -b .debug_macro~
%patch73 -p1 -b .pkgcheck~
%patch74 -p1 -b .builddir~
%patch75 -p1 -b .srcdefattr~
%patch76 -p1 -b .twice_terminate~
%patch77 -p1 -b .db52~
%patch78 -p1 -b .ruby19~
%patch79 -p1 -b .range_nooverlap~
#patch81 -p1 -b .libsql~
%patch83 -p1 -b .kmod_xz~
%patch84 -p1 -b .int_dep_gen~
%patch85 -p1 -b .int_gen_overlap~
%patch86 -p1 -b .mono_deps_new~
%patch87 -p1 -b .php_dep_gen~
%patch88 -p1 -b .16004~
%patch89 -p1 -b .16005~
%patch90 -p1 -b .16022~
%patch91 -p1 -b .fc_deps~
%patch92 -p1 -b .rpmfc_ruby~
%patch93 -p1 -b .rb_newline~
%patch94 -p1 -b .haskell~
%patch95 -p1 -b .interpret_deps~
%patch96 -p1 -b .uclibc~
%patch97 -p1 -b .env_color~
%patch98 -p1 -b .fc_overlap~
%patch99 -p1 -b .py_macros~
%patch100 -p1 -b .script_overlap~
%patch101 -p1 -b .font~
%patch102 -p1 -b .kmod~
%patch103 -p1 -b .desktop~
%patch104 -p1 -b .skip_chrdev~
%patch105 -p1 -b .sizeof~
%patch106 -p1 -b .link_loop~
%patch107 -p1 -b .python_color~
%patch108 -p1 -b .pyegg_nodirs~
%patch109 -p1 -b .uclibc_nolib64~
%patch110 -p1 -b .req_devel~
%patch112 -p1 -b .gnu_hash~
%patch113 -p1 -b .depoch_rpmlib~
%patch114 -p1 -b .no_verdepfeat~
%patch115 -p1 -b .free~
%patch116 -p1 -b .skip_doc~
%patch117 -p1 -b .exec_modules~
#patch118 -p1 -b .soname_only~
%patch119 -p1 -b .rubyabi_prov~
%patch120 -p1 -b .filedep_origins~
%patch121 -p1 -b .equal_overlaps~
%patch122 -p1 -b .strdup~
%patch123 -p1 -b .ds_fopen~
%patch124 -p1 -b .debuginfo~
%patch125 -p1 -b .unitialized~
%patch126 -p1 -b .trig_pcre~
%patch127 -p1 -b .trigger_args~
%patch128 -p1 -b .triggers_nooverlap~
%patch129 -p1 -b .memleak~
%patch130 -p1 -b .str_nul~
%patch131 -p1 -b .dlopen~
%patch132 -p1 -b .py_input~
%patch133 -p1 -b .devel_prov~
#patch134 -p1 -b .lua~
%patch135 -p1 -b .db_rdonly~
%patch136 -p1 -b .ds_merge~
%patch137 -p1 -b .slash~
#patch138 -p1 -b .trigtrans~
%patch139 -p1 -b .fix_verify~
%patch140 -p1 -b .rpmv3~
%patch141 -p1 -b .dev_unfuck~
%patch142 -p1 -b .typelib~
%patch143 -p1 -b .mono_newline~
%patch144 -p1 -b .urpm~
#required by P55, P80, P81, P94..
./autogen.sh

mkdir -p cpu-os-macros
tar -zxf %{SOURCE3} -C cpu-os-macros

%build
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
		--with-mozjs185=external \
%else
		--without-mozjs185 \
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
%if %{with squirrel}
		--with-squirrel=external \
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
		--with-lua=internal \
		--with-expat=external \
		--with-pcre=external \
%ifarch %{ix86} x86_64 ppc ppc64 ia64
		--with-cpuinfo=external \
%else
		--without-cpuinfo \
%endif
		--with-syck=external \
		--with-file=external \
		--with-path-magic=%{_datadir}/misc/magic.mgc \
		--with-beecrypt=external \
		--with-usecrypto=beecrypt \
		--with-keyutils=external \
		--with-neon=external \
		--with-acl \
		--enable-openmp \
%if %{with xar}
		--with-xar=%{_includedir}/xar \
%endif
		--with-db \
		--with-dbsql=external \
		--without-db-tools-integrated \
%if %{with sqlite}
		--with-sqlite=external \
%else
		--without-sqlite \
%endif
%if %{with ossp-uuid}
		--with-uuid=external \
%else
		--without-uuid \
%endif
%if %{with augeas}
		--with-augeas=external \
%else
		--without-augeas \
%endif
%if 0
		--with-extra-path-macros=%{_usrlibrpm}/macros.d/mandriva \
%else
		--with-extra-path-macros=%{_usrlibrpm}/platform/%%{_target}/macros:%{_sysconfdir}/rpm/macros.d/*.macros:%{_usrlibrpm}/macros.d/mandriva \
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
%if %{with docs}
%make apidocs
%endif

%check
#make check

%install
%makeinstall_std

# XXX: why isn't this installed by 'make install'?
install -m755 scripts/symclash.* %{buildroot}%{_rpmhome}

# Save list of packages through cron
install -m755 scripts/rpm.daily -D %{buildroot}%{_sysconfdir}/cron.daily/rpm
install -m644 scripts/rpm.log -D %{buildroot}%{_sysconfdir}/logrotate.d/rpm

mkdir -p %{buildroot}/var/spool/repackage

mkdir -p %{buildroot}%{_sysconfdir}/%{name}/{{pre,}macros.d,sysinfo}

# actual usefulness of this seems rather dubious with macros.d now...
cat > %{buildroot}%{_sysconfdir}/%{name}/macros <<EOF
# Put your own system macros here
# usually contains 

# Set this one according your locales
# %%_install_langs

EOF

# FIXME: weird issue, seems to have issue with lines starting with '%%_'...
cat > %{buildroot}%{_sysconfdir}/%{name}/premacros.d/cpuinfo_target.macros <<EOF
# This sets which of the available architectures to prefer when building
# packages with libcpuinfo support enabled.
 %%_prefer_target_cpu     x86_64 i586
EOF

# Get rid of unpackaged files
# XXX: is there any of these we might want to keep?
for f in %{py_platsitedir}/poptmodule.a %{py_platsitedir}/rpmmodule.a \
	%{py_platsitedir}/rpm/*.a %{_rpmhome}/*.a %{_rpmhome}/lib/*.a\
	%{_rpmhome}/{Specfile.pm,cpanflute2,cpanflute,sql.prov,sql.req,tcl.req} \
	%{_rpmhome}/{config.site,cross-build,rpmdiff.cgi} \
	%{_rpmhome}/trpm %{_bindir}/rpmdiff; do
	rm -f %{buildroot}$f
done

%find_lang %{name}

mkdir -p %{buildroot}/var/lib/rpm/{log,tmp}
for dbi in `./rpm --macros macros/macros --eval %_dbi_tags_4|tr : ' '` Seqno __db.00{0..9}; do
    touch %{buildroot}/var/lib/rpm/$dbi
    echo "%attr(0644, root, root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) %{_localstatedir}/lib/rpm/$dbi" >> %{name}.lang
done

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
install -m644 %{SOURCE4} -D %{buildroot}%{_sysconfdir}/%{name}/macros.d/legacy_compat.macros

%if %{with docs}
install -d %{buildroot}%{_docdir}/rpm
cp -r apidocs/html %{buildroot}%{_docdir}/rpm
%endif

install -d %{buildroot}%{multiarch_bindir}
install -d %{buildroot}%{multiarch_includedir}
%if "%{_lib}" == "lib64"
install -d %{buildroot}%(linux32 rpm -E %%{multiarch_bindir})
install -d %{buildroot}%(linux32 rpm -E %%{multiarch_includedir})
%endif

# TODO: review which files goes into what packages...?
%files -f %{name}.lang
%doc CHANGES doc/manual/[a-z]*
%if %{with docs}
%exclude %{_docdir}/rpm/html
%endif
/bin/rpm
%{_bindir}/multiarch-dispatch
%{_bindir}/rpmconstant*
%{_bindir}/rpm2cpio*
%{_rpmhome}/bin/augtool
%{_rpmhome}/bin/chroot
%{_rpmhome}/bin/cp
%{_rpmhome}/bin/dbconvert
%{_rpmhome}/bin/find
#%%{_rpmhome}/bin/grep
#%%{_rpmhome}/bin/lua
%{_rpmhome}/bin/mtree
%{_rpmhome}/bin/mgo
#%%{_rpmhome}/bin/rc
%{_rpmhome}/bin/rpmspecdump
%{_rpmhome}/bin/wget
%if %{with xar}
%{_rpmhome}/bin/txar
%endif
%{_rpmhome}/dbconvert.sh
%{_rpmhome}/rpm.*
%{_rpmhome}/rpm2cpio
%{_rpmhome}/rpmdb_loadcvt
%{_rpmhome}/tgpg

%dir %{_localstatedir}/lib/rpm
%dir %{_localstatedir}/lib/rpm/log
%dir %{_localstatedir}/lib/rpm/tmp


%{_rpmhome}/macros.d/*
%{_rpmhome}/cpuinfo.yaml
%{_rpmhome}/macros
%{_rpmhome}/rpmpopt
%{_rpmhome}/platform/*/macros
%config(noreplace) %{_localstatedir}/lib/rpm/DB_CONFIG

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
%dir %{_sysconfdir}/%{name}/sysinfo
%{_sysconfdir}/%{name}/macros.d/*.macros
%{_sysconfdir}/%{name}/premacros.d/*.macros

%{_mandir}/man[18]/*.[18]*
%lang(pl)	%{_mandir}/pl/man[18]/*.[18]*
%lang(ru)	%{_mandir}/ru/man[18]/*.[18]*
%lang(ja)	%{_mandir}/ja/man[18]/*.[18]*
%lang(sk)	%{_mandir}/sk/man[18]/*.[18]*
%lang(fr)	%{_mandir}/fr/man[18]/*.[18]*
%lang(ko)	%{_mandir}/ko/man[18]/*.[18]*
%exclude	%{_mandir}/man8/rpmbuild.8*
%exclude	%{_mandir}/man8/rpmdeps.8*

%{_sysconfdir}/cron.daily/rpm
%config(noreplace,missingok) %{_sysconfdir}/logrotate.d/rpm

%dir %{multiarch_bindir}
%dir %{multiarch_includedir}
%if "%{_lib}" == "lib64"
%dir %(linux32 rpm -E %%{multiarch_bindir})
%dir %(linux32 rpm -E %%{multiarch_includedir})
%endif

%{_includedir}/multiarch-dispatch.h

%files build
%{_bindir}/gendiff
%{_bindir}/rpmbuild
%{_bindir}/multiarch-platform
#%%{_rpmhome}/bin/abi-compliance-checker.pl
%{_rpmhome}/bin/api-sanity-autotest.pl
%{_rpmhome}/bin/dbsql
%{_rpmhome}/bin/debugedit
%{_rpmhome}/bin/install-sh
%{_rpmhome}/bin/lua
%{_rpmhome}/bin/luac
%{_rpmhome}/bin/mkinstalldirs
%{_rpmhome}/bin/pom2spec
%{_rpmhome}/bin/rpmcache
%{_rpmhome}/bin/rpmcmp
%{_rpmhome}/bin/rpmdeps
%{_rpmhome}/bin/rpmdigest
%{_rpmhome}/bin/rpmkey
%{_rpmhome}/bin/rpmlua
%{_rpmhome}/bin/rpmluac
%{_rpmhome}/bin/rpmrepo
%{_rpmhome}/bin/sqlite3
%dir %{_rpmhome}/helpers
%{_rpmhome}/helpers/*
%dir %{_rpmhome}/qf
%{_rpmhome}/qf/*
%{_rpmhome}/vcheck
%{_rpmhome}/brp-*
%{_rpmhome}/check-files
%{_rpmhome}/check-multiarch-files
#%%{_rpmhome}/cross-build
%{_rpmhome}/find-debuginfo.sh
%{_rpmhome}/find-lang.sh
%{_rpmhome}/find-prov.pl
%{_rpmhome}/find-provides.perl
%{_rpmhome}/find-req.pl
%{_rpmhome}/find-requires.perl
%{_rpmhome}/fontconfig.prov
%{_rpmhome}/gem_helper.rb
%{_rpmhome}/getpo.sh
%{_rpmhome}/gstreamer.sh
%{_rpmhome}/haskelldeps.sh
%{_rpmhome}/http.req
%{_rpmhome}/javadeps.sh
%{_rpmhome}/kmod-deps.sh
%{_rpmhome}/mkmultiarch
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
%{_rpmhome}/pythoneggs.py
%{_rpmhome}/rubygems.rb
%{_rpmhome}/symclash.*
%{_rpmhome}/u_pkg.sh
%{_rpmhome}/vpkg-provides.sh
%{_rpmhome}/vpkg-provides2.sh

%if %{with js}
%{_rpmhome}/bin/tjs
%endif
%{_rpmhome}/macros.rpmbuild
%{_mandir}/man8/rpmbuild.8*
%{_mandir}/man8/rpmdeps.8*

%files -n %{librpmname}
%{_libdir}/librpm-%{libver}.so
%{_libdir}/librpmconstant-%{libver}.so
%{_libdir}/librpmdb-%{libver}.so
%{_libdir}/librpmio-%{libver}.so
%{_libdir}/librpmmisc-%{libver}.so
%{_libdir}/librpmbuild-%{libver}.so
%if %{with js}
%{_rpmhome}/lib/librpmjsm.so.*
%{_rpmhome}/lib/rpmjsm.so
%endif
#%%if %%{with sqlite}
#%%{_rpmhome}/libsql*.so.*
#%%endif

%files -n %{librpmnamedevel}
#%%doc apidocs/html
%{_includedir}/rpm
%{_libdir}/librpm.so
%{_libdir}/librpmconstant.so
%{_libdir}/librpmdb.so
%{_libdir}/librpmio.so
%{_libdir}/librpmmisc.so
%{_libdir}/librpmbuild.so
%{_libdir}/pkgconfig/rpm.pc

%if %{with js}
%{_rpmhome}/lib/librpmjsm.so
%endif
#%%if %%{with sqlite}
#%%{_rpmhome}/libsql*.so
#%%endif

%files -n %{librpmstatic}
%{_libdir}/librpm.a
%{_libdir}/librpmconstant.a
%{_libdir}/librpmdb.a
%{_libdir}/librpmio.a
%{_libdir}/librpmmisc.a
%{_libdir}/librpmbuild.a

%if %{with perl}
%files -n perl-%{perlmod}
#%%doc perl/Changes
%if %{with embed}
%{_rpmhome}/lib/rpmperl.so
%endif
%{_mandir}/man3/RPM*
%{perl_vendorarch}/%{perlmod}.pm
%dir %{perl_vendorarch}/%{perlmod}
%{perl_vendorarch}/%{perlmod}/*.pm
%{perl_vendorarch}/auto/%{perlmod}
%endif

%if %{with python}
%files -n python-rpm
%if %{with embed}
%{_rpmhome}/lib/rpmpython.so
%endif
%dir %{py_platsitedir}/rpm
%{py_platsitedir}/rpm/*.py
%{py_platsitedir}/rpm/*.so
%endif

%if %{with ruby}
%files -n rpm-rubyembed
%{_rpmhome}/bin/trb
%{_rpmhome}/lib/rpm.so
%{_rpmhome}/lib/rpmruby.so
%endif

%if %{with tcl}
%files -n rpm-tclembed
%{_rpmhome}/lib/rpmtcl.so
%endif

%if %{with squirrel}
%files -n rpm-squirrelembed
%{_rpmhome}/lib/rpmsquirrel.so
%endif

%if %{with docs}
%files apidocs
%dir %{_docdir}/rpm/html
%{_docdir}/rpm/html/*
%endif
