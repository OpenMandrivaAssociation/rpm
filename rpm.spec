%ifarch %{arm}
%define _xz_threads 0
%endif

%define python_version 2.7
%define	_target_vendor	mandriva

%bcond_with	bootstrap
%bcond_with	debug
%bcond_without	ossp_uuid
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
# disabled due to issues with texlive packages ~always being out of sync with
# synthesis..
%bcond_with	docs
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

# can probably be restored now..
%if %{with bootstrap}
#include %%{_sourcedir}/bootstrap.spec
%endif

%define	bdb		db52

%define	libver		5.4
%define	minorver	15
%define	srcver		%{libver}.%{minorver}
#define	prereldate	20110712

%define	libname	%mklibname rpm %{libver}
%define	devname	%mklibname -d rpm
%define	static	%mklibname -d -s rpm

%ifarch aarch64
# "linux32 rpm -E %{_arch}" returns aarch64 on aarch64...
# Force it to do the right thing for now
%define multiarch_platform multiarch-arm-%{_target_os}
%endif

Summary:	The RPM package management system
Name:		rpm
Epoch:		1
Version:	%{libver}.%{minorver}
Release:	%{?prereldate:0.%{prereldate}.}19
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
# In order to more easily cope with merges and avoid issues with binary formats,
# we're now using the ar format which will give us a pure ascii archive that'll
# make it possible to track & merge individual changes like with other text files.
# Unfortunately the format doesn't support paths..
# recommended way of making changes and updating archive:
# rm -rf foo
# pushd foo
# ar x ../cpu-os-macros.a
# <perform your changes>
# popd
# ar cDr cpu-os-macros.a foo/*macros
#
# !!! THIS FILE SHOULD BE MAINTAINED IN GIT !!!
Source3:	cpu-os-macros.a
Source4:	legacy_compat.macros
Source5:	RPMBDB-0.1.tar.xz
Source6:	git-repository--after-tarball
Source7:	git-repository--apply-patch
# TODO: make conditional & disabled through macro by default (enable for legacy compatibility)
# status: to be removed later
Patch2:		rpm-5.4.9-non-pre-scripts-dont-fail.patch
# status: to be removed later
Patch3:		rpm-5.4.9-no-doc-conflicts.patch
# Don't disable keyserver queries
Patch6:		rpm-5.4.10-use-keyserver.patch
# Don't override libexecdir, that's bogus
Patch7:		rpm-5.4.10-no-libexecdir-override.patch
# fixes a typo in russian translation (#62333)
# status: needs to be pushed back to the Russian i18n project
Patch11:	rpm-5.4.9-fix-russian-typo.patch
# temporary workaround for issues with file triggers firing multiple times and
# a huge memleak...
# DIE
Patch15:	rpm-5.3.8-fire-file-triggers-only-once.patch
# status: ready to merge, it's already been merged on HEAD, so commiting it to rpm-5_4
# would basically just mean backporting it..
Patch29:	rpm-5.4.4-add-_specfile-macro.patch
# status: ready for merge
Patch31:	rpm-5.4.9-fix-rpm_qa-pattern.patch
# uhm.. broken?
# status: this one was fixed for real in 5.3.12, but I forgot commiting it
# on rpm-5_4 branch back then, and I've been unable to remember and not
# bothered figuring out what was wrong..
Patch32:	rpm-5.4.4-really-always-invoke-clean-at-end.patch
# status: i18n strings is getting dropped, so this one might be of less relevance,
# but feel free to discuss it on rpm-devel
Patch33:	rpm-5.4.9-fix-mdvbz62979.patch
# This patch adds support for untangling dependency loops with prioritized removal
# of dependencies from loops. It's very crude for now and certainly needs some obvious
# improvement, but it'll fix the most common scenario giving issues where ie.
# Requires(post) has been used and shouldn't introduce any regressions..
# REF: http://rpm5.org/community/rpm-devel/4633.html
# status: needs to be finished and probably rewrite the implementation,
# so keep locally for now, but feel free to discuss it on rpm-devel if you run out
# of things to do.. :p
Patch34:	rpm-5.4.4-use-dependency-type-for-ordering.patch
# status: needs to be cleaned up and properly reviewed together with rest
# of the patches related to dependency generation
Patch37:	rpm-5.4.9-avoid-dependencies-on-self.patch
# status: probably ready to merge
Patch40:	rpm-5.4.4-pkgconfigdeps-check-path.patch
# status: probably okay to merge, but discuss on rpm-devel first
Patch42:	rpm-5.4.4-glob-wildcards-for-loading-macro-files.patch
# status: needs to be discussed
Patch46:	rpm-5.4.4-allow-installation-of-repackaged-rpms.patch
# status: same as for other dependency generation related patches
Patch47:	rpm-5.4.4-fix-removal-of-overlapping-dependencies.patch
# status: ready to merge
Patch48:	rpm-5.4.8-dont-show-suggests-with-requires.patch
# backport from HEAD
# status: almost ready for merge, the strip reloc flag to debugedit needs to be made
# conditional first in order to not break backwards compatibility with older elfutils versions
Patch55:	rpm-5.4.9-find-debuginfo-strip-reloc-debug-sections.patch
# status: ready for merge
Patch61:	rpm-5.4.4-fix-same-package-with-epoch-possible-to-upgrade.patch
# status: ready for merge
Patch63:	rpm-5.4.9-strip-buildroot-away-from-duplicate-files-list.patch
# status: probably okay to merge, but discuss on rpm-devel first
Patch64:	rpm-5.4.10-duplicate_files_terminate_build.patch
# status: same as above
Patch65:	rpm-5.4.10-unpackaged_subdirs_terminate_build.patch
# mdvbz#64898
# status: uncertain, might be okay to merge, discuss on rpm-devel first
Patch66:	rpm-5.4.4-rpmbuild-withoutclean.patch
# status: ready for merge
Patch67:	rpm-5.4.4-find-debuginfo-avoid-excessive-output-from-eu-strip.patch
# no sense in having an additional dependency on 'pkgconfig' on all packages that
# have a pkgconfig file, it's not needed for them to be made useful and anything
# actuallly using pkgconfig for this purpose will pull it in as a dependency anyways...
# status: might be okay to merge, but discuss on rpm-devel first
Patch69:	rpm-5.4.4-drop-useless-auto-generated-pkgconfig-dependency.patch
# drop dependencies such as /bin/sh which will always be satisfied by glibc's dependency on
# bash, and also on /sbin/ldconfig which always will be satisfied by glibc
# status: should *NOT* be merged
Patch70:	rpm-5.4.4-drop-base-dependencies.patch
# status: ready for merge
Patch71:	rpm-5.4.12-fix-rpmconstant-to-always-use-LC_CTYPE-C-for-case-conversion.patch
# $RPM_BUILD_DIR isn't necessarily the same as $PWD, it's %%{_builddir}, not
# %%{_builddir}/%%{?buildsubdir}, messing up paths in debug packages created..
# status: needs to be discussed and investigated a bit better..
Patch74:	rpm-5.4.4-pass-_builddir-properly-to-find-debuginfo.patch
# status: probably okay to merge, but discuss on rpm-devel first
Patch76:	rpm-5.4.10-files-listed-twice-terminates-build.patch
# status: don't merge
Patch77:	rpm-5.4.15-use-bdb-5.2.patch
# status: probably okay to merge
Patch78:	rpm-5.4.9-ruby1.9-fixes.patch
# mdvbz#65269
# status: same as for other dependency generation patches
Patch79:	rpm-5.4.4-dont-consider-ranged-dependencies-as-overlapping-for-removal.patch
# status: same as for other dependency generation patches
Patch85:	rpm-5.4.5-fix-removal-of-overlapping-dependencies-for-internal-dependency-generator.patch
# this updates to using the dependency generator shipped with mono, it has some
# issues which makes me cautious about actually merging it with rpm5 upstream,
# but we'll anyways use it as is for now to prevent any potential regressions
# by switching to the internal dependency generator
# status: shouldn't be merged as is
Patch86:	rpm-5.4.5-update-mono-dependency-generator.patch
# status: probably okay to merge
Patch87:	rpm-5.4.5-dont-generate-php-dependencies-only-when-executable.patch
# status: these three were lost on rpm-5_3 branch, so should be okay to merge
Patch88:	rpm-5.4.5-patchset_16004.patch
Patch89:	rpm-5.4.5-patchset_16005.patch
Patch90:	rpm-5.4.5-patchset_16022.patch
# status: same as for other dep gen patches
Patch91:	rpm-5.4.9-update-rpmfc-when-removing-dependencies-on-self.patch
# status: idem
Patch92:	rpm-5.4.9-rpmfc-extract-dependencies-for-all-files.patch
# status: ready for merge
Patch93:	rpm-5.4.5-rubygems-add-missing-newline.patch
# status: ugly, keep locally for now
Patch94:	rpm-5.4.15-generate-haskell-dependencies.patch
# status: same as for other dep gen patches
Patch95:	rpm-5.4.5-drop-some-interpreter-deps.patch
# status: probably okay to merge..
Patch96:	rpm-5.4.5-fix-elf-interpreter-resolving-breaking-uclibc-deps.patch
# status: probably okay to merge
Patch97:	rpm-5.4.5-set-proper-file-color-for-scripts-using-env-in-shellbang.patch
Patch98:	rpm-5.4.5-update-rpmfc-when-removing-overlapping-dependencies.patch
# status: probably okay to merge
Patch99:	rpm-5.4.5-python-export-spec-macros.patch
# status: same as for other dep gen patches
Patch100:	rpm-5.4.5-do-not-merge-script-dependencies-with-non-script-dependencies.patch
# status: idem
Patch101:	rpm-5.4.15-font-provides.patch
# status: idem
Patch102:	rpm-5.4.7-kmod-dependencies.patch
# status: idem
Patch103:	rpm-5.4.15-desktop-provides.patch
# status: probably okay to merge, discuss on rpm-devel first
Patch104:	rpm-5.4.5-skip-dependencies-for-character-devices.patch
# status: same as for other dep gen patches
Patch106:	rpm-5.4.5-break-out-of-elf-link-loop.patch
# status: probably okay to merge
Patch107:	rpm-5.4.5-rpmfc-apply-python-coloring-from-magic.patch
# status: same as for other dep gen patches
Patch109:	rpm-5.4.5-fix-generation-of-uclibc-deps-on-non-lib64.patch
# status: idem
Patch110:	rpm-5.4.7-only-generate-devel-deps-for-symlinks-start-with-lib.patch
# status: keep locally
Patch111:	rpm-5.4.9-keep-loading-script-macros.patch
# status: ready for merge
Patch112:	rpm-5.4.7-use-gnu-hash-style-by-default-and-drop-rtld-dep.patch
# status: keep locally only
Patch113:	rpm-5.4.9-add-distepoch-rpmlib-feature.patch
# status: probably okay to merge, but discuss on rpm-devel first
Patch114:	rpm-5.4.9-dont-add-versioneddependency-rpmlib-feature-dependency.patch
# status: probably okay to merge
Patch116:	rpm-5.4.12-dont-try-generate-rpmfc-dependencies-from-doc-files.patch
# status: ready to merge
Patch117:	rpm-5.4.7-only-generate-ruby-and-python-deps-for-executables-and-modules.patch
# status: ready
Patch119:	rpm-5.4.7-fix-generation-of-ruby-abi-provides.patch
# status: same as for other dep gen patches
Patch120:	rpm-5.4.7-print-name-of-files-removed-dependencies-are-generated-from.patch
# status: idem
Patch121:	rpm-5.4.7-always-choose-equal-only-deps-when-overlapping.patch
# status: idem
Patch122:	rpm-5.4.7-rpmfc-strdup-EVR-in-overlap-removal.patch
# status: idem
Patch123:	rpm-5.4.7-rpmds-dont-try-fopen-empty-filenames.patch
# status: ready
Patch124:	rpm-5.4.7-change-to-debuginfo-suffix.patch
# crash reproducable with 'rpm -qa --triggers'
# status: ready
Patch125:	rpm-5.4.7-hdrfmt-fix-unitialized-argv-element.patch
# status: probably okay to merge, discuss on rpm-devel first
Patch126:	rpm-5.4.9-add-filetriggers-regex-matching-support.patch
# status: idem
Patch127:	rpm-5.4.12-add-matches-as-arguments-to-triggers.patch
# status: same as for other dep gen patches
Patch128:	rpm-5.4.7-dont-consider-trigger-dependencies-as-overlapping.patch
# status: ready
Patch129:	rpm-5.4.7-fix-minor-memleaks.patch
# status: ready
Patch130:	rpm-5.4.9-mire-fix-strings-lacking-null-terminator.patch
# status: keep locally for now
Patch131:	rpm-5.4.15-dlopen-embedded-interpreters.patch
# status: ready
Patch132:	rpm-5.4.9-rpmpython-fix-input.patch
# status: same as for other dep gen patches
Patch133:	rpm-5.4.7-generate-devel-provides-outside-of-libdirs.patch
## status: ready/merged?
#Patch134:	rpm-5.4.14-actually-perform-linking-against-internal-lua.patch
# status: ready
Patch135:	rpm-5.4.7-no-seqid_init-on-rdonly-database.patch
# status: same as for other dep gen patches
Patch136:	rpm-5.4.9-add-support-for-using-rpmdsMerge-with-filepath-tags.patch
# status: probably ready for merging
Patch137:	rpm-5.4.9-avoid-double-slash-in-path-for-dirname-filetrigger-matching.patch
# This patch adds %%triggerpretransin, %%triggerpretransun,
# %%triggerposttransin, %%triggerposttransun # triggers, which behaves in
# similar fashion as the legacy mandriva triggers, ie. it will fire only once
# for all matches per transaction.
# Caveat: Due to lack of available bits for dependency flags, the same bits as
# for regular triggers are reused with only one additional bit used to identify
# as pre/posttrans triggers, meaning that older rpm versions will identify
# these triggers as regular triggers. One possible solution could be something
# like setting an environment variable that the packager writing the trigger
# can check for in the trigger script..
# status: pretty much done, but implementation might not be satisfactory to
# everyone, requiring some greater discussion to take place before even
# considering merging it upstream.
# status: ready for use, but keep locally for now...
Patch138:	rpm-5.4.15-trigtrans.patch
# status: probably ready to merge, discuss on rpm-devel first
# https://qa.mandriva.com/show_bug.cgi?id=64378
Patch139:	rpm-5.4.9-fix-verify-segfault.patch
# status: keep locally
Patch140:	rpm-5.4.15-rpmv3-support.patch
# status: ready
Patch143:	rpm-5.4.7-mono-find-requires-strip-newlines.patch
# status: ready
Patch144:	rpm-5.4.8-URPM-build-fix.patch
# status: keep locally, might drop this one later..
Patch146:	rpm-5.4.9-support-signatures-and-digest-disablers.patch
# status: can be merged, but doesn't really matter as it's to be removed and
# we now anyways disable the support in question..
Patch150:	rpm-5.4.9-dont-remap-i18n-strings-if-enabled.patch
# status: just keep around and toss away when ripped out upstream...
Patch151:	rpm-5.4.9-disable-support-for-i18nstring-type.patch
# lack insight on actual functionality, which anyways seems broken, so let's
# disable it to avoid errors from berkeley db..
# status: keep locally/disabled upstream as well
#Patch152:	rpm-5.4.9-disable-l10ndir.patch
# the php dependency generator carried with rpm5 is based on a version from PLD
# that they've backed out later on, reverting to their older version.
# this patch replaces current upstream rpm5 version with mandriva one, which is
# based on the same as PLD currently uses.
# status: current version carried upstream seems useless and unmaintained, so
# replacing it with this one shouldn't hurt..
Patch156:	rpm-5.4.9-updated-pld-mandriva-php-dep-generator.patch
# this patch contains changes from rpm-setup & rpm.org
# status: not entirely convinced by the perl version conversion macro stuff
# in the script, which might not be upstream material, but rest of the patch
# should otherwise be sane 'nuff
Patch157:	rpm-5.4.10-merge-rpm.org-and-mandriva-perl-dep-gen-changes.patch
# Due to rpmdav/neon being written in a different fashion than other rpmio clients,
# the inconsistent behaviour affects code elsewhere which expects consistent behaviour,
# with the result being that when unable to download files, neon will save error
# page as the target file.
# status: should go upstream, but uncertain about "correct" fix, ie. this is
# more of a workaround, while rewriting rpmdav code to behave consistently
# would be "the right thing to do". Yet I'm not fully able to grasp all of the
# code and don't want to spend more time just to get the API..
Patch158:	rpm-5.4.10-fix-neon-saving-error-pages-as-target-file.patch
# As the transaction flags for ignoring arch & os are no longer used, there's
# currently no way to ignore arch & os of packages anymore. This patch adds
# support for doing this again by defining rpm variables and overriding
# --ignorearch & --ignoreos to set these.
# status: needs to be discussed upstream before thinking about merging
Patch159:	rpm-5.4.10-support-ignore-arch-and-os-again.patch
Patch160:	rpm-5.4.10-bump-up-to-default-xz-compression-level.patch
# fix so that we search through library dirs within buildroot for uclibc libraries
# status: same as for other dep gen patches
Patch161:	rpm-5.4.10-search-through-buildroot-library-dirs-for-uclibc-deps.patch
# status: same as for other dep gen patches
Patch162:	rpm-5.4.10-fix-uninitialized-variable.patch
Patch163:	rpm-5.4.10-new-moondrake-name.patch
# pass --disable-silent-rules to configure so that we'll by default always get
# consistent behaviour of verbose build output
# status: ready
Patch164:	rpm-5.4.10-configure-disable-silent-rules.patch
# our own helper scripts needs to be run first so that library permissions gets
# fixed for find-debuginfo.sh to properly strip them
# status: ready as they only modify our own distribution specific macros..
Patch165:	rpm-5.4.10-post-install-helper-order.patch
# fixes issue with ldflags getting duplicated when configure is run more than once
# status: ready
Patch166:	rpm-5.4.10-fix-ldflags-passing.patch
# fixes extraction of perl version from Config.pm when it's of a different
# version than system version
# status: ready
Patch167:	rpm-5.4.10-fix-perl-abi-provides-version.patch
# in our perl package, the perl library now has a versioned soname, so there's no
# longer any need for special treatment of perl extension with explicitly
# versioned perl(abi) dependencies anymore
# status: relies on mandriva specific behaviour with local patches, so keep locally
Patch168:	rpm-5.4.10-no-more-explicit-perl-abi-version-reqs.patch
# this patch updates the upstream brp-compress scripts, which will be replacing
# our own locally maintained compress-files script from spec-helper
# status: ready
Patch169:	rpm-5.4.10-update-and-use-brp-compress.patch
# status: ready
Patch170:	rpm-5.4.10-arch_tagged-consistent-with-mark64-provides.patch
# status: ready
Patch171:	rpm-5.4.10-set-lc_ctype-to-utf8-when-building-gem.patch
# see http://www.mail-archive.com/rpm-maint@lists.rpm.org/msg01819.html
# broken, don't apply
#Patch172:	rpm-5.4.10-debugedit-resolve-paths-to-absolute-paths.patch
# resolve absolute path before setting $RPM_BUILD_DIR rather to fix same issue
# without regression
# status: ready
Patch172:	rpm-5.4.10-resolve-absolute-path-to-RPM_BUILD_DIR-for-debugedit.patch
# just fix a couple of minor memleaks at exit..
# status: ready
Patch173:	rpm-5.4.10-fix-a-couple-of-debugedit-memleaks.patch
# make "canonicalization(...)shrank by one character" error message more useful
# status: ready
Patch174:	rpm-5.4.10-debugedit-saner-error-msg.patch
# files added with %%doc gets copied to buildroot after %%install, preventing
# ie. fix_eol to be run on these files (where it's usually most relevant),
# so let's add support for specific scripts to be run after this and make sure
# to execute fix_eol then..
# status: kinda breaks use of (prolly' never used) $DONT_FIX_EOL variable,
# while not feeling exactly perfectly implemented either, but works more than
# satisfactory 'nuff for us, so should be discussed before merging upstream..
Patch175:	rpm-5.4.10-run-spec-helper-at-end-of-doc-stage.patch
# reverts change upstream that adds rpath to perl module
# status: as it reverts a previous upstream change, it prolly' shouldn't be
# merged, but probably worthwhile a discussion at least...
Patch176:	rpm-5.4.10-drop-rpath-from-perl-module.patch
Patch178:	rpm-5.4.15-crosscompile.patch
# tool for automatically checking and fixing broken rpmdb
# status: probably' worth merging upstream
Patch179:	rpm-5.4.14-rpmdbchk.patch
# adds casts for C++ compatibility
# status: ready
Patch180:	rpm-5.4.10-rpmdb-typecasts.patch
# adds ability for printing parsed version of spec file with 'rpm -q --specfile --printspec'
# status: very simple, non-intrusive, while quite convenient, should be okay to merge
Patch181:	rpm-5.4.14-printspec.patch
# drop remaining legacy scripts from rpm-mandriva-setup-build package for us to
# be able to obsolete it
# status: mandriva specific, ready to merge
Patch182:	rpm-5.4.10-drop-legacy-scripts-from-rpm-setup.patch
# as these flags are enabled in linker by default now there's no point in
# passing them, while the disablers are also completely useless as well as
# a result
# status: mandriva specific, ready to merge
Patch183:	rpm-5.4.10-drop-linker-flags-from-ldflags-macro-thats-now-implicitly-enabled-by-default.patch
# clean out some old macros etc.
# status: mandriva specific, ready to merge
Patch184:	rpm-5.4.10-cleanup-mandriva-specific-macros.patch
# elf(buildid) provides are currently not actually used for any purpose, yet
# they're generated for each individual executable binary, so let's just
# disable this for now and look at this again whenever in the future it
# might have any possible relevance
# status: keep locally
Patch185:	rpm-5.4.10-disable-generation-of-buildid-provides.patch
# adjust to gstreamer 1.0
Patch188:	rpm-5.4.10-gstreamer1.0-deps.patch
# $RPM_PACKAGE_NAME & $RPM_ARCH are used by aot-compile{,-rpm}, so let's just
# add it back for now...
# status: keep local
Patch189:	rpm-5.4.10-add-back-RPM_PACKAGE_NAME_and_RPM_ARCH.patch
Patch190:	rpm-5.4.10-configure-disable-rpath-and-dependency-tracking.patch
Patch191:	rpm-5.4.10-enhance-rename-macro-to-accept-optional-second-version-arg.patch
Patch192:	rpm-5.4.10-do-assert-rather-than-just-exit-on-memalloc-filaure.patch
# fixes issue where querying a package with >= 3 '-' in the name with an extra '-' behind
# status: ready
Patch193:	rpm-5.4.10-fix-memalloc-realloc-to-0.patch
#From ce2ce4c19724879b9ea469e7760c7922660b9698 Mon Sep 17 00:00:00 2001
#From: Panu Matilainen <pmatilai@redhat.com>
#Date: Tue, 3 Jan 2012 13:10:26 +0200
#Subject: [PATCH] Implement scriptlet start and stop callbacks (RhBug:606239)
#
#- Adds two new transaction callbacks: RPMCALLBACK_SCRIPT_START and
#  RPMCALLBACK_SCRIPT_STOP which get issued for every scriptlet we run.
#- On script start, callback can optionally return an FD which will
#  override transaction-wide script fd to make it easier to accurately
#  collect per-scriptlet output (eg per-scriptlet temporary file).
#  Callback is also responsible for closing the fd if it returns one.
#- For both callbacks, "amount" holds the script tag number. On stop
#  callback, "total" holds the scriptlet exit status mapped into
#  OK/NOTFOUND/FAIL for success/non-fatal/fatal errors. Abusing "notfound"
#  for warning result is ugly but differentiating it from the other
#  cases allows callers to ignore SCRIPT_ERROR if they choose to
#  implement stop and start. 
# status: ready
Patch194:	rpm-5.4.10-implement-start-and-stop-callbacks.patch
#From ff0ece3f6be58c8c28a766bdee5ed36daf1727b1 Mon Sep 17 00:00:00 2001
#From: Panu Matilainen <pmatilai@redhat.com>
#Date: Thu, 5 Jan 2012 14:34:46 +0200
#Subject: [PATCH] Add enum for RPMCALLBACK_INST_STOP callback event
#
#- Unused atm but we'll be adding this shortly
Patch195:	rpm-5.4.10-add-enum-for-RPMCALLBACK_INST_STOP-callback-event.patch
Patch197:	rpm-5.4.10-dont-require-group-and-summary-tag-during-build.patch
Patch198:	rpm-5.4.10-enable-nofsync-for-rpm-rebuilddb.patch
Patch199:	rpm-5.4.10-fix-font-dep-misidentification.patch
Patch200:	rpm-5.4.10-dont-silence-patch-output.patch
Patch201:	rpm-5.4.10-fix-log-install-remove-to-syslog.patch
Patch203:	rpm-5.4.10-postpone_subpackage_build_failures.patch
# Do not generate pythonegg provides for python3 until we find a better solution
Patch204:       rpm-5.4.10-python3-egg-reqs.patch
# fixed upstream
#Patch205:	rpm-5.4.12-fix-squirrel-version-check.patch
Patch209:	rpm-5.4.12-fix-rpmlua-print.patch
Patch210:	rpm-5.4.13-fix-rpmpython-module-import-init.patch
Patch211:	rpm-5.4.12-truncate-output-buffer-after-use.patch
# (tpg) do not build static libs by default
Patch212:	rpm-5.4.10-configure-disable-static.patch
Patch215:	rpm-5.4.13-fix-free-of-memory-still-in-use.patch
Patch216:	rpm-5.4.13-perl-bindings-do-not-use-xmalloc.patch
# (bero): Add libpackage macro -- these lines are replicated into way too many spec files
Patch217:	rpm-5.4.10-libpackage-macro.patch
# Allows to override location of /etc/rpm, ie. convenient for avoiding to
# modify the platform configuration in the host environment such as explained
# at https://wiki.openmandriva.org/en/ARM (someone please update wiki).
# The following paths may be overridden during runtime:
# RPM_USRLIBRPM=/usr/lib/rpm
# RPM_ETCRPM=/etc/rpm
# RPM_LOCALEDIR=/usr/share/locale
Patch219:	rpm-5.4.14-allow-overriding-etcrpm-etc-during-runtime.patch
# (fedya): add aarch64 macro
Patch221:	0001-fix-aarch64-rpm5-multiarch-headers-scripting.patch
Patch222:	fix-config-sub-in-configure.patch
Patch223:	rpm-5.4.15-cmake-dependency-generator.patch
# there's some funky businiss going on with ABF where omv macros gets used,
# so let's make our variables read only for now...
Patch224:	rpm-5.4.14-moondrake-ro-variables.patch
Patch225:	rpm-5.4.14-add-more-archs-to-arm-macro.patch
Patch226:	rpm-5.4.14-support-multithreaded-xz-compression.patch
Patch227:	rpm-5.4.14-add-output-sync-to-make-macro.patch
Patch228:	rpm-5.4.14-makeinstall_std-preserve-timestamps.patch
Patch229:	rpm-5.4.14-allocate-large-enough-buffer-to-fit-terminator.patch
Patch230:	rpm-5.4.14-fix-overlapping-strcpy.patch
Patch231:	rpm-5.4.14-dont-hide-errors-from-pkgconfig.patch
Patch232:	rpm-5.4.14-find-debuginfo-exit-early-if-none-found.patch
Patch233:	rpm-5.4.14-avoid-false-positives-checking-for-arbitrary-tags.patch
Patch234:	rpm-5.4.14-query-always-noisy.patch
Patch235:	rpm-5.4.14-fix-filedigests-verify.patch
Patch236:	rpm-5.4.14-null-term-ascii-digest.patch
# fixed upstream
#Patch237:	rpm-5.4.14-verify-ghosts-broken-logic.patch
Patch238:	rpm-5.4.14-lua-enable-extra-libs.patch
Patch239:	rpm-5.4.14-gst-inspect-typo.patch
Patch240:	rpm-5.4.15-add-missing-openmp-flags.patch
Patch241:	rpm-5.4.14-scripts-closefds.patch
Patch242:	rpm-5.4.14-fix-internal-lua-build.patch
Patch243:	rpm-5.4.14-ruby-archdirs.patch
Patch244:	rpm-5.4.14-ruby-abi-versioned.patch
Patch245:	rpm-5.4.14-gem_helper-spec-arg.patch
Patch246:	rpm-5.4.14-rubygems2-support.patch
Patch247:	rpm-5.4.14-update-ruby_gemdir-and-ruby_ridir-macros.patch
Patch248:	rpm-5.4.14-fix-dependency-generation-when-ruby_version-is-empty.patch
# ???
#Patch249:	rpm-5.4.14-fix-undef-with_embedded-typo.patch
Patch250:	rpm-5.4.14-add-missing-_RPMLUA_INTERNAL-define.patch
Patch251:	rpm-5.4.14-workaround-scriptlet-dependency-ordering-issue.patch
Patch252:	rpm-5.4.15-add-support-for-deprecating-epoch.patch
Patch253:	rpm-5.4.14-enable-twiddle-in-evr-tupple.patch
Patch254:	rpm-5.4.14-rpmdav-handle-301-302-redirects.patch
Patch255:	rpm-5.4.10-silence-RPM_CHAR_TYPE.patch
Patch256:	rpm-5.4.14-preserve-tag-type.patch
Patch257:	rpm-5.4.10-namespace-compare.patch
Patch258:	rpm-5.4.12-revert-gpg-argv-parsing.patch
Patch259:	rpm-5.4.10-fix--p-interpreter-and-empty-script.patch
Patch260:	rpm-5.4.15-fix-missing-types-in-headers.patch
Patch261:	rpm-4.5-unglobal.patch
Patch262:	rpm-5.4.13-double-check-unpackaged-dirs.patch
Patch263:	rpm-5.4.9-debugedit-segv.patch
Patch264:	rpm-debugedit-valid-file-to-fix-segment-fault.patch
Patch265:	0001-Ensure-clean-paths-are-used-for-matching-in-debugedi.patch
Patch266:	rpm-5.4.14-overridable-src-rpm-filename.patch
# %%configure2_5x deprecation, %%configure handling
Patch267:	rpm-5.4.10-deprecate-configure2_5x.patch
Patch268:	rpm-5.4.14-add-dlopen_req-macro.patch
Patch269:	rpm-5.4.14-add-_rundir-macro.patch
# this patch will disable automatic %%doc files for files in specific
# directories by setting the _no_default_doc_files variable.
# as this will drop all %%docdirs for where %%doc files would be copied
# to, you'll need to add ie. a %%docdir %%{_defaultdocdir} line to %%files
Patch270:	rpm-5.4.14-add-support-for-disabling-default-doc-files.patch
# There's not really much good brought by assertion abort on broken headers,
# and there's anyways sanity checks of the headers following.
# By allowing rpm to not die on broken headers, ie. rpmdbchk will be able to
# fix these rpmdbs.
Patch271:	rpm-5.4.14-no-assert-abort-with-broken-headers.patch
Patch272:	rpm-5.4.14-delete-require-tags-if-all-dependencies-are-removed.patch
Patch273:	rpm-5.4.14-add-missing-delMacroAll-prototype.patch
Patch274:	rpm-5.4.15-fix-typo-in-configure.ac-breaking-perlembed.patch
Patch275:	rpm-5.4.15-fix-missing-rpmpython-endif.patch
Patch276:	rpm-5.4.15-rpmpython-fix-proper-inclusion-order.patch
Patch277:	rpm-5.4.15-revive-multiarch-optional.patch
Patch278:	rpm-5.4.15-fix-fortify-passing.patch
# Default to clang/clang++ for __cc and __cxx
Patch279:      rpm-5.4.10-default-to-clang.patch
# Use -gnueabihf rather than -gnueabi as suffix for arm hardfloat
# targets
# file 5.18+ reports xz files as "XZ compressed data" while older
# versions say "xz compressed data" -- make the check case insensitive.
Patch280:	rpm-5.4.10-rpm2cpio-file-5.18.patch
# Make sure macros work with python 3.x
Patch281:	rpm-5.4.10-macros-python3.patch
# Make the perl module use the same toolchain as everything else
Patch282:	rpm-5.4.10-perl-use-same-toolchain.patch
# Fix the %%config_update macro for config.* files in subdirectories
# whose names contain spaces (seen in resIL)
Patch283:	rpm-5.4.10-config_update-spaces-in-filenames.patch
# Default optflags to -Oz
Patch284:	rpm-5.4.10-default-to-Oz.patch
# Fix mklibname to automatically generate e.g. lib64qtxdg5_0
# (rather than lib64qtxdg50) for "%%mklibname qtxdg5 0"
Patch285:	rpm-5.4.14-mklibname-fix-lib-names-ending-with-digits.patch
Patch286:	rpm-5.4.14-rubygems2.2-support.patch
Patch287:	rpm-5.4.14-rubygems2_more_fixes.patch
# Turn back old implementation of __urlgetfile handling
Patch288:       rpm-5.4.10-turn-back-urlgetfile.patch
Patch289:	rpm-5.4.14-MDV-use-gnu-tar-compression-detection-for-parsePrep.patch
# backport from cvs
Patch290:	0001-rpmds-fix-off-by-1-comparison-check-parsing-N.A-comp.patch
Patch291:	rpm-5.4.15-add-disablers-for-target-host-build-configure-args.patch
Patch292:	rpm-5.4.15-define-proper-sharedstatedir.patch
Patch293:	rpm-5.4.15-drop-non-existant-file-from-libtpm-configure.patch
Patch294:	rpm-5.4.15-if-no-release-is-defined-dont-print-distepoch-as-part-of-EVRD.patch
Patch295:	rpm-5.4.15-lib_soname-macro.patch
Patch296:	rpm-5.4.15-avoid-use-of-c99-header-types-in-public-api.patch
Patch297:	rpm-5.4.15-platform_detect.patch
Patch298:	rpm-5.4.15-ignore-missing-macro-files.patch
Patch299:	rpm-5.4.15-update-autoconf-syntax.patch
Patch300:	rpm-5.4.14-tag-generate-endian-conversion-fix.patch
Patch301:	rpm-5.4.14-showrc-memleak-workaround.patch
Patch302:	rpmqv_cc_b_gone.patch
Patch303:	rpm-5.4.10-payload-use-hashed-inode.patch
Patch304:	rpm-5.4.15-properly-load-password-and-group-for-root-environment.patch
Patch305:	rpm-5.4.14-hardlink-segfault-fix.patch
Patch306:	rpm-5.4.14-fix-platform-and-sysinfo-loading.patch
Patch307:	rpm-5.4.15-rpmpy-dont-uncoditionally-reread-configuration-files.patch
Patch308:	rpm-5.4.15-rubygems.rb-pld-ruby-2.0-fixes.patch
Patch309:	rpm-5.4.15-gem_helper.rb-merge-pld-fixes-for-ruby-2.0-etc.patch
Patch310:	rpm-5.4.15-perl-magic.patch
Patch311:	rpm-5.4.15-strip-away-gnu-suffix-from-host_os-and-target_os-properly.patch
Patch312:	rpm-5.4.15-Fix-find-debuginfo.sh-for-ELF-with-file-warnings.patch
Patch313:	rpm-5.4.15-dont-require-ghost-files-to-be-created-during-build.patch
Patch314:	rpm-5.4.15-add-back-rpmvsf-nodigests_nosignatures.patch
Patch315:	rpm-5.4.15-fix-non-void-function-not-returning-a-value.patch
Patch316:	rpm-5.4.15-dont-use-nested-functions.patch
Patch317:	rpm-5.4.15-fix-implicit-function-declaration-missing-header.patch
Patch318:	rpm-5.4.15-fix-faulty-null-pointer-check-against-sstate-array.patch

BuildRequires:	autoconf >= 2.57
BuildRequires:	bzip2-devel
BuildRequires:	automake >= 1.8
BuildRequires:	elfutils-devel >= 0.154
BuildRequires:	sed >= 4.0.3
BuildRequires:	beecrypt-devel >= 4.2.1-8
BuildRequires:	ed
BuildRequires:	gettext-devel
BuildRequires:	byacc
BuildRequires:	pkgconfig
BuildRequires:	pkgconfig(neon)
BuildRequires:	readline-devel
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	pkgconfig(libssl)
BuildRequires:	pkgconfig(libcrypto)
BuildRequires:	pkgconfig(liblzma) >= 5.1.3alpha
BuildRequires:	pkgconfig(libpcre)
BuildRequires:	pkgconfig(libpcreposix)
BuildRequires:	acl-devel
BuildRequires:	magic-devel
BuildRequires:	pkgconfig(popt) >= 1.15
BuildRequires:	pkgconfig(libxml-2.0)
# we're now building with internal..
#BuildRequires:	pkgconfig(lua)
# needed by internal lua
BuildRequires:	pkgconfig(expat)
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
BuildRequires:	pkgconfig(python) = 2.7 
%endif
%if %{with js}
BuildRequires:	pkgconfig(mozjs185)
%endif
%if %{with ruby}
BuildRequires:	pkgconfig(ruby-1.9)
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
%if %{with ossp_uuid}
BuildRequires:	pkgconfig(ossp-uuid)
%endif
%if %{with augeas}
BuildRequires:	pkgconfig(augeas)
%endif
BuildRequires:	spec-helper >= 0.31.12
BuildRequires:	stdc++-static-devel >= 4.6.2-8
BuildRequires:	elfutils >= 0.154
BuildRequires:	libtool >= 2.4.2-3
# rpm can't be built with clang currently (nested functions)
BuildRequires:	gcc
Requires:	bsdcpio
Requires:	gawk
Requires:	coreutils
Requires:	update-alternatives
Requires:	%{bdb}_recover
Suggests:	%{bdb}-utils
Requires:	%{libname} = %{EVRD}
Conflicts:	rpm-build < 1:5.3.10-0.20110422.3
Requires(pre):	coreutils
%rename		rpmconstant
%rename		multiarch-utils
%rename		rpm-mandriva-setup
%rename		rpm-manbo-setup
Obsoletes:	haskell-macros < 6.4-5

%description
RPM is a powerful command line driven package management system capable of
installing, uninstalling, verifying, querying, and updating software packages.
Each software package consists of an archive of files along with information
about the package like its version, a description, etc.

%package -n	%{libname}
Summary:	Libraries used by rpm
Group:		System/Libraries
# Forcing upgrades of anything else linked against it as rpmdb is incompatible
# with older versions (#61658, comment #136)
Conflicts:	librpm < 5.3
Conflicts:	%{_lib}db5.1 < 5.1.25
Conflicts:	%{_lib}elfutils1 < 0.154
Conflicts:	%{_lib}beecrypt7 < 4.2.1

%description -n	%{libname}
RPM is a powerful command line driven package management system capable of
installing, uninstalling, verifying, querying, and updating software packages.
This package contains common files to all applications based on rpm.

%package -n	%{devname}
Summary:	Development files for applications which will manipulate RPM packages
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	rpm-devel = %{EVRD}
%rename		%{_lib}rpmconstant-devel
Obsoletes:	%{_lib}rpm4.4-devel

%description -n %{devname}
This package contains the RPM C library and header files. These
development files will simplify the process of writing programs
which manipulate RPM packages and databases and are intended to make
it easier to create graphical package managers or any other tools
that need an intimate knowledge of RPM packages in order to function.

This package should be installed if you want to develop programs that
will manipulate RPM packages and databases.

%package -n	%{static}
Summary:	Static libraries for rpm development
Group:		Development/C
Requires:	%{devname} = %{EVRD}

%description -n %{static}
Static libraries for rpm development.

%package	build
Summary:	Scripts and executable programs used to build packages
Group:		System/Configuration/Packaging
Requires:	autoconf
Requires:	automake
Requires:	clang
Requires:	file
Requires:	gcc-c++
Requires:	libtool-base >= 2.4.2-3
Requires:	patch >= 2.5.9-7
Requires:	make
Requires:	unzip
Requires:	elfutils >= 0.152-4
Requires:	rpm = %{EVRD}
%rename		rpm-%{_target_vendor}-setup-build
Requires:	spec-helper >= 0.31.12
Requires:	rpmlint-%{_target_vendor}-policy >= 0.3.2
%if %{without bootstrap}
Requires:	python-rpm = %{EVRD}
%if "%{distepoch}" < "2015.0"
Requires:	python-pkg-resources
BuildRequires:	python-pkg-resources
%define	py2_platsitedir	%py_platsitedir
%else
Requires:	python2-pkg-resources
Requires:	python-pkg-resources
BuildRequires:	python2-pkg-resources
%endif
%endif
Requires:	pkgconfig
# ditch to eliminate dependency on perl deps not part of standard perl library
# also kinda wanna discourage heavy adoption of embedded perl interpreter
#Requires:	perl-RPM = %{EVRD}
Conflicts:	rpmlint < 1.4-4
Conflicts:	multiarch-utils < 1:5.3.10
Conflicts:	rpm < 1:5.4.4-32
%rename		rpm-manbo-setup-build
%rename		rpm-mandriva-setup-build
# avoid depnendencies outside of standard perl library, rather make optional
%define __noautoreqfiles %{_rpmhome}/bin/pom2spec
Suggests:	perl(LWP::UserAgent) perl(XML::LibXML)

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
Requires:	perl(IO::String)

%description -n perl-%{perlmod}
The RPM Perl module provides an object-oriented interface to querying both
the installed RPM database as well as files on the filesystem.

%package -n	perl-RPMBDB
Summary:	Perl extension for accessing certain Berkeley DB functionality
Group:		Development/Perl
Requires:	%{libname} = %{EVRD}

%description
This perl extension provides certain Berkeley DB functionality used by urpmi.
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
%setup -q -a5
mkdir platform
pushd platform
# breaks on arm?!?!
%{_target_platform}-ar x %{SOURCE3}
popd
%patch111 -p1 -b .script_macros~
# These patches has been commited hastily upstream for review,
# keeping them around here for now untill finished...
%patch2 -p1 -b .scriptlet~
%patch3 -p1 -b .doc_conflicts~
%patch11 -p1 -b .ru~
%if 0
%patch15 -p1 -b .trigger_once~
%endif
%patch6 -p1 -b .keyserver~
%patch7 -p1 -b .libexec~
%patch29 -p1 -b .specfile~
%patch31 -p1 -b .rpm_qa~
#%%patch32 -p1 -b .clean~
%patch34 -p1 -b .ordering~
%patch37 -p1 -b .drop_deps~
%patch40 -p1 -b .pc_paths~
%patch42 -p1 -b .glob~
%patch46 -p1 -b .repackage~
%patch47 -p1 -b .overlap~
%patch48 -p1 -b .suggests~
%patch55 -p1 -b .strip_reloc_debug~
%patch61 -p1 -b .epoch_cmp~
%patch63 -p1 -b .buildroot_dups~
%patch64 -p1 -b .dups_terminate~
%patch65 -p1 -b .subdir_terminate~
%patch66 -p1 -b .withoutclean~
%patch67 -p1 -b .strip_silent~
%patch69 -p1 -b .oneshot~
%patch70 -p1 -b .drop_basedeps~
%patch71 -p1 -b .locale~
%patch74 -p1 -b .builddir~
%patch76 -p1 -b .twice_terminate~
%patch77 -p1 -b .db52~
%patch78 -p1 -b .ruby19~
%patch79 -p1 -b .range_nooverlap~
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
%patch106 -p1 -b .link_loop~
%patch107 -p1 -b .python_color~
%patch109 -p1 -b .uclibc_nolib64~
%patch110 -p1 -b .req_devel~
%patch112 -p1 -b .gnu_hash~
%patch113 -p1 -b .depoch_rpmlib~
%patch114 -p1 -b .no_verdepfeat~
%patch116 -p1 -b .skip_doc~
%patch117 -p1 -b .exec_modules~
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
%patch143 -p1 -b .mono_newline~
%patch144 -p1 -b .urpm~
%patch146 -p1 -b .nosig~
%patch150 -p1 -b .i18n_str~
%patch151 -p1 -b .noi18n~
#patch152 -p1 -b .l10ndir~
%patch156 -p1 -b .php_deps~
%patch157 -p1 -b .perl_deps~
%patch158 -p1 -b .dl_error~
%patch159 -p1 -b .ignorearch~
%patch138 -p1 -b .trigtrans~
%patch160 -p1 -b .xz_level~
%patch161 -p1 -b .uclibc_buildroot~
%patch162 -p1 -b .uninitialized~
#patch163 -p1 -b .mdk~
%patch164 -p1 -b .verbosebuilds~
%patch165 -p1 -b .helper_order~
%patch166 -p1 -b .ldflags~
%patch167 -p1 -b .perl_abiver~
%patch168 -p1 -b .perl_abireq~
%patch169 -p1 -b .brpcomp~
%patch170 -p1 -b .archtagged~
%patch171 -p1 -b .ruby_utf8~
%patch172 -p1 -b .debug_path~
%patch173 -p1 -b .debugedit_memleaks~
%patch174 -p1 -b .debugedit_errmsg~
%patch175 -p1 -b .doc_post~
%patch176 -p1 -b .droprpath~
%patch178 -p1 -b .cross~
%patch179 -p1 -b .rpmdbchk~
%patch180 -p1 -b .typecast~
%patch181 -p1 -b .printspec~
%patch182 -p1 -b .drop_rpmsetup~
%patch183 -p1 -b .strip_ldflags~
%patch184 -p1 -b .legacy_macros~
%patch185 -p1 -b .buildid_deps~
%patch188 -p1 -b .gstreamer1.0~
%patch189 -p1 -b .envvars~
%patch190 -p1 -b .norpath~
%patch191 -p1 -b .rename~
%patch192 -p1 -b .mem_assert~
%patch193 -p1 -b .xrealloc~
%patch194 -p1 -b .cb~
%patch195 -p1 -b .cb2~
%patch197 -p1 -b .permissive~
%patch198 -p1 -b .rpmdbnofsync~
%patch199 -p1 -b .fontdep_sure~
%patch200 -p1 -b .unsilent~
%patch201 -p1 -b .syslog~
%patch203 -p1 -b .subpackage_errors~
%patch204 -p1 -b .python3~
#patch205 -p1 -b .squir_ver~
%patch209 -p1 -b .rpmluaprint~
%patch210 -p1 -b .rpmpythonmod~
%patch211 -p1 -b .rpmpythontrunc~
%patch212 -p1 -b .static~
%patch215 -p1 -b .tok_free~
%patch216 -p1 -b .xmalloc~
%patch217 -p1 -b .libpackage~
%patch219 -p1 -b .etcrpm~
%patch221 -p1 -b .aarch64_multiarch~
%patch222 -p1 -b .update_config.subguess~
%patch223 -p1 -b .cmakedeps~
#patch224 -p1 -b .ro~
%patch225 -p1 -b .armx~
%ifnarch %{arm}
%patch226 -p1 -b .multithread~
%endif
%patch227 -p1 -b .outputsync~
%patch228 -p1 -b .timestamps~
%patch229 -p1 -b .str_term~
%patch230 -p1 -b .str_overlap~
%patch231 -p1 -b .pcnomuteerr~
%patch232 -p1 -b .exitifnone~
%patch233 -p1 -b .noarb~
%patch234 -p1 -b .querynoise~
%patch235 -p1 -b .fixfdigests~
%patch236 -p1 -b .asciinullterm~
#patch237 -p1 -b .broken_verify~
%patch238 -p1 -b .lua_posix~
%patch239 -p1 -b .gst_typo~
%patch240 -p1 -b .openmp~
%patch241 -p1 -b .closefds~
%patch242 -p1 -b .fixintlua~
%patch243 -p1 -b .rubyarchdirs~
%patch244 -p1 -b .rubyabiver~
%patch245 -p1 -b .gem_spec~
%patch246 -p1 -b .rubygems2~
%patch247 -p1 -b .ruby_macros~
%patch248 -p1 -b .no_ruby_version~
#patch249 -p1 -b .fixembtypo~
%patch250 -p1 -b .rpmlua_internal~
%patch251 -p1 -b .order~
%patch252 -p1 -b .deprecate_epoch~
%patch253 -p1 -b .twiddle~
%patch254 -p1 -b .ne_redirect~
%patch255 -p1 -b .silence_char_type~
%patch256 -p1 -b .preserve_tag_type~
%patch257 -p1 -b .namespace~
%patch258 -p1 -b .gpg_parsing~
%patch259 -p1 -b .interpreter_script~
%patch260 -p1 -b .missing_types~
%patch261 -p1 -b .unglobal~
%patch262 -p1 -b .unpkg_dirdups~
%patch263 -p1 -b .debugedit_segv~
%patch264 -p1 -b .large_bss~
%patch265 -p1 -b .clean_paths~
%patch266 -p1 -b .srcfilename~
%patch267 -p1 -b .configure2_5x~
%patch268 -p1 -b .dlopen_req~
%patch269 -p1 -b .rundir~
%patch270 -p1 -b .nodefaultdocdir~
%patch271 -p1 -b .noassert~
%patch272 -p1 -b .remove_all_deptags~
%patch273 -p1 -b .missing_prototype~
%patch274 -p1 -b .perlembed_typo~
%patch275 -p1 -b .fix_rpmpython_conds~
%patch276 -p1 -b .system_header~
%patch277 -p1 -b .multiarch~
%patch278 -p1 -b .fortify~
%patch279 -p1 -b .clangdefault~
%patch280 -p1 -b .file~
%patch281 -p1 -b .python3~
%patch282 -p1 -b .sameToolchain~
%patch283 -p1 -b .configUpdate~
%patch284 -p1 -b .Oz~
%patch285 -p1 -b .mklibname_fix~
%patch286 -p1 -b .rubygems2.2
%patch287 -p1 -b .morerubygems2
%patch288 -p1 -b .urlgetfile~
%patch289 -p1 -b .tar~
%patch290 -p1 -b .rpmds_offbyone~
%patch291 -p1 -b .no_conf_target_host_build~
%patch292 -p1 -b .sharedstatedir~
%patch293 -p1 -b .tpm_ac~
%patch294 -p1 -b .EVRD~
%patch295 -p1 -b .lib_soname~
%patch296 -p1 -b .noc99_types~
%patch297 -p1 -b .platform_detect~
%patch298 -p1 -b .ignore_missinc_macros~
%patch299 -p1 -b .ac_syntax~
%patch300 -p1 -b .tag_endian~
# ???
#patch301 -p1 -b .showrc_memleak~
%patch302 -p1 -b .rpmqv_cc~
%patch303 -p1 -b .hashed_inode~
%patch304 -p1 -b .init_pw_gr~
%patch305 -p1 -b .hardlink_segafault~
%patch306 -p1 -b .platform_sysinfo~
%patch307 -p1 -b .py_confread~
#disabled as it breaks the way we have things (empty version number as per fedora)
#patch308 -p1 -b .pld_ruby20~
#disabled as it breaks building extensions on ruby 2.2
#patch309 -p1 -b .pld_gemhelper_ruby20~
%patch310 -p1 -b .perl-magic~
%patch311 -p1 -b .strip_gnu~
%patch312 -p1 -b .debuginfo_too_many_notes~
%patch313 -p1 -b .noghost~
%patch314 -p1 -b .rpmvsf~
%patch315 -p1 -b .return_type~
%patch316 -p1 -b .nested_func~
%patch317 -p1 -b .implicit_func_decl~
%patch318 -p1 -b .sstate_check~

#required by P55, P80, P81, P94..
./autogen.sh

# (proyvind): hack around to force static linking against liblzma because of
# it's unstable multithreading API & ABI
sed -e 's#-llzma#-Wl,-Bstatic,-llzma,-Bdynamic#g' -i configure

%build
# XXX:
# building rpm with clang breaks it due to strict aliasing issue at psm.c:1065
#    pid = rpmsqFork(&psm->sq);
# triggered by execution of package scriptlets....
export CC=gcc
export CXX=g++
export __PYTHON=%{_bindir}/python2
export CONFIGFILES=""
# this should really have been fixed by P240, but for some reason this no
# longer seems to be the case
LDFLAGS="-fopenmp" \
%configure	--enable-nls \
		--enable-shared \
		--enable-static \
		--with-pic \
%if %{with debug}
		--enable-debug \
		--with-valgrind \
%endif
		--enable-posixmutexes \
%if %{with python}
		--with-python=%{python_version} \
		--with-python-inc-dir="$(${__PYTHON} -c 'from distutils.sysconfig import get_python_inc; print get_python_inc()')" \
		--with-python-lib-dir="$(${__PYTHON} -c 'from distutils.sysconfig import get_python_lib; print get_python_lib(1)')" \
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
		--with-dbabi=db \
		--with-dbsql=external \
		--without-db-tools-integrated \
%if %{with sqlite}
		--with-sqlite=external \
%else
		--without-sqlite \
%endif
%if %{with ossp_uuid}
%if 0
# TODO: needs to be fixed properly for automatic detection in internal lua build
%endif
		--with-uuid=%{_libdir}:%{_includedir}/ossp-uuid \
%else
		--without-uuid \
%endif
%if %{with augeas}
		--with-augeas=external \
%else
		--without-augeas \
%endif
%if 0
# (tpg) this file name should be changed to something like distro.macros
		--with-extra-path-macros=%{_usrlibrpm}/macros.d/mandriva \
%else
		--with-extra-path-macros=%{_usrlibrpm}/platform/%%{_target}/macros:%{_sysconfdir}/rpm/macros.d/*.macros:%{_usrlibrpm}/macros.d/mandriva \
%endif
		--with-rundir=/run \
		--with-vendor=mandriva \
		--enable-build-warnings \
		--with-platform-detect=yes \
		--with-multiarch

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

%if %{with perl}
pushd RPMBDB-*
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}" CCCDLFLAGS="-fno-PIE -fPIC"
sed -i -e 's,-fPIC -fno-PIE,-fno-PIE -fPIC,g' ../perl/Makefile.perl
%make
popd
%endif

%check
make check

%install
%makeinstall_std
%if %{with perl}
%makeinstall_std -C RPMBDB-*
%endif

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
for f in %{py2_platsitedir}/poptmodule.a %{py2_platsitedir}/_rpmmodule.a \
	%{py2_platsitedir}/rpm/*.a %{_rpmhome}/*.a %{_rpmhome}/lib/*.a\
	%{_rpmhome}/{Specfile.pm,cpanflute2,cpanflute,sql.prov,sql.req,tcl.req} \
	%{_rpmhome}/{config.site,cross-build,rpmdiff.cgi} \
	%{_rpmhome}/trpm %{_bindir}/rpmdiff; do
	rm -f %{buildroot}$f
done

%find_lang %{name} --with-man --all-name

mkdir -p %{buildroot}/var/lib/rpm/{log,tmp}
for dbi in `./rpm --macros macros/macros --eval %_dbi_tags_4|tr : ' '` __db.00{0..9}; do
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

for i in platform/*macros; do
    install -m644 $i -D %{buildroot}%{_usrlibrpm}/platform/$(echo `basename $i`|sed -e 's#\.#/#g')
done
 
install -m644 %{SOURCE4} -D %{buildroot}%{_sysconfdir}/%{name}/macros.d/legacy_compat.macros
install -m755 %{SOURCE6} -D %{buildroot}%{_rpmhome}/git-repository--after-tarball
install -m755 %{SOURCE7} -D %{buildroot}%{_rpmhome}/git-repository--apply-patch

%if %{with docs}
install -d %{buildroot}%{_docdir}/rpm
cp -r apidocs/html %{buildroot}%{_docdir}/rpm
%endif

install -d %{buildroot}%{multiarch_bindir}
install -d %{buildroot}%{multiarch_includedir}
%if "%{_lib}" == "lib64"
%ifnarch aarch64
install -d %{buildroot}%(linux32 rpm -E %%{multiarch_bindir})
install -d %{buildroot}%(linux32 rpm -E %%{multiarch_includedir})
%else
install -d %{buildroot}
install -d %{buildroot}%{multiarch_includedir}
%endif
%endif

# should really be handled by make script..
ln -f %{buildroot}%{_rpmhome}/bin/{rpmlua,lua}
ln -f %{buildroot}%{_rpmhome}/bin/{rpmluac,luac}

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
%{_rpmhome}/bin/rpmdbchk
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
%dir %{_rpmhome}/lib
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
%{_rpmhome}/bin/api-sanity-checker.pl
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
%{_rpmhome}/desktop-file.prov
%{_rpmhome}/find-debuginfo.sh
%{_rpmhome}/find-lang.sh
%{_rpmhome}/find-prov.pl
%{_rpmhome}/find-provides.perl
%{_rpmhome}/find-req.pl
%{_rpmhome}/find-requires.perl
%{_rpmhome}/fontconfig.prov
%{_rpmhome}/gem_helper.rb
%{_rpmhome}/getpo.sh
%{_rpmhome}/git-repository--after-tarball
%{_rpmhome}/git-repository--apply-patch
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
%{_rpmhome}/cmakedeps.sh
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

%files -n %{libname}
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

%files -n %{devname}
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

%files -n %{static}
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

%files -n perl-RPMBDB
%{perl_vendorarch}/RPMBDB.pm
%dir %{perl_vendorarch}/auto/RPMBDB
%{perl_vendorarch}/auto/RPMBDB/RPMBDB.so
%endif

%if %{with python}
%files -n python-rpm
%if %{with embed}
%{_rpmhome}/lib/rpmpython.so
%endif
%dir %{py2_platsitedir}/rpm
%{py2_platsitedir}/rpm/*.py
%{py2_platsitedir}/rpm/*.so
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
