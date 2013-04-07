%define	_target_vendor mandriva

%bcond_with	bootstrap
%bcond_with	debug
# Use --with moondrake for Moondrake branding
# anything else for OpenMandriva branding
%bcond_with	moondrake

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

%define libver		5.4
%define	minorver	10
%define	srcver		%{libver}.%{minorver}
#define	prereldate	20110712

%define librpmname	%mklibname rpm %{libver}
%define librpmnamedevel	%mklibname -d rpm
%define	librpmstatic	%mklibname -d -s rpm

Summary:	The RPM package management system
Name:		rpm
Epoch:		1
Version:	%{libver}.%{minorver}
Release:	%{?prereldate:0.%{prereldate}.}35
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
Source3:	cpu-os-macros.tar
Source4:	legacy_compat.macros
Source5:	RPMBDB-0.1.tar.xz
Source6:	git-repository--after-tarball
Source7:	git-repository--apply-patch
# already merged upstream
Patch0:		rpm-5.3.8-set-default-bdb-log-dir.patch
# TODO: should be disable for cooker, packaging needs to be fixed (enable for legacy compatibility)
# status: to be removed later..
Patch1:		rpm-5.3.8-dependency-whiteout.patch
# TODO: make conditional & disabled through macro by default (enable for legacy compatibility)
# status: to be removed later
Patch2:		rpm-5.4.9-non-pre-scripts-dont-fail.patch
# status: to be removed later
Patch3:		rpm-5.4.9-no-doc-conflicts.patch
# if distsuffix is defined, use it for disttag (from Anssi)
# status: merged upstream IIRC, could probably be dropped
Patch4:		rpm-5.3.8-disttag-distsuffix-fallback.patch
# ugly hack to workaround disttag/distepoch pattern matching issue to buy some
# time to come up with better pattern fix..
# status: needs to be fixed properly, but can be merged upstream
Patch5:		rpm-5.3.8-distepoch-pattern-hack.patch
# fixes a typo in russian translation (#62333)
# status: needs to be pushed back to the Russian i18n project
Patch11:	rpm-5.4.9-fix-russian-typo.patch
# temporary workaround for issues with file triggers firing multiple times and
# a huge memleak...
# DIE
Patch15:	rpm-5.3.8-fire-file-triggers-only-once.patch
# status: keep as mandriva specific for now
Patch21:	rpm-5.3.12-change-dep-loop-errors-to-warnings.patch
# status: need to be revisited and made sure that we get the correct behaviour,
# regression tests certainly required
Patch22:	rpm-5.3.12-55810-rpmevrcmp-again-grf.patch
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
Patch71:	rpm-5.4.4-fix-rpmconstant-to-always-use-LC_CTYPE-C-for-case-conversion.patch
# $RPM_BUILD_DIR isn't necessarily the same as $PWD, it's %%{_builddir}, not
# %%{_builddir}/%%{?buildsubdir}, messing up paths in debug packages created..
# status: needs to be discussed and investigated a bit better..
Patch74:	rpm-5.4.4-pass-_builddir-properly-to-find-debuginfo.patch
# status: probably okay to merge, but discuss on rpm-devel first
Patch76:	rpm-5.4.10-files-listed-twice-terminates-build.patch
# status: don't merge
Patch77:	rpm-5.4.7-use-bdb-5.2.patch
# status: probably okay to merge
Patch78:	rpm-5.4.9-ruby1.9-fixes.patch
# mdvbz#65269
# status: same as for other dependency generation patches
Patch79:	rpm-5.4.4-dont-consider-ranged-dependencies-as-overlapping-for-removal.patch
# status: ignoree for now
Patch81:	rpm-5.4.5-libsql-conditional.patch
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
Patch94:	rpm-5.4.9-generate-haskell-dependencies.patch
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
Patch101:	rpm-5.4.9-font-provides.patch
# status: idem
Patch102:	rpm-5.4.7-kmod-dependencies.patch
# status: idem
Patch103:	rpm-5.4.10-desktop-provides.patch
# status: probably okay to merge, discuss on rpm-devel first
Patch104:	rpm-5.4.5-skip-dependencies-for-character-devices.patch
# status: ready to merge
Patch105:	rpm-5.4.5-rpmfc-use-strlen-not-sizeof.patch
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
# status: ready to merge
Patch115:	rpm-5.4.7-rpmfc-fix-invalid-free-if-not-_defaultdocdir-set.patch
# status: probably okay to merge
Patch116:	rpm-5.4.10-dont-try-generate-rpmfc-dependencies-from-doc-files.patch
# status: ready to merge
Patch117:	rpm-5.4.7-only-generate-ruby-and-python-deps-for-executables-and-modules.patch
# status: same as for other dep gen patches
Patch118:	rpm-5.4.7-dont-generate-soname-provides-for-dsos-with-no-soname.patch
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
Patch127:	rpm-5.4.9-add-matches-as-arguments-to-triggers.patch
# status: same as for other dep gen patches
Patch128:	rpm-5.4.7-dont-consider-trigger-dependencies-as-overlapping.patch
# status: ready
Patch129:	rpm-5.4.7-fix-minor-memleaks.patch
# status: ready
Patch130:	rpm-5.4.9-mire-fix-strings-lacking-null-terminator.patch
# status: keep locally for now
Patch131:	rpm-5.4.10-dlopen-embedded-interpreters.patch
# status: ready
Patch132:	rpm-5.4.9-rpmpython-fix-input.patch
# status: same as for other dep gen patches
Patch133:	rpm-5.4.7-generate-devel-provides-outside-of-libdirs.patch
# status: ready
Patch134:	rpm-5.4.7-actually-perform-linking-against-internal-lua.patch
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
Patch138:	rpm-5.4.10-trigtrans.patch
# status: probably ready to merge, discuss on rpm-devel first
Patch139:	rpm-5.4.9-fix-verify-segfault.patch
# status: keep locally
Patch140:	rpm-5.4.7-rpmv3-support.patch
# status: ready
Patch143:	rpm-5.4.7-mono-find-requires-strip-newlines.patch
# status: ready
Patch144:	rpm-5.4.8-URPM-build-fix.patch
# status: undefined
Patch145:	rpm-5.4.8-add-armv7l-specific-macros.patch
# status: keep locally, might drop this one later..
Patch146:	rpm-5.4.9-support-signatures-and-digest-disablers.patch
# status: undefined
Patch147:	rpm-5.4.9-add-x32-macros.patch
# status: ready and should be merged
Patch149:	rpm-5.4.9-fix-typo-in-rpmtag-header.patch
# status: can be merged, but doesn't really matter as it's to be removed and
# we now anyways disable the support in question..
Patch150:	rpm-5.4.9-dont-remap-i18n-strings-if-enabled.patch
# status: just keep around and toss away when ripped out upstream...
Patch151:	rpm-5.4.9-disable-support-for-i18nstring-type.patch
# lack insight on actual functionality, which anyways seems broken, so let's
# disable it to avoid errors from berkeley db..
# status: keep locally
Patch152:	rpm-5.4.9-disable-l10ndir.patch
# drop this dead macro
# status: ready
Patch154:	rpm-5.4.9-drop-dead-cputoolize-macro.patch
# idem
Patch155:	rpm-5.4.9-ditch-install-info-macros.patch
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
Patch177:	rpm-5.4.10-automake-1.13.patch
Patch178:	rpm-5.4.10-crosscompile.patch
# tool for automatically checking and fixing broken rpmdb
# status: probably' worth merging upstream
Patch179:	rpm-5.4.10-rpmdbchk.patch
# adds casts for C++ compatibility
# status: ready
Patch180:	rpm-5.4.10-rpmdb-typecasts.patch
# adds ability for printing parsed version of spec file with 'rpm -q --specfile --printspec'
# status: very simple, non-intrusive, while quite convenient, should be okay to merge
Patch181:	rpm-5.4.10-printspec.patch
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
# backport from upstream
Patch186:	rpm-5.4.10-dont-repackage-if-justdb-is-specified.patch
# backport from upstream
Patch187:	rpm-5.4.10-adjust-trigger-counts-for-delayed-commit.patch
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
# this fixes tagSwab to properly handle RPM_UINT64_TYPE, fixing headerPut with
# status: ready
Patch196:	rpm-5.4.10-fix-64bit-tagSwab.patch
Patch197:	rpm-5.4.10-dont-require-group-and-summary-tag-during-build.patch
Patch198:	rpm-5.4.10-enable-nofsync-for-rpm-rebuilddb.patch
Patch199:	rpm-5.4.10-fix-font-dep-misidentification.patch

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
BuildRequires:	pkgconfig(liblzma)
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
BuildRequires:	pkgconfig(python)
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
Conflicts:	%{_lib}elfutils1 < 0.154
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
%rename		rpm-%{_target_vendor}-setup-build
Requires:	spec-helper >= 0.31.12
Requires:	rpmlint-%{_target_vendor}-policy >= 0.3.2
%if %{without bootstrap}
Requires:	python-rpm = %{EVRD}
Requires:	python-pkg-resources
BuildRequires:	python-pkg-resources
%endif
Requires:	pkgconfig
# ditch to eliminate dependency on perl deps not part of standard perl library
# also kinda wanna discourage heavy adoption of embedded perl interpreter
#Requires:	perl-RPM = %{EVRD}
Conflicts:	rpmlint < 1.4-4
Conflicts:	multiarch-utils < 1:5.3.10
Conflicts:	rpm < 1:5.4.4-32
Obsoletes:	rpm5-manbo-setup
%rename		rpm-manbo-setup-build
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
Requires:	%{librpmname} = %{EVRD}

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
#%%patch21 -p1 -b .loop_warnings~
#%%patch22 -p1 -b .55810~
#patch27 -p1 -b .mdv~
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
#patch81 -p1 -b .libsql~
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
#patch140 -p1 -b .rpmv3~
%patch143 -p1 -b .mono_newline~
%patch144 -p1 -b .urpm~
%patch146 -p1 -b .nosig~
%patch147 -p1
%patch149 -p1 -b .typo~
%patch150 -p1 -b .i18n_str~
%patch151 -p1 -b .noi18n~
%patch152 -p1 -b .l10ndir~
%patch154 -p1 -b .cputoolize~
%patch155 -p1 -b .install_info~
%patch156 -p1 -b .php_deps~
%patch157 -p1 -b .perl_deps~
%patch158 -p1 -b .dl_error~
%patch138 -p1 -b .trigtrans~
%patch159 -p1 -b .ignore_arch~
%patch160 -p1 -b .xz_level~
%patch161 -p1 -b .uclibc_buildroot~
%patch162 -p1 -b .uninitialized~
%patch163 -p1 -b .mdk~
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
%patch177 -p1 -b .automake13~
%patch178 -p1 -b .cross~
%patch179 -p1 -b .rpmdbchk~
%patch180 -p1 -b .typecast~
%patch181 -p1 -b .printspec~
%patch182 -p1 -b .drop_rpmsetup~
%patch183 -p1 -b .strip_ldflags~
%patch184 -p1 -b .legacy_macros~
%patch185 -p1 -b .buildid_deps~
%patch186 -p1 -b .rpkg_justdb~
%patch187 -p1 -b .trig_cnt~
%patch188 -p1 -b .gstreamer1.0~
%patch189 -p1 -b .envvars~
%patch190 -p1 -b .norpath~
%patch191 -p1 -b .rename~
%patch192 -p1 -b .mem_assert~
%patch193 -p1 -b .xrealloc~
%patch194 -p1 -b .cb~
%patch195 -p1 -b .cb2~
%patch196 -p1 -b .ui64p~
%patch197 -p1 -b .permissive~
%patch198 -p1 -b .rpmdbnofsync~
%patch199 -p1 -b .fontdep_sure~

#required by P55, P80, P81, P94..
./autogen.sh

mkdir -p cpu-os-macros
tar -xf %{SOURCE3} -C cpu-os-macros
%patch145 -p1

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

%if %{with perl}
pushd RPMBDB-*
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
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
for f in %{py_platsitedir}/poptmodule.a %{py_platsitedir}/rpmmodule.a \
	%{py_platsitedir}/rpm/*.a %{_rpmhome}/*.a %{_rpmhome}/lib/*.a\
	%{_rpmhome}/{Specfile.pm,cpanflute2,cpanflute,sql.prov,sql.req,tcl.req} \
	%{_rpmhome}/{config.site,cross-build,rpmdiff.cgi} \
	%{_rpmhome}/trpm %{_bindir}/rpmdiff; do
	rm -f %{buildroot}$f
done

%find_lang %{name}

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

cp -r cpu-os-macros %{buildroot}%{_usrlibrpm}/platform
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
install -d %{buildroot}%(linux32 rpm -E %%{multiarch_bindir})
install -d %{buildroot}%(linux32 rpm -E %%{multiarch_includedir})
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

%changelog
* Sat Mar 18 2013 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.10-29
- allow to build packages without group or summary tag (P197)
- fix tagSwab to properly handle RPM_UINT64_TYPE to work with headerPut (P196)
- add enum for RPMCALLBACK_INST_STOP callback event (P195)
- implement scriptlet start and stop callbacks (P194, rhbz#606239)
- fix "memory alloc (0 bytes) returned NULL." when trying to query an
  existing package name with an extra '-' behind it
- do assert rather than just exit on mem alloc failure so that we can get
  backtrace for debugging (P192)

* Sun Feb 24 2013 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.10-28
- add optional second argument for specifying a specific version to %%rename
- pass --disable-dependency-tracking & --disable-rpath to %configure by default

* Thu Feb 21 2013 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.10-27
- fix so that %%trigger{pre,post}trans{in,un,prein,preun) triggers doesn't
  fire %%trigger* triggers as well

* Wed Feb 20 2013 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.10-26
- add back $RPM_ARCH & $RPM_PACKAGE_NAME (required by aot-compile)

* Fri Jan 25 2013 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.10-25
- fix gstreamer dependencies generator and update it for gstreamer1.0 (P188)

* Fri Jan 25 2013 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.10-20
- add dependency on pkgconfig to rpm-build
- fix regression in %%before_configure macro

* Wed Jan 16 2013 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.10-19
- adjust trigger counts for delayed commit (P187)
- fix: don't repackage if --justdb is specified (P186)
- disable elf(buildid) provides as they're currently not used for anything,
  yet as they get generated for every individual executable elf binary
  they make up 1/4 of all provides generated for all packages on my local
  system(!) (P185)
- clean out some ancient legacy mandriva specific macros (P184)
- drop linker flags from %ldflags thats now implicitly enabled by default (P183)

- drop remaining legacy scripts from rpm-mandriva-setup-build package for us to
  be able to obsolete it
- drop invokation of fix-libtool-ltmain-from-overlinking for same reason also
- drop invokation of old force-as-needed-for-shared-lib-in-libtool script
  before running configure. --as-needed are now enabled by default in binutils,
  so this is no longer relevant (P182)
- implement 'rpm -q --specfile --printspec' to print parsed spec file (P181)
- add missing typecasts for C++ compatibility in rpmdb.h (P180)

* Wed Jan 16 2013 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.10-18
- add rpmdbchk tool for automatically fixing broken rpmdb (P179)
- add a RPMBDB perl module with necessary functions using berkeley db api
  exported, ensured to be buitl against same as rpm, thus preventing breakage
  during upgrade

* Mon Jan  7 2013 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.10-17
- "finish" implementation of %%triggerpretransin, %%triggerpretransun,
  %%triggerposttransin, %%triggerposttransun triggers (P138)
- convert explicit perl-IO-String dependency to canonical perl(IO::String)
- get rid of rpath from perl module (P176)
- reenable regression tests again as network access is working just fine from
  build environment on ABF
- make fix_eol script run after %%doc, so that wrong-file-end-of-line-encoding
  gets fixed for files installed after %%install as well (P175)
- convert some more foo-devel buildrequires to pkgconfig(foo) deps
- print more meaningful error message for debugedit "shrank by one"
  (P174, from Thierry Vignaud)
- fix a couple of memleaks in debugedit (P173)
- replace debugedit patch, rather just resolve absolute path to %%_builddir
  when setting $RPM_BUILD_DIR so that debugedit doesn't burn and crash (P172)

  + Bernhard Rosenkraenzer <bero@lindev.ch>
    - Add support for crosscompiling (P177)
    - Fix automake 1.13 warnings (P178)

* Thu Dec 27 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.10-16
- fix debugedit issues with certain paths, resulting in debuginfo packages
  without sources (P172, from Guilherme Destefani)

* Wed Dec 26 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.10-15
- set LC_CTYPE as UTF-8 when building gem (P171, from Funda)
- modify arch_tagged macro to use ()(64bit) instead of (lib64), to be
  compatible with the mark64 provides generated by find-provides (P170,
  from blino)
- update brp-compress script for us to replace our own locally maintained
  compress-files from spec-helper (P169)

* Wed Dec 19 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.10-14
- drop dependency on perl-RPM in rpm-build
- avoid perl dependencies outside of perl standard library in rpm-build

* Mon Nov 05 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.10-10
+ Revision: 821918
- drop rpmv3 compatibility patch due to security concerns
- fix %%ldflags issue when %%configure is used more than once within a spec (P166)

* Tue Oct 30 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.10-8
+ Revision: 820705
- darnfudgit, forgot to remove exclusivearch workaround..

* Tue Oct 30 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.10-7
+ Revision: 820703
- fix so that spec-helper scripts gets run before find-debuginfo.sh so that any
  file permissions fixed it relies gets done first (P165)

* Mon Oct 29 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.10-6.1
+ Revision: 820313
- try sneak around bs bs with x86_64 exclusive build

* Mon Oct 29 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.10-6
+ Revision: 820284
- pass --disable-silent-rules to configure so that we'll by default always get
  consistent behaviour of verbose build output (P164)
- change name otherwise as well..
- change disttag to 'mdk'

* Thu Oct 04 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.10-5
+ Revision: 818380
- fix duplicate /usr/lib/rpm/bin/{{rpmlua,lua},{rpmluac,luac} files to be
  hardlinks in stead
- own /usr/lib/rpm/lib
- fix a possibly unitialized variable being used (P162)
- search through library dirs within buildroot for uclibc dependencies (P161)

* Thu Aug 30 2012 Andrey Bondrov <abondrov@mandriva.org> 5.4.10-4
+ Revision: 816074
- Update ruby1.9-fixes patch to deal with new psych

* Wed Aug 22 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.10-3
+ Revision: 815594
- bump binary payload compression level up to xz' default level (6)
- fix so that dependencies really doesn't get generated from doc files, also
  allow for enabling generation with %%_generate_dependencies_from_docdir (P116)

* Tue Aug 14 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.10-2
+ Revision: 814815
- rebuild for missing x86_64 packages..

* Fri Jul 27 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.10-1
+ Revision: 811384
- support --ignorearch & --ignoreos again (P159)
- try workaround strange issue with tests being run during install when built
  on build server...
- new version

* Wed Jul 04 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.9-6
+ Revision: 808116
- fix issue with noen saving error pages to target file when hitting errors
  after connecting to http server (P158)
- change %%optflags for x32 to '-Os -g -mx32 -march=atom -mtune=core-avx-i'
- merge perl dependency generator scripts from rpm-mandriva-setup
- merge php dependency generator scripts from rpm-mandriva-setup-build
- ditch install-info macros
- drop dead %%cputoolize macro (P154)

* Sat May 19 2012 Matthew Dawkins <mattydaw@mandriva.org> 5.4.9-5
+ Revision: 799683
- added p153 for findlang of the new gnome help directory
- taken from upstream rpm5.org

* Fri May 18 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.9-4
+ Revision: 799528
- disable sqlite stuff which seems broken, giving berkeley db errors (P152)
- disable support for localized strings (P150)

* Fri May 18 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.9-3
+ Revision: 799483
- fix broken description, group & summary tag for src.rpms generated (P150)
- fix a typo in the internal rpmtag.h header (P149)
- fix build breakage due to use of libgit2 functions when not enabled (P148)
- add initial x32 support (P147)

* Thu May 17 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.9-2
+ Revision: 799292
- add back fix for 'rpm -qa \*foo\*' which were wrongly assumed to have been
  merged upstream

* Thu May 17 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.9-1
+ Revision: 799275
- support signature & digest disablers
- Seqno is now part of %%_dbi_tags_4, so be sure to not make it duplicate in
  %%files list
- rebase on rpm 5.4.9 (tons of patches merged upstream, beware of possible
  regressions..)
- prepare and comment with instructions and status for mdawkins to take care
  of upstream merging :)

  + Franck Bui <franck.bui@mandriva.com>
    - clean up the armv7l macro file so it contains target-specific macros only
    - Add armv7l specific macros

* Wed Apr 25 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.8-1
+ Revision: 793419
- fix lua ossp-uuid as well
- fix uuid being disable (enabling it for real)
- * fix some regressions
  * regenerate patches
  * update to 5.4.8
- fix newline from mono dependency generator which will produce empty deps (P143)

* Sat Apr 21 2012 Matthew Dawkins <mattydaw@mandriva.org> 5.4.7-14
+ Revision: 792633
- added p142 for typelib (rediffed from upstream)
- made spec more readable

* Thu Apr 12 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.7-13
+ Revision: 790449
- revert "Hash instead of 64b->16b truncate to prevent aliasing" (P141)

* Thu Apr 12 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.7-12
+ Revision: 790425
- disable %%triggerposttransin & %%triggerposttransun support for now as
  implementation details likely needs to change in ways that will affect any
  packages built using this
- add back support for rpmv3 packages (#65443)
- fix --verify segfaulting on packages using old signature type (#64378)
- implement %%triggerposttransin  & %%triggerposttransun (P138)

* Thu Mar 29 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.7-11
+ Revision: 788049
- fix dependency generator not generating kmod() deps for all dkms packages
- fix so that we don't get double '/' in path for dirname matching against
  file triggers (P137)
- add support for using rpmdsMerge() with file path tags (P136)

* Wed Mar 28 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.7-10
+ Revision: 787993
- libexpat is needed by lua, so let's enable use of libexpat for rpm as well also
- don't do seqid_init() on read-only database (P135)
- enable internal lua per jbj request

* Fri Mar 23 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.7-9
+ Revision: 786436
- allow generating devel() provides for files outside of standard libdirs (P133)
- fix rpmpython input issue resulting in 'BDB4511 Error' (P132)
- merge all interpreter dlopen() patches into one
- add dependencies on python-rpm & perl-RPM for rpm-build package so that we're
  sure that we always have embedded python & perl interpreters available during
  rpm building, thus making it easier and encouraging usage
- pass trigger matches as arguments to triggers using embedded interpreters also
- load embedded squirrel interpretter via dlopen() (P135)
- load embedded tcl interpreter via dlopen() (P134) and enable it
- implement loading of embedded ruby interpreter via dlopen() (P133), disabled
  for now as the embedded interpreter support was already broken and I don't want
  to waste anymore time on trying to fix it right now.. :p
- load embedded perl interpreter via dlopen() (P132) and enable it
- load embedded python interpreter via dlopen() (P131) and enable it

* Thu Mar 22 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.7-8
+ Revision: 785965
- fix regex & glob matching against strings that's not NUL terminated (P130)
- fix a couple of minor memleak (P129)
- don't consider trigger dependencies as overlapping (P128)
- enable provides generation for DSOs without soname again (for now..)
- add matches as arguments to triggers (P127)
- add filename regex matching support for file triggers (P126)
- fix unitialized value resulting in segfault for 'rpm -qa --triggers' (P125)

* Fri Mar 16 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.7-7
+ Revision: 785403
- only generate devel() deps for files under /lib, /lib64, /usr/lib & /usr/lib64

* Fri Mar 16 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.7-6
+ Revision: 785399
- change debug package suffix to '-debuginfo' (P124)
- .la files now gets automatically removed since spec-helper 0.31.12

* Fri Mar 16 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.7-5
+ Revision: 785347
- fix devel() dependencies not being generated if soname has '.' before '.so'
- fix kmod() dependencies not being generated
- own multiarch directories
- don't generate rpmlib(DistEpoch) dependencies quite yet..

* Wed Mar 14 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.7-3
+ Revision: 784990
- pull in fixed libtool version
- don't try fopen() empty filenames when trying to resolve elf interpreter (P123)
- strdup() EVR of package merged while removing overlapping dependencies (P122)
- always choose dependencies with equal only when overlapping (P121)
- print the name of the files that removed dependencies are generated from (P120)

* Sat Mar 10 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.7-2
+ Revision: 783945
- eu-strip in elfutils 0.152-5 seems to have suddenly started segfaulting on me,
  so let's be sure that we pull in 0.153 when we build rpm
- fix generation of ruby(abi) provides (P119)
- don't generate SONAME provides for DSOs without SONAME (P118)
- only generate ruby and python dependencies for executables and modules (P117)
- don't try generate dependencies from any files under /usr/share/doc (P116)
- fix invalid free() if not %%_defaultdocdir is defined (P115)
- don't generate rpmlib(VersionedDependency) rpmlib feature dependencies (P113)
- add rpmlib(DistEpoch) feature (P113, way overdue, should *really* have been
  done before 2011 release in order to prevent broken upgrades.. :/)
- use gnu hash style by default when linking (P112)
- don't bother generating rtld(GNU_HASH) dependencies for packages using gnu
  hash style as our glibc has provided this for ages now anyways (P112)

* Fri Mar 09 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.7-1
+ Revision: 783464
- new version
- reenable docs

* Fri Mar 09 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.5-2
+ Revision: 783454
- disable docs for a brief moment to squeeze by dependenci issues on buildsystem
- set _use_internal_dependency_generator to 1 (disabling scriptlet dependencies)
- only generate devel() dependencies for symlinks with 'libfoo' filename (P110)
- fix generation of uClibc() depsn on non-lib64 (P109)
- fix fontconfig.prov not being installed

* Tue Mar 06 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.5-1
+ Revision: 782550
- be sure to scan /usr/lib{,64} for elf interpreter
- fix issue with pythonegg() dependencies not generated with internal dependency
  generator when egg metadata is stored in directories rather than archives(P108)
- add rpmfc python color from string returned by file magic (P107)
- break out of elf link loops when trying to resolve elf interpreter (P106)
- fix incorrect use of sizeof() rather than strlen() on strings, affecting
  perl dependencies generated by the internal dep generator (P105)
- skip dependency generation for block devices as well..
- don't try extract dependencies from character devices, otherwise the dependency
  generator might get stuck in a eternal loop (P104)
- add mimehandler() provides (P103)
- add missing pieces to get kmod() dependencies working (P102)
- generate font() provides (P101)
- don't consider script dependencies as overlapping to other dependencies (P100)
- add a macros function to python spec class to get macros from a package (P99)
- update dependency references in rpmfc dictionary when removing overlapping
  dependencies (P98)
- cron't script isn't a configuration file
- set proper file color for scripts using env in shellbang (P97)
- fix elf interpreter resolving that breaks generation of uclibc deps (P96)
- drop interpreter deps on 'bash', 'env', 'perl', 'python', 'ruby' & 'sh' (P95)
- oboslete haskell-macros
- generate haskell() dependencies (P94)
- SILENCE: I knew this one was wrong..
- print missing newline for unversioned ruby(abi) dependencies generated (P93)
- be sure to always extract dependencies for all files classified as ruby (P92)
- update rpmfc when removing dependencies on self (P91)
- apply various misc changes for fixing uClibc() dependencies and also devel()
  dependencies (P90)
- fix typo inverting (64bit) mark (P89, from rpm-5_3)
- add a uClibc(...) dependency for libraries linked against uClibc to avoid
  conflicting duplicates (P88, from rpm-5_3)
- ditch librpm-devel provides
- obsolete rpm-mandriva-setup
- don't generate php dependencies only when scripts are executable (P87)
- use our own dependency generator for php as well for now (updates P84)
- update to using version of mono dependency generator shipped with mono (P86)
- fix removal of overlapping dependencies for internal dependency generator (P85)
- enable internal dependency generator (P83)
- remove dependencies on self generated by internal dependency generator as well
- add support for extracting kmod() deps from xz compressed kernel modules
- fix python bindings using a no longer existing rpm4 function (P82)
- apply russian typo fix again (patch seems to have been accidentally disabled)
- fix build against db 5.2 for now.. (P77)
- fix building of libsql not being conditional (P81)
- fix automake 1.11.2 fix (P80)
- new version

* Wed Feb 15 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.4-36
+ Revision: 774475
- do not consider dependency ranges as overlapping for removal (#65269)

* Sun Feb 12 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.4-35
+ Revision: 773377
- update ruby macro for ruby 1.9 to avoid deprecation warnings
- fix gem_helper.rb to work with ruby 1.9

* Fri Feb 10 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.4-34
+ Revision: 772526
- hold on with db 5.3 migration a bit, need to get ruby dep extractor working
  again first...
- fix actual printing of rubygem dependencies also with ruby 1.9
- update rubygem dependency extractor for ruby 1.9
- switch to berkeley db 5.3

* Tue Feb 07 2012 Oden Eriksson <oeriksson@mandriva.com> 5.4.4-33
+ Revision: 771559
- rebuilt against new pcre (second time)

* Sun Feb 05 2012 Oden Eriksson <oeriksson@mandriva.com> 5.4.4-32
+ Revision: 771270
- rebuilt against new pcre

  + Matthew Dawkins <mattydaw@mandriva.org>
    - moved pom2spec to rpm-build package
    - added Obsoletes for rpm5-manbo-setup package

* Mon Jan 23 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.4-31
+ Revision: 766961
- terminate build on file listed twice
- hardcore path to rpmlint to prevent breakage with people redefining %%_bindir
- add rpmlintrc file

* Fri Jan 06 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.4-30
+ Revision: 758125
- workaround spec-helper not properly removing all .la files properly..(?)
- support loading local rpmlint configuration file from
  %%{_sourcedir}/%%{name}.rpmlintrc
- add a versioned dependency on rpmlint-mandriva-policy
- add support for %%_srcdefattr macro, setting it to (644,root,root)
- bump rpmlint version conflicts again.. ;)
- enable %%_nonzero_exit_pkgcheck_terminate_build (ghasp!;)
- don't remove Requires(pre) dependencies satisfied by self, but rather print an
  error (not terminating build though, leaving this up to rpmlint check to do
  later)
- pass '-T' argument to rpmlint for it to always return zero unless error
  threshold is exceeded
- silence rpmlint 'macro-in-comment' complaints
- ditch dedicated rpm user and file/directory ownership of

* Wed Dec 21 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.4-29
+ Revision: 744043
- reenable rpmlint invokation from rpmbuild and add conflict on older rpmlint
  releaes that has bug with paths to extracted files from src.rpm

* Tue Dec 20 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.4-28
+ Revision: 744028
- disable rpmlint invokation during rpmbuild untill network transport issues with
  src.rpms is resolved
- drop 'GROUPS' file carried and included as doc for 'rpm' package, earlier
  required by rpmlint, but no longer... :)

* Tue Dec 20 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.4-27
+ Revision: 743978
- add '>= 4.2.1-8' to 'beecrypt-devel' buildrequires to get proper libtool files
- add back $RPM_BUILD_DIR again for now to properly generate paths for debug pkgs
- add support for %%_build_pkgcheck, rpmbuild invoking rpmlint automatically per
  package built (P73, from rpm.org)
- disable %%_unpackaged_subdirs_terminate_build untill check fixed..
- teach debugedit about .debug_macro dwarf section (rhbz#759272, P72 from rpm.org)
- switch to using rpm's own xtoupper() & xtolower() in stead of changing LC_CTYPE

* Fri Dec 16 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.4-26
+ Revision: 743086
- fix locale-dependent behaviour of toupper()/tolower() breaking conversion of
  string casing and the lookup of rpm constants in languages such as turkish
  where 'i' is considered uppercase and 'I' lowercase (P71, fixes mdv#63860)

* Wed Dec 14 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.4-25
+ Revision: 741297
- change log level of message about dropping dependencies to debug, way too
  annoying otherwise..

* Wed Dec 14 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.4-24
+ Revision: 741197
- actually enable dropping of dependencies on '/bin/sh' & '/sbin/ldconfig' (P70)

* Sun Dec 11 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.4-23
+ Revision: 740189
- drop dependencies such as /bin/sh which will always be satisfied by glibc's
  dependency on bash, and also on /sbin/ldconfig which always will be satisfied
  by glibc (P70)

* Sun Dec 11 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.4-22
+ Revision: 740168
- drop useless dependency on 'pkgconfig' on all files which has a pkgconfig file,
  it's not really needed to make the packages usable, and any package actually
  requiring pkgconfig will pull it in long before anyways (P69)
- fix %%find_lang --with-html
- enable net transport for 'rpm -qp' (closes mdv#64914)

* Tue Dec 06 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.4-21
+ Revision: 738087
- avoid excessive output from eu-strip in find-debuginfo.sh now that
--reloc-debug-sections is used (P67)
- add a 'rpmbuild --withoutclean' option (P66, closes mdvbz#64898)
- strip away buildroot from unpackaged subdirs listed as well
- implement %%_unpackaged_subdirs_terminate_build as well (P65)
- implement %%_duplicate_files_terminate_build (P64)
- strip buildroot path from list of files duplicated across packages (P63)
- update buildrequires on libgomp-devel to gomp-devel
- fix path of %%_sys_macros_dir
- don't redefine %%{debugcflags} completely, extend it in stead and add '-g3'

* Wed Nov 30 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.4-20
+ Revision: 735832
- fix NULL pointer dereferencing
- add a versioned requires on elfutils to ensure we get --reloc-debug-sections

* Wed Nov 30 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.4-19
+ Revision: 735726
- update buildrequires to use pkgconfig(foo)
- fix so that --reloc-debug-sections isn't used when DISABLE_DEBUG is set

* Tue Nov 29 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.4-18
+ Revision: 735479
- fix same package with epoch being possible to upgrade (P60, reported by Ze)

* Tue Nov 29 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.4-17
+ Revision: 735473
- add missing partial stripping part from our old find-debuginfo.sh (P60)
- add -Wa,--compress-debug-sections to %%debugcflags

* Tue Nov 29 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.4-16
+ Revision: 735302
- use DWARF 4 for debugging format (P58)

* Tue Nov 29 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.4-15
+ Revision: 735291
- create GDB index from find-debuginfo if possible (rhbz#617166, from rpm.org)
- add quotes around $RPM_BUILD_ROOT everywhere to avoid breakage with filename
  spaces (P56, from rpm.org)
- add support for stripping out/resolve relocations between .debug_* elf
  sections in ET_REL files. This can save a lot of space for kernel module (P55)
- Add DWARF-4 support to debugedit (rhbz#707677, P54 from rpm.org)
- Bail out of debuginfo if stabs format encountered (rhbz#453506, P53 from rpm.org)
- Remove unused variable in debugedit (P52, from rpm.org)
- fix incorrect error messages regarding -b and -d (P51, from rpm.org/Anssi)
- Make debugedit -i recompute build ID only when any DWARF was actually
  changed (P50, from rpm.org)
- Whitespace fixups for tools/debugedit.c (P49, from rpm.org)

* Sat Nov 26 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.4-14
+ Revision: 733515
- don't show suggests with --requires
- only log as debug message when only merging flags

* Fri Nov 25 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.4-13
+ Revision: 733452
- fix dependencies with different attributes overlapping being removed, they will
  now rather have their attributes merged in stead

* Fri Nov 25 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.4-12
+ Revision: 733368
- fix buggy removal of overlapping dependencies, also add detection warning (P47)

* Thu Nov 24 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.4-11
+ Revision: 733223
- fix build issue caused by libxml libtool files removal
- drop dependency whiteout, time to clean up loops
- allow installation of repackage rpms (P46)
- drop dependency on rpm-mandriva-setup now that it's macros has been merged
- merge build macros from rpm-mandriva-setup-build (P45)
- switch to using xz payload (P44)
- merge remaining common macros from rpm-mandriva-setup package (P44)
- don't redefine %%_vendor and other variables we don't want redefined in
  platform-specific macros
- fix versioned dependencies on rpm-mandriva-setup
- implement support for glob for loading macros with %%{load:} (P42)

* Thu Nov 17 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.4-10
+ Revision: 731397
- don't apply %%clean patch (P32), it seems to be broken..
- merge most of macros from rpm-manbo-setup & obsolete it
- make sure pkgconfig files to extract dependencies from are located in right
  location (P40)
- drop unnecessary 'sort' in find-debuginfo.sh giving (harmless) error (P39)
- make find-lang.sh handle man pages that's compressed (P38)
- drop auto-generated dependencies for packages that they satisfy themself (P37)

* Wed Nov 16 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.4-9
+ Revision: 731099
- fix missing output file with --all-name

* Wed Nov 16 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.4-8
+ Revision: 731068
- support passing multiple names to find-lang.sh (last argument will be output
  file name) (P36)

* Wed Nov 16 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.4-7
+ Revision: 730854
- be sure to rescan for dependency loops again when dependencies has been skipped

* Wed Nov 16 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.4-6
+ Revision: 730839
- add support for --with-html to find-lang.sh (P35)
- fix a memleak in ordering patch, and also report dependencies not being removed
  from tsort relations

* Sun Nov 13 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.4-5
+ Revision: 730423
- apply ordering patch for helping solving dependency loops where ie.
  Requires(post) etc. has been used to try solve ordering with loops.. (P33)

* Sun Nov 13 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.4-4
+ Revision: 730407
- fix mdvbz#62979 again (P33, forgotten on rpm-5_3)
- really always invoke %%clean at end (P32, forgotten on rpm-5_3)

* Sat Nov 12 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.4-3
+ Revision: 730209
- workaround strange issue for lines starting with '%%_'...
- fix rpm -qa \*foo\* regression (P31)

* Fri Nov 11 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.4-2
+ Revision: 730073
- use /sbin/nologin rather than /bin/false as login shell for 'rpm' user
- drop patch reverting $RPM_BUILD_DIR++ removal, it's no longer required as we're
  no longer using our own version of find-debuginfo.sh using this
- add back fix for rpm -qf /unpackaged-file (P30, forgotten on rpm-5_3)
- add %%_specfile macro (P29, commit forgotten on rpm-5_3)
- reenable scriptlet failure & no doc conflict patches (commits forgotten)

* Fri Nov 11 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.4-1
+ Revision: 729992
- merge find-lang.sh changes from rpm.org (P28)
- merge changes from rpm-setup's find-debuginfo.sh (P27)
- new version

* Mon Nov 07 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.3-2
+ Revision: 727143
- add back NVRA pattern hack that got lost on rpm-5_3 branch (P27, fixes urpme)

* Wed Oct 19 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.4.3-1
+ Revision: 705415
- revert removal of env vars breaking ie. find-debuginfo.sh (P26, reverts r16320)
- fix different epoch being ignored for packages with same NVRA compared (P25)
- add %%ruby_sitedir and %%ruby_vendor macros (P24)
- climb up to 5.4 series.. :)
- revert previous patch added, already merged upstream after all..
- revive patch fixing #62262 which got lost earlier
- fix previous hastily reverted patch in a (hopefully) proper way

  + Jon Dill <dillj@mandriva.org>
    - bump release to 13
      - moved various {_rpmhome}/bin/ binaries  to main rpm pkg from rpm-build as defined in /usr/lib/rpm/macros
      - added {_rpmhome}/bin/lua as it was missing from the spec

* Tue Jul 12 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.3.12-0.20110712.2
+ Revision: 689790
- revert a previous commit of mine which broke deps without distepoch (rushed)

* Tue Jul 12 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.3.12-0.20110712.1
+ Revision: 689687
- change errors on dependency loops to warnings
- update to new cvs snapshot:
  	o fixes issues with upgrading packages of same EVR, but different
  	  distepoch
  	o fix /usr/lib/rpm/bin/dbconvert segfaulting when no root is provided
  	o automatically install gstreamer.sh dep genereator

* Wed Jul 06 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.3.12-0.20110625.3
+ Revision: 689009
- install gstreamer.sh dependency generator

* Mon Jul 04 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.3.12-0.20110625.2
+ Revision: 688659
- add a conflicts on older beecrypt version to fix upgrade from 2009.0
- add a conflicts on older elfutils to handle upgrade from 2009.0

* Sat Jun 25 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.3.12-0.20110625.1
+ Revision: 687193
- new cvs snapshot
- add a suggests on db51-utils
- fix broken %%optflags for i686-linux macros (#63517)

  + Matthew Dawkins <mattydaw@mandriva.org>
    - added arm support for rpm5, cpuinfo doesn't support arm

* Wed Jun 01 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.3.11-0.20110525.3
+ Revision: 682280
- add a null pointer check for nvra disttag hack, otherwise we'll easily segfault
- update javascript enabler to pass the right arguments
- come up with a better hack for querying rpmdb for nvra with disttag (ie. urpme
  on plf packages with disttag should now *finally* be working properly..;)
- add buildrequires on db51-utils (required by testsuite)

* Wed May 25 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.3.11-0.20110525.1
+ Revision: 679105
- reenable regression checks
- fix too hasty merged syslog patch (P20)
- don't package *.{a,la} files for python module
- drop '-DXP_UNIX=1' from CPPFLAGS, leftover from internal js build...
- follow s/ossp_uuid/ossp-uuid/ package name change
- update to latest cvs snapshot (for cleaning and also fixes #63318)

* Mon May 16 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.3.10-0.20110422.4
+ Revision: 675030
- fix c++ compatibility in rpmdb.h api (P22)
- fix build of dbconvert & install it by default (P21)
- update doxygen input file paths for api docs (P20)
- workaround doxygen 1.7.4 issue blocking build (P19 from pcpa)
- fix assertion error when trying to extract archives without required perms

* Mon May 02 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.3.10-0.20110422.3
+ Revision: 662260
- move multiarch-dispatch to main package (#63160)

  + Funda Wang <fwang@mandriva.org>
    - move multiarch-dispath into main rpm package (bug#63160)

* Mon Apr 25 2011 Funda Wang <fwang@mandriva.org> 5.3.10-0.20110422.2
+ Revision: 658722
- fix wrong path of mkmultiarch script

* Sun Apr 24 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.3.10-0.20110422.1
+ Revision: 658161
- drop redundant %%defattr usage & buildroot cleaning at beginning of %%install
- don't load arch specific macros from rpm-mandriva-setup anymore, they've been
  merged into the standard arch specific macros for rpm
- obsolete multiarch-utils
- new cvs snapshot

* Sun Apr 10 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.3.9-0.20110330.7
+ Revision: 652164
- fix filetriggers firing multiple times hack (P19)

* Thu Apr 07 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.3.9-0.20110330.6
+ Revision: 651738
- add proper fix for i18n descriptions from Jeff
- fix %%_arch to be canonical

* Tue Apr 05 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.3.9-0.20110330.5
+ Revision: 650797
- fix translated descriptions not being added to packages (P18, #62979)
- add /etc/rpm/sysinfo dir

* Fri Apr 01 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.3.9-0.20110330.4
+ Revision: 649644
- fix stupid typo that managed to sneak itself back in again to mess up db log dir
- don't ship find-provides & find-requires, we're using our own version anyways..
- enable acl support
- drop unused expat-devel buildrequires
- s/tetex/texlive/ (pcpa)
- fix --without docs
- disable sqlite & docs build for bootstrap builds

* Wed Mar 30 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.3.9-0.20110330.3
+ Revision: 649239
- bah, fix incorrect package name in conflicts on db5.1

* Wed Mar 30 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.3.9-0.20110330.2
+ Revision: 649233
- add versioned buildrequires & conflicts to ensure >= db 5.1.25

* Wed Mar 30 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.3.9-0.20110330.1
+ Revision: 649206
- new cvs snapshot
- add rpm-helper>rpm to _dependency_whiteout_mandriva
- fix typo messing up bdb log dir used..
- update cvs snapshot (pulls in fix for ie. #62822 among other things)
- drop redundant --with-sqlite
- fix duplicate %%clean section (thx andrey for noticing!)
- fix mess happening while merging file trigger workaround upstream (#62865)

* Fri Mar 25 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.3.9-0.20110324.1
+ Revision: 648434
- drop %%clean now that it's enabled by default
- enable build of augeas support
- build with uuid support
- new cvs snapshot

* Sun Mar 06 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.3.9-0.20110303.2
+ Revision: 642259
- drop duplicates of of package first independent of distepoch (P16)

* Thu Mar 03 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.3.9-0.20110303.1
+ Revision: 641499
- new cvs snapshot
- get rid of some compile warnings for ugly distepoch pattern hack..

  + Funda Wang <fwang@mandriva.org>
    - rebuild to obsolete old packages

* Mon Feb 21 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.3.8-0.20110125.5
+ Revision: 639230
- work around file triggers firing multiple times and a related critical memleak
- set count in rpmmiCount() rather than rpmmiNext() for iterators with db cursor
  set to reduce unnecessary overhead

* Tue Feb 15 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.3.8-0.20110125.4
+ Revision: 637879
- accept NULL as argument for rootDir with mandriva filetriggers (#62395)
- fix issue with uninstall triggers always being run during upgrade (#62267)
- reset db cursor to NULL at end of rpmmiCount() so iterator won't break (#62279)
- drop feeble attempt to hack around disttag/distepoch issues by undefining it...

* Thu Feb 10 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.3.8-0.20110125.3
+ Revision: 637195
- fix typo in russian translation (#62333)
- fix %%__dbi_sqlconfig typo (#62386)

* Sat Feb 05 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.3.8-0.20110125.2
+ Revision: 636294
- revert st00pid conflicts->obsoletes change which broke upgrades...
- replace conflict on perl-RPM4 with an obsolete
- don't try adding files awaiting file triggers when --test is used (P9)

  + Funda Wang <fwang@mandriva.org>
    - add python link patch
    - link python module with python lib

* Mon Jan 31 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.3.8-0.20110125.1
+ Revision: 634521
- fix problem with ignored signals causing rpmbuild to break with gnome-terminal
  (fixes #62262, P7 from Theerud Lawtrakul/Jeff Johnson)
--Denne lnjoen og de som er under vil bli ignorert--
  A    SOURCES/rpm-5.3.8-rpmsq-ignored-signal-return-value.patch
  M    SPECS/rpm.spec
- remove no longer need Requires(post) on db51-utils which sed
- replace conflicts on librpm < 5.3 with obsoletes
- fix wrong tool path macros (#62322)
- fix regression tests and enable all of them in %%check from now on
- new cvs snapshot, drop patches merged upstream
- fix regression in rpmdsCompare() patch
- ignore -mdv2011.0 (disttag/distepoch) when querying package names for now

  + Funda Wang <fwang@mandriva.org>
    - really fix tool path

* Sun Jan 23 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.3.8-0.20110109.11
+ Revision: 632404
- d'oh, missed a line in previous patch..

* Sun Jan 23 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.3.8-0.20110109.10
+ Revision: 632396
- replace rpmdsCompare() patch with a simpler and less intrusive for now
- if distsuffix is defined, use it for disttag (from Anssi)
- fix handling of missing values when using 'rpm' directly as well (#55810 again)
- drop bootstrap.spec to workaround bs issue..
- fix inverted logic of %%_legacy_compat_non_pre_scripts_dont_fail
- don't do conversion in %%posttrans anymore, it will be handled by urpmi now
- change non-pre-scripts-dont-fail patch to be macro enabled
- gather all legacy compatibility hacks into legacy_compat.macros
- add back macro-enabled no-doc-conflicts patch
- always set log dir as a transaction log will always be created independent of whether setting DB_INIT_LOG or not
- add a dependency on perl-IO-String for perl-RPM (#61709)
- disable fsync call per file causing heavy performane penalties (P8, from eugeni)
- handle missing distepoch in version comparision (P7)
- increase max number of bdb locks
- don't fail package install on scriptlet failure, except for %%pre
- remove ppc macro symlink for now..
- fix install of dependency_whiteout.macros
- fix typo
- add more dependency loops to %%depency_whiteout and move out to separate file
- use %%_dependency_whiteout to fix some dependency loops for now..
- be sure that /var/lib/rpm/log exists before using it..
- don't make path to rpm absolute...
- be sure to set a default logdir for bdb, otherwise it won't be set for empty
  chroots
- fix use of no longer existing binaries such as 'rpmquery' (thx Dick Gevers)
- add provide/obsolete on %%{_lib}rpmconstant-devel
- fix typo in perl bindings giving issues with 'mdvsys' on missing buildrequires
- rpmconstant is part of rpm5, so obsolete/provide this..

* Sun Jan 09 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.3.8-0.20110109.3mdv2011.0
+ Revision: 630755
- use default directory for %%setup
- add missing errno.h header to rpm4compat.h (P0)

* Sun Jan 09 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.3.8-0.20110109.2mdv2011.0
+ Revision: 630735
- add back conflicts: librpm < 5.3 now that 'abrt' is linked against this version

* Sun Jan 09 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.3.8-0.20110109.1mdv2011.0
+ Revision: 630713
- new cvs snapshot
- get rid of doc-copy workarond and duplication of docs in 'rpm-build'
- disable conflicts on older librpm again awaiting 'abrt' in main/release rebuild
- fix path ppc-* -> powerpc-* symlink path, and always create it...
- fix 'rpm -qf' to work on owned files (#62148)
- reenable conflict on older librpm versions
- merge 5.3 branch

* Sat Nov 27 2010 Funda Wang <fwang@mandriva.org> 4.6.1-5mnb2
+ Revision: 601652
- rebuild for liblzma 5

* Fri Oct 29 2010 Michael Scherer <misc@mandriva.org> 4.6.1-4mnb2
+ Revision: 589999
- rebuild for python 2.7

* Mon Oct 18 2010 Per Øyvind Karlsen <peroyvind@mandriva.org> 4.6.1-3mnb2
+ Revision: 586616
- automatically handle ruby gem extraction in %%setup

* Thu Oct 07 2010 Per Øyvind Karlsen <peroyvind@mandriva.org> 4.6.1-2mnb2
+ Revision: 583901
- fix regression introduced with %%exclude change in previous release (fixes #61207)

* Wed Sep 29 2010 Per Øyvind Karlsen <peroyvind@mandriva.org> 4.6.1-1mnb2
+ Revision: 582007
- add '~' suffix to backup files created when using %%apply_patches
- finally put copyright & serial tags to death for real
- reapply fix for rmpvercmp with missing values & conflicts behaviour fix(#55810)
- update to to more recent debugedit that handles '.debug_pubtypes' section
- "New" release: 4.6.1 (while awaiting decission on where to go next...)
- fix %%exclude's behaviour to *only* mean exclude from %%files, not from check
  of unpackaged files. This brings back the behaviour we had in the past with
  rpm 4.4.8, and will require files not to be packaged to be deleted in %%install,
  and breaks building of any packages which incorrectly uses %%exclude for this
  purpose. Please fix any packages doing so! (P1016)

* Fri Aug 20 2010 Christophe Fergeau <cfergeau@mandriva.com> 4.6.0-15mnb2
+ Revision: 571456
- drop Pascal's patch for now
- fix "canonicalization unexpectedly shrank by one character" errors, patch by Anssi
- drop patch 135 which looks dubious
- revert previous commit, we don't want to diverge too much from rpm 4.x, we can
  readd it *after* this patch is upstreamed in rpm 4.x

  + Pascal Terjan <pterjan@mandriva.org>
    - Refuse to build a rpm with 2 identical triggers (#60699)

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - reapply fix for #55i810 (if not fully comprehended, those of us who wrote it
      does, ao removing out of ignorance and lack of insight will not e tolerated.

* Mon May 17 2010 Christophe Fergeau <cfergeau@mandriva.com> 4.6.0-14mnb2
+ Revision: 544968
- use db 4.8
- fix default perms in debug packages, #59083

  + Pascal Terjan <pterjan@mandriva.org>
    - Check chroot return code before running external script
    - Check chroot return code before running lua script

* Fri Apr 16 2010 Christophe Fergeau <cfergeau@mandriva.com> 4.6.0-12mnb2
+ Revision: 535522
- fix file trigger hang when several filetrigger scripts are run in parallel (#57878)

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuilt against nss-3.12.6

* Wed Feb 17 2010 Christophe Fergeau <cfergeau@mandriva.com> 4.6.0-10mnb2
+ Revision: 507168
- don't diverge from upstream wrt EVR comparisons

* Tue Feb 16 2010 Funda Wang <fwang@mandriva.org> 4.6.0-9mnb2
+ Revision: 506733
- rebuild for libpopt file path change

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - fix broken bitwise operator usage (thx to anssi for noticing)
    - do a new fix for #55810 that doesn't cause same regressions as the previously
      revert fix and hopefully no other regressions either.. ;)
      (P1010, http://rpm5.org/community/rpm-devel/4011.html)

* Fri Nov 20 2009 Per Øyvind Karlsen <peroyvind@mandriva.org> 4.6.0-8mnb2
+ Revision: 467682
- revert previous change as it'll break == dependencies on version only
  (which even requires-on-release policy requires) :/

* Fri Nov 20 2009 Per Øyvind Karlsen <peroyvind@mandriva.org> 4.6.0-7mnb2
+ Revision: 467652
- don't skip release comparision when checking conflicts if release value is
  missing (P1011 from Jeff Johnson, fixes #55810)

  + Michael Scherer <misc@mandriva.org>
    - fix unowned directory, reported by bitshuffler on irc, causing problem
      when installing rpm and using the wrong umask

* Fri Sep 25 2009 Olivier Blin <blino@mandriva.org> 4.6.0-6mnb2
+ Revision: 448653
- remove n32 support for now (not actually used)
- handle n32 ABI in find-requires and find-provides (from Arnaud Patard)
- switch to armv5tl (from Arnaud Patard)
  There are little chances that we'll have armv4tl. Doesn't use
  armv5tel as some SoC have broken instructions in the "e" extension
- fix %%_isa rpm macros for ARM (from Arnaud Patard)
- mips build fixes: define __isa* macros otherwise rpm doesn't work
  (from Arnaud Patard)
- fix stack-protector check: -fstack-protector doesn't error if it's
  not supported but issues a warning, building test case with -Werror
  the test case fixes the issue (from Arnaud Patard)
- add %%mips macro define all mips abi (from Arnaud Patard)

* Sun Aug 23 2009 Anssi Hannula <anssi@mandriva.org> 4.6.0-5mnb2
+ Revision: 419760
- fix ignored Requires(pre) and (post) when they have a plain Requires
  counterpart (rpm-fix-corequisites.patch backported from upstream 4.7.1)
- fix legacy prereq detection (rpm-fix-islegacyprereq.patch backported
  from upstream 4.7.1)
- map prereq to Requires(pre,preun) instead of nothingness when building
  (rpm-map-prereq.patch backported from upstream 4.7.1)

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - Avoid adding Lua sources/patches twice when recursing (P1010, git backport)

* Fri Jul 24 2009 Anssi Hannula <anssi@mandriva.org> 4.6.0-4mnb2
+ Revision: 399298
- fix filetriggers to be called on package removal as well (regression
  introduced in 4.6.0 package because of an error in rediffing of
  filetriggers.patch; fixes bug #52333)

* Tue Jun 30 2009 Thierry Vignaud <tv@mandriva.org> 4.6.0-3mnb2
+ Revision: 391017
- bump release so that cooker's rpm is newer than 2009.1's one

* Thu Jun 11 2009 Christophe Fergeau <cfergeau@mandriva.com> 4.6.0-2mnb2
+ Revision: 385093
- add missing calls to rpmluaPop to patch 159, might fix #50579
- Revert switch to db4.7

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - Expose packagecolor tag and add new tags from rpm5 as rpm otherwise will break
      when these unknown tags might be found in the rpmdb. Notice that this will only
      make rpm recognize these, not implement actual support for them.. (P1008)
    - build against bdb 4.7
    - build against db4.7 rather than db4.6 from now on

  + Arnaud Patard <apatard@mandriva.com>
    - define apply_patches if not already done. This fix bootstrapping issues
      (eg building current rpm on older rpm or building rpm on a system without
      rpm)
    - fix dependency on patch as rpm-build is now using "patch -U" which has
      been introduced in version 2.5.9-7mdv2009.1.

* Fri Feb 13 2009 Christophe Fergeau <cfergeau@mandriva.com> 4.6.0-1mnb2
+ Revision: 340115
- Update to rpm 4.6.0

* Thu Jan 29 2009 Pixel <pixel@mandriva.com> 4.6.0-0.rc3.7mnb2
+ Revision: 335221
- add %%apply_patches: it can be used to replace all "%%patchN" lines,
  but it forces all patches to be "-p1".
- call %%_patch and %%_after_setup for use in rpm-mandriva-setup-build
  (useful for "--with git_repository")

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - don't wipe out $DOCDIR when using %%doc as it will wipe out any files that would
      happen to be installed during %%install. (P1008)

* Tue Jan 20 2009 Pixel <pixel@mandriva.com> 4.6.0-0.rc3.6mnb2
+ Revision: 331759
- replace nss-inithack patch with upstream patch
  (which is more complete, esp fixes rpmresign in perl-RPM4)
- add patch fixing rpmdsMerge on rpmdsSingle (fixes 07dep.t in perl-RPM4)
- fix segfault triggered by perl-RPM4 tests

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - fix internal enum value for xz (noticed by jnovy, thx!)
    - oops, fix a minor glitch with a final api change
    - add versioned requires on liblzma-devel since we *really* need latest api
      changes :)
    - update lzma payload support to add support for new xz format in parallel(P1007)

* Wed Dec 24 2008 Funda Wang <fwang@mandriva.org> 4.6.0-0.rc3.5mnb2
+ Revision: 318370
- temporarily disable graphviz BR

  + Michael Scherer <misc@mandriva.org>
    - rebuild for new python

  + Pixel <pixel@mandriva.com>
    - add conflict on urpmi-recover since rpm 4.6.0 dropped support for --repackage

* Thu Dec 18 2008 Pixel <pixel@mandriva.com> 4.6.0-0.rc3.3mnb2
+ Revision: 315608
- add patch153: "fix" segfault in mdkapplet (#46323)
- add patch154: fix compilation with Werror=format-security
- merge patch91 (check-dupl-files) into patch111 (check-files fix for "//" in buildroot)

* Mon Dec 15 2008 Pixel <pixel@mandriva.com> 4.6.0-0.rc3.2mnb2
+ Revision: 314562
- enable sqlite (was disabled after rpm-4.6.0 switch)

* Fri Dec 12 2008 Pixel <pixel@mandriva.com> 4.6.0-0.rc3.1mnb2
+ Revision: 313584
- 4.6.0-rc3
- drop patch153 (buildroot-subpackage), fixed upstream

* Thu Dec 11 2008 Pixel <pixel@mandriva.com> 4.6.0-0.rc2.2mnb2
+ Revision: 312890
- rediff patch71, patch83, patch91, patch140, patch145, patch147, patch1005
- fix patch2002 (python-writeHdlist), was broken with rpm 4.6 API

* Tue Dec 09 2008 Pixel <pixel@mandriva.com> 4.6.0-0.rc2.1mnb2
+ Revision: 312303
- use %%configure (so that libdir is correctly on x86_64)
- 4.6.0-rc2
- add patch152: fix build
- add patch153: buildroot with subpackages issue
- drop already unused %%buildnptl (obsolete since rpm uses system libdb)
- drop patch134 (defaultbuildroot), so %%defaultbuildroot is no more used,
  global %%buildroot is used, and BuildRoot is no more handled
- drop patch56 (ppc32). hopefully now unneeded
- drop patch44 (amd64-x86_64 compat). hopefully now unneeded
- drop patch112 (dont-use-rpmio-to-read-file-for-script), only needed on rpm 4.4.8?
- drop patch1002 (default-topdir--usr-src-rpm). it is now /root/rpmbuild
- drop patch1003: drop support for "suggests" the way rpm >= 4.4.7 do it
  (all Mandriva packages uses the new "suggests" nowadays)
- drop patch139 (do-not-allow-fileconflict-between-non-colored-file),
  since partially applied upstream (47c85270631de173d873b98bc79727e2db203007)
- drop popt (it is no more internal), drop patch1004, patch2004
- drop patch3 ("file" is no more internal)
- drop patch149 (upstream has already got rid of internal db)
- drop patch1450 (problem fixed upstream, though differently)
- drop patch132 (extcond), patch133 has been simplified (butchered) to work without it
- drop patch1133 (integrated in patch133 (weakdeps))
- drop patch100 (rpmbuild-missing), no more needed since we have rpmb_deprecated
- drop patch142, patch143, patch144, patch150 applied upstream
- simplify patch1001 since most is upstream, create patch1006 containing the
  PayloadIsLzma compat issue
- adapt patch137 (headerIconv)
- adapt patch31 (syslog)
- adapt/simplify patch114: only specifically read macros.d/*.macros
- adapt patch2000, patch2001 (serial/copyright tag)
- adapt patch133 (weakdeps), drop --suggests/--recommends difference
- rediff patch49, patch64, patch70, patch141, patch146, patch147, patch148,
  patch151, patch2002, patch2005

* Sun Oct 19 2008 Per Øyvind Karlsen <peroyvind@mandriva.org> 4.4.2.3-22mnb2
+ Revision: 295367
- rebuild against liblzma which I had to bump the major of yet again
- actually remember to bump popt release as well this time (popt should REALLY
  be split out!!!)

* Sat Oct 18 2008 Per Øyvind Karlsen <peroyvind@mandriva.org> 4.4.2.3-21mnb2
+ Revision: 294824
- fix build with new liblzma (updates P1001)

  + Pixel <pixel@mandriva.com>
    - failing triggers must not block an update (otherwise both packages are kept)

* Wed Oct 01 2008 Pixel <pixel@mandriva.com> 4.4.2.3-20mnb2
+ Revision: 290443
- protect-against-non-robust-futex patch: remove the ugly error messages
  when non-root

* Wed Oct 01 2008 Pixel <pixel@mandriva.com> 4.4.2.3-19mnb2
+ Revision: 290325
- ensure stale futex locks do not block (#41868)

* Thu Sep 11 2008 Pixel <pixel@mandriva.com> 4.4.2.3-18mnb2
+ Revision: 283690
- fix broken cpio for hardlink on softlink (#43737)
- remove /usr/lib/libpopt.so.0 symlink (unneeded)

* Sat Sep 06 2008 Pixel <pixel@mandriva.com> 4.4.2.3-17mnb2
+ Revision: 281842
- use external libdb-4.6.so instead of internal one (was DB 4.3.27: December 22, 2004).
  (hopefully fixing #41868)

* Tue Aug 26 2008 Pixel <pixel@mandriva.com> 4.4.2.3-16mnb2
+ Revision: 276212
- add patch148 which ensures chroot errors are not ignored
  (the bug occured on mandriva build system, the files
  were installed on the non rooted system)

* Tue Aug 05 2008 Frederic Crozat <fcrozat@mandriva.com> 4.4.2.3-15mnb2
+ Revision: 263799
- bump popt release too
- Bump minimal version of rpm-mandriva-setup, to ensure filetriggers
  are enabled during upgrade from older distributions

* Thu Jul 17 2008 Oden Eriksson <oeriksson@mandriva.com> 4.4.2.3-14mnb2
+ Revision: 237798
- bump release for popt as well
- fix deps and rebuild against latest neon-devel

* Fri Jul 04 2008 Pixel <pixel@mandriva.com> 4.4.2.3-13mnb2
+ Revision: 231680
- fix memory leak in patch124 (regression introduced on 2008-06-23)
- fix detecting wether filetriggers are activated (through %%_filetriggers_dir)

* Thu Jun 26 2008 Pixel <pixel@mandriva.com> 4.4.2.3-12mnb2
+ Revision: 229317
- fix --testing errors introduced by filetriggers

* Tue Jun 24 2008 Pixel <pixel@mandriva.com> 4.4.2.3-11mnb2
+ Revision: 228550
- nicely handle /etc/rpm/macros.cdb disappearance (esp. for people having %%_dbapi set there)

* Mon Jun 23 2008 Pixel <pixel@mandriva.com> 4.4.2.3-10mnb2
+ Revision: 228082
- enhance patch124 to use "Dirnames" db before using "Packages" db
  (hence much less db accesses in the pathological "COPYING" case)
- rpm must feature PayloadIsLzma = 4.4.2-1 to be the most compatible (?!)
  (with SuSE, and with temporary cooker packages with PayloadIsLzma <= 4.4.2.2-1)

* Sun Jun 22 2008 Pixel <pixel@mandriva.com> 4.4.2.3-8mnb2
+ Revision: 227894
- PayloadIsLzma version must be at least 4.4.6-1 to be compatible with mdv2008.0
- fix segfault when transaction fails

* Fri Jun 20 2008 Pixel <pixel@mandriva.com> 4.4.2.3-7mnb2
+ Revision: 227396
- drop our old macros.cdb, which was forcing old values,
  esp "verify" which forcing rpm to verify db after each changes
  (which was making rpm quite slow when rpmdb was not in cache)
- cleanup: drop not applied global-RPMLOCK patch

* Thu Jun 19 2008 Pixel <pixel@mandriva.com> 4.4.2.3-6mnb2
+ Revision: 226213
- fix filetriggers (librpm was exiting in case of sigpipe in filetrigger script)
- checks on "non packaged binary packages" now depend on %%_missing_subpackage_terminate_build (patch147)
- checks on "non packaged binary packages" only done on "mdv" packages (patch147)

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - fix version typo
    - switch to use liblzma for lzma payload (P1000, partly derived from rpm5.org & OpenSuSE)

* Wed Jun 11 2008 Pixel <pixel@mandriva.com> 4.4.2.3-4mnb2
+ Revision: 218093
- rpmbuild: add patch to ensure some parse errors are really fatal as they should

* Mon Jun 09 2008 Pixel <pixel@mandriva.com> 4.4.2.3-3mnb2
+ Revision: 217217
- add new fatal errors (during package build):
  o disallow scriptlets for non packaged binary packages
  o "%%files foo" for subpackages is now mandatory
- do not call ldconfig in %%post/%%postun, it is now handled by filetriggers
- replace "%%post -p ldconfig" hack with a full featured generic solution:
  filetriggers (cf http://wiki.mandriva.com/en/Rpm_filetriggers)
- "#%%define foo bar" is now a fatal error
- handle "%%posttrans -p ..." with no script body (eg: %%posttrans -p /sbin/ldconfig)
- add "requires tar" in rpm-build
- fix build of debugedit (patch143)

* Tue May 13 2008 Thierry Vignaud <tv@mandriva.org> 4.4.2.3-1mnb2
+ Revision: 206778
- fix build on x86_64

  + Pixel <pixel@mandriva.com>
    - 4.4.2.3
    - add patch142 which ensures chroot errors are not ignored
      (the bug occured on mandriva build system, the files from package binutils
      were installed on the non rooted system)
    - drop patches applied upstream: 136, 138
    - rediff patch17

* Tue Apr 01 2008 Pixel <pixel@mandriva.com> 4.4.2.3-0.rc1.7mnb1
+ Revision: 191469
- postpone and group ldconfig %%post in %%posttrans instead of wrongly skipping ldconfig

* Fri Mar 28 2008 Pixel <pixel@mandriva.com> 4.4.2.3-0.rc1.6mnb1
+ Revision: 190842
- rebuild with fixed libneon0.26-devel

* Mon Mar 17 2008 Pixel <pixel@mandriva.com> 4.4.2.3-0.rc1.5mnb1
+ Revision: 188330
- add support for "suggests" and "enhances" in rpmds (needed for "sophie") (nanardon)
- use %%_vendor instead of %%vendor (thanks-to/required-by nanardon)
- fix typo in recent commit
- fix broken symlink (due to %%rpmversion != %%srcver for rc1)
- trivial fix for Russian translation (#38713)

  + Toshihiro Yamagishi <toshihiro@turbolinux.co.jp>
    - get rid of _host_vendor definition. It should be defined by rpm-xxx-macros.
    - use original find-requires,find-provides,find-lang when build with turbolinux.

* Sat Mar 01 2008 Pixel <pixel@mandriva.com> 4.4.2.3-0.rc1.3mnb1
+ Revision: 177474
- fix file conflicts wrongly allowed on x86_64
- when dropping requires during tsort, do not display "PreReq" when it really is "Requires"
- rpm-mandriva-setup and rpm-mandriva-setup-build requires are only on Mandriva
- add buildlang patch which unsets locales when building packages (for Turbolinux)

  + Thierry Vignaud <tv@mandriva.org>
    - replace %%mkrel with %%manbo_mkrel for Manbo Core 1

* Thu Feb 14 2008 Pixel <pixel@mandriva.com> 4.4.2.3-0.rc1.2mdv2008.1
+ Revision: 167788
- use rpmrc and rpmpopt from rpm-manbo-setup
- get best lang from rpm HEADERI18NTABLE, instead of getting first fuzzy match
  (eg: zh_TW matches zh_CN whereas zh_TW entry is available)
- debugedit: remove a wrong check in case %%_topdir is /RPM (from Turbolinux)
- add japanese popt translations
- add Turbolinux specific patches:
  o re-allow "Serial" and "Copyright" (aliases of "Epoch" and "License")
    (to ease Turbolinux migration)
  o add writeHeaderListTofile function into python binding
    (needed by Turbolinux buildman build system)

  + Toshihiro Yamagishi <toshihiro@turbolinux.co.jp>
    - headerIconv.patch: check realloc() value
    - convert the data to a specific encoding which used in the selected locale.

* Mon Jan 28 2008 Pixel <pixel@mandriva.com> 4.4.2.3-0.rc1.1mdv2008.1
+ Revision: 159090
- 4.4.2.3 adds ix86 macros files to x86_64
- new release 4.4.2.3-rc1
- libpopt needs a release number different from rpm so that we can reset rpm's
  release and increase libpopt's
- drop applied patches: patch82 (ordering), patch98 (bad pointer),
  patch108 (dgettext), patch116 (qv), patch119 (without-O2),
  patch121 (timeout 60secs), patch127 (rpmbuild --quiet),
  patch128 (rpm -K segfault), patch136 (macro on last line),
  patch1006 (triggerprein), patch1007 (russian),
  patch1008 (display Requires found),
- drop patch135 (truncated rpmProblemString): no more needed, workarounded
  upstream

* Wed Jan 23 2008 Pixel <pixel@mandriva.com> 4.4.2.2-7mdv2008.1
+ Revision: 157054
- fix rpmbuild not printing Requires after build (fix backported from 4.4.8) (#36672)
- allow doc conflict in same transaction (#37040)
  (it was already allowed in different transactions)
- fix russian translation (#36974)

* Sat Jan 12 2008 Anssi Hannula <anssi@mandriva.org> 4.4.2.2-6mdv2008.1
+ Revision: 149522
- allow conflicting ghost file types as sometimes the same ghost file
  is a file in one package and a symlink in another package (modifies
  rpm-4.4.2.2-allow-conflicting-ghost-files.patch)

* Tue Jan 08 2008 Pixel <pixel@mandriva.com> 4.4.2.2-5mdv2008.1
+ Revision: 146377
- %%triggerprein were missing in 4.4.2.2, adding them

* Thu Dec 20 2007 Pixel <pixel@mandriva.com> 4.4.2.2-4mdv2008.1
+ Revision: 135996
- fix multiline macro handling on last line of spec file (#27417)
- fix truncated "file conflict" error message in russian (#31680)

* Tue Dec 18 2007 Pixel <pixel@mandriva.com> 4.4.2.2-3mdv2008.1
+ Revision: 132430
- re-introduce temporarily BuildRoot so that rpm builds
- drop patch for SOURCEPACKAGE (unneeded in rpm 4.4.2.2 which keeps compatibility)
- fix defaultbuildroot patch (fix building with %%defaultbuildroot and subpackages)
- allow conflicting %%ghost files (as used to be in rpm >= 4.4.6)
- modify patch no-doc-conflicts instead of patching it
- for compatibility with rpm 4.4.8, allow conflicting doc files in
  /usr/share/man, /usr/share/gtk-doc/html /usr/share/gnome/html

* Mon Dec 17 2007 Pixel <pixel@mandriva.com> 4.4.2.2-2mdv2008.1
+ Revision: 125038
- patch134 introduces %%defaultbuildroot to use instead of %%buildroot in our global macros
- keep libpopt.so versioning from 4.4.8 (to avoid warnings)
- fix URL
- switch to 4.4.2.2 (using epoch: 1)
- add patch132 and patch133 to handle "Suggests" via RPMTAG_SUGGESTSNAME
- add patches to be compatible with >= 4.4.8 :
  o patch1000: handle %%buildroot macro
  o patch1001: handle suggests via RPMTAG_REQUIRENAME + RPMSENSE_MISSINGOK
  o patch1001: lzma-support (integrates patch130 (lzma-fixes), patch131 (lzma_alone))
  o patch1002: default %%_topdir is /usr/src/rpm
  o patch1003: handle RPMSENSE_MISSINGOK (integrates patch129 (do-not-cache-unsatisfied-suggest))
- drop unneeded patches:
  o applied: patch63 (applied in lib/package.c), patch68, patch72,
    patch77 (%%_srcdefattr), patch92 (newtar), patch94 (rpmv3-support),
    patch113 (%%_docdir_fmt), patch123 (find-lang omf)
  o patch1 (no builtin zlib)
  o patch2 (rpm is dynamically linked by default)
  o patch85 (no more perl module)
  o patch87 (was disabling dirname require introduced in 4.4.6)
  o patch89 (>= 4.4.6 specific compilation issue)
  o patch107 (fixed differently in changeset 6799:446988cfb9c1)
  o 4.4.8 specific: patch109, patch117 (dont-replace-config-not-in-db),
    patch118 (lowercase platform), patch120 (segfault fix), patch122 (fix
    crash with buggy rpm and FILELINKTOS), patch125 (popt.h fix), patch126
    (platform32 support)
  o 4.4.8 specific?: patch115 (dont-clean-buildroot-in-install)
- adapt patches:
  o rediff: patch31 (syslog), patch64 (vendor popt), patch84 (rpmqv-ghost),
    patch116 (qv-use-same-indentation), patch49, patch56, patch82, patch86,
    patch112, patch119
  o patch3 (prefer-pic in "file" lib .la)
  o patch17 (keep enhancements from upstream version)
  o patch114 (read our macros files)
  o patch124 (speedup-by-not-checking-same-files-with-different-paths-through-symlink)
    and add patch1124 (revert-unused-skipDir-functionality) needed by patch124
- use autoreconf and don't do it in db/dist (it fails)
- drop perl-RPM (unused and no more in rpm 4.4.2.2)
- drop now unneeded perldirs patch85
- don't build apidocs since we don't bundle them
- drop patch78 (Do not use futex, but fcntl) which is not doing anything anymore

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - use LZMA_Alone file format, even with newer versions (P131, from cvs)
    - be more consistent and use unlzma in stead of lzma -d -c in rpm2cpio.sh (lzma patch)
    - drop unused leftover macros for lzma patch..
    - final fix of lzma payload patch, it can now be used properly same way as gzip and bzip2
    - correctify lzma fix patch
    - switch to patch from cvs for lzma fixes
    - update arguments for lzma utils as current old arguments breaks it
    - I suck, don't move man pages around at all and stop messing:p
    - move man page for perl module to perl-RPM package

  + Olivier Blin <blino@mandriva.org>
    - do not expand _install_langs macro in default /etc/rpm/macros
    - fix typo in default /etc/rpm/macros
    - explicitely require neon-devel 0.26 (does not build with neon 0.27)

* Tue Oct 02 2007 Pixel <pixel@mandriva.com> 4.4.8-22mdv2008.0
+ Revision: 94448
- fix rpm allowing to remove a package which is both suggested and required (#34342)

* Fri Sep 28 2007 Pixel <pixel@mandriva.com> 4.4.8-21mdv2008.0
+ Revision: 93603
- remove global RPMLOCK, it doesn't seem to fix rpmdb issues, and may cause
  installer to crash

* Thu Sep 27 2007 Pixel <pixel@mandriva.com> 4.4.8-20mdv2008.0
+ Revision: 93272
- patch global-RPMLOCK:
  o fix rebuilddb (#34181)
  o don't lock when querying the db as non-superuser
  o fix locking in shared mode (ie fix typo)
  o remove message "RPMLOCK_NOWAIT should have been set!"
    which can't be done reliably
  o more debug messages about RPMLOCK

* Wed Sep 26 2007 Pixel <pixel@mandriva.com> 4.4.8-19mdv2008.0
+ Revision: 93120
- patch global-RPMLOCK:
  o allow rpm to not wait on lock when RPMLOCK_NOWAIT is set
  o ensure we don't have a dead-lock in package scriptlets which call "rpm -q"
    (eg: dkms). but it will die with an error
  o do create /var/lib/rpm directory when needed (as done in rpmdb/db3.c)
  o use flock instead of fcntl+F_SETLK
    (so that we really ensure the same process doesn't open twice the db)
  (still need not to lock when accessing in shared mode with not enough rights
  to write RPMLOCK)
- fix creating /RPMLOCK instead of /var/lib/rpm/RPMLOCK

* Mon Sep 24 2007 Pixel <pixel@mandriva.com> 4.4.8-18mdv2008.0
+ Revision: 92580
- do not use __db* files anymore, make them private
- (re-)add a global lock to ensure everything is correct
  (to ensure doing "rpm -qa" is always correct even if an upgrade is in
  progress)
- fix rpm -K segfaulting on corrupted header (#33735)

* Mon Sep 10 2007 Pixel <pixel@mandriva.com> 4.4.8-17mdv2008.0
+ Revision: 84150
- make "rpm -bb --quiet" quiet as should be

* Thu Sep 06 2007 Pixel <pixel@mandriva.com> 4.4.8-16mdv2008.0
+ Revision: 81086
- bug fix release, fix stupid typo in /etc/platform32 reading patch

* Thu Sep 06 2007 Pixel <pixel@mandriva.com> 4.4.8-15mdv2008.0
+ Revision: 80965
- really allow to use "linux32 rpm -bb" instead of "linux32 rpm -bb --target x86_64"
  (it uses /etc/rpm/platform32)

* Wed Sep 05 2007 Pixel <pixel@mandriva.com> 4.4.8-13mdv2008.0
+ Revision: 79852
- allow to use "linux32 rpm -bb" instead of "linux32 rpm -bb --target x86_64"
  (for this to work, %%{_host_cpu32} must be set in rpm-mandriva-setup)

* Thu Aug 30 2007 Pixel <pixel@mandriva.com> 4.4.8-12mdv2008.0
+ Revision: 75298
- fix popt.h (remove N_) (#31397)

* Wed Aug 29 2007 Pixel <pixel@mandriva.com> 4.4.8-11mdv2008.0
+ Revision: 74355
- add patch to speedup simple "rpm -e" or "rpm -U"
- make find-lang --with-gnome picks up omf files (rhbz#251400) (rpm.org patch)
- add the bug number fixed

* Tue Aug 21 2007 Pixel <pixel@mandriva.com> 4.4.8-10mdv2008.0
+ Revision: 68566
- patch fixing parse_hdlist (and so genhdlist2) on heavy loaded boxes
- fix segfault on weird rpm that used to work (#32102)
- remove recursive %%_mandir (and don't keep it, it's not needed anymore)

  + Thierry Vignaud <tv@mandriva.org>
    - replace %%{_datadir}/man by %%{_mandir}!
    - replace %%_datadir/man by %%_mandir!

* Sat Aug 18 2007 Oden Eriksson <oeriksson@mandriva.com> 4.4.8-9mdv2008.0
+ Revision: 65549
- don't provide these files twice:
 /usr/lib/rpm/rpmdb_deadlock
 /usr/lib/rpm/rpmdb_dump
 /usr/lib/rpm/rpmdb_load
 /usr/lib/rpm/rpmdb_loadcvt
 /usr/lib/rpm/rpmdb_stat
 /usr/lib/rpm/rpmdb_svc
 /usr/lib/rpm/rpmdb_verify
 they are now only provided in the main rpm package, and not
 also in the devel package. that is the way to go according to
 jbj.

  + Thierry Vignaud <tv@mandriva.org>
    - fix URL

* Mon Aug 06 2007 Pixel <pixel@mandriva.com> 4.4.8-8mdv2008.0
+ Revision: 59505
- do not use nptl on any arch (since x86_64 specific issues seem to disappear
  when using same locking mechanism as x86) (may fix #32102)
- fix segfault occuring with some old rpm v3 from urpmi test cases
- allow building --with debug
- restore do-check-free-size-when-bavail-is-0 patch (after rediff)

* Wed Jul 25 2007 Olivier Thauvin <nanardon@mandriva.org> 4.4.8-7mdv2008.0
+ Revision: 55450
- fix #31535: lowercase OS tag to compare against platform
- use upstream patch

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - add requires on lzma

* Fri Jul 06 2007 Olivier Thauvin <nanardon@mandriva.org> 4.4.8-6mdv2008.0
+ Revision: 48984
- fix config file replace when not yet in db
- kill not bad macros definition
- find-lang is now a perl script

* Fri Jun 22 2007 Anssi Hannula <anssi@mandriva.org> 4.4.8-5mdv2008.0
+ Revision: 42672
- require arch-specific libpopt and libpopt-devel
- add back dropped librpm-devel and libpopt-devel provides

* Wed Jun 20 2007 Olivier Thauvin <nanardon@mandriva.org> 4.4.8-4mdv2008.0
+ Revision: 41943
- fix buildreq for autoconf/automake
- apply new devel policy

* Tue Jun 19 2007 Olivier Thauvin <nanardon@mandriva.org> 4.4.8-3mdv2008.0
+ Revision: 41414
- kill coloring patch, buggy, and not so usefull
- patch116: fix rpm -V output (#31287)

* Sun Jun 10 2007 Olivier Thauvin <nanardon@mandriva.org> 4.4.8-2mdv2008.0
+ Revision: 37847
- patch115: avoid breakage of conectiva --without bm feature
- remove patch 110, add patch114: do no longer use rpmrc, using only macros instead, so requiring latest rpm-mandriva-setup to have /etc/rpm/platform
- fix perl module release
- patch to backport _docdir_fmt macro
- 4.4.8
  o rediff patch 72, 87, 49, 62, 17, 56, 64
  o kill patch (merge or fix upstream, woot):
    57, 80, 90, 93, 193, 95, 96, 97, 99, 103, 104, 105, 109, 110, 111,
    112, 114, 115, 101, 102, 107
  o kill patch 69, hard to maintain, will be merge upstream
  o Patch109: workaround specfile parsing check,
    http://rpm5.org/cvs/tktview?tn=6
  o Patch110: still read rpmrc (this should die one day)
  o Patch111: trim twice / in buildroot, making unpackaged files check failing
  o Patch112: avoid a very issue regarding Fopen()

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - use %%{ix86} & %%{sunsparc} macros for x86 & sparc
    - use %%{sunsparc} macro to ensure sparcv9 gets included too

  + Pixel <pixel@mandriva.com>
    - make it explicit that older perl-URPM are not compatible with 4.4.8
    - add patches 112 113 114 115 from both rpm 4.4.9 and hg.rpm.org
    - cleanup provides-obsoleted.patch, moving other fixes into rebuilddb-with-root.patch
    - more complete fix-segfault-on-header-without-RPMTAG_NAME patch (from upstream)
    - don't segfault on header without RPMTAG_NAME
    - add requires pkgconfig in rpm-build (#30632)
      (it is needed for performing automatic computation of pkgconfig files
      dependencies, see /usr/lib/rpm/mandriva/pkgconfigdeps.sh)
    - add patch (ensure-uninst-callback-is-called-for-empty-packages)
      to allow urpmi to display "remove package foo" when removing an empty package

* Wed Apr 25 2007 Adam Williamson <awilliamson@mandriva.org> 4.4.6-22mdv2008.0
+ Revision: 18290
- rebuild against new beecrypt


* Wed Feb 14 2007 Pixel <pixel@mandriva.com> 4.4.6-21mdv2007.1
+ Revision: 120751
- fix parsing ")" (for if statements in spec files for example)
- rpm handles nicely failing %%pre, but it doesn't handle the rest
- patch to use dgettext instead of gettext to allow progs like urpmi to use
  their own textdomain and still have rpm translations
- fix checking available free space when "non-superuser free space" is 0

  + Gwenole Beauchesne <gbeauchesne@mandriva.com>
    - requires newer rpm-mandriva-setup for rtld(GNU_HASH) notes

* Fri Jan 12 2007 Pixel <pixel@mandriva.com> 4.4.6-19mdv2007.1
+ Revision: 108072
- P98: security fix for CVE-2006-5466
-mv8 which is deprecated and no longer valid (Per Oyvind, #26501)

  + Thierry Vignaud <tvignaud@mandriva.com>
    - provides with unexpanded macros aren't that nice

* Mon Jan 08 2007 Pixel <pixel@mandriva.com> 4.4.6-18mdv2007.1
+ Revision: 105990
- fix bug 27987 where sslexplorer rpm has "Source RPM: (none)" and so rpm
  thought it is a src.rpm. the fix is only done for old v3 rpms
- "rpm -i --root" as user can't work, don't silently ignore the failing chroot()
- fix --root rpm option failing for non-root users (Christiaan Welvaart)
- really commit the patch
- fix segfault on weird buggy rpm header
- fix query format xml on rpm header with tag 265 which has no name (#27108)

* Fri Dec 08 2006 Gwenole Beauchesne <gbeauchesne@mandriva.com> 4.4.6-12mdv2007.1
+ Revision: 93842
- generate PIC code for static objects that can be built into a DSO
- remove (obsolete) arch-dependent flags
- don't build statically linked executables
- Fix zlib tree to parallel build, propagate optflags to there too.
- Introduce new ppc32 arch, fix ppc64 bi-arch builds, fix ppc builds on newer CPUs.
- fix build on ppc64

  + Pixel <pixel@mandriva.com>
    - fix segfault on some old format rpms (#27263)

* Thu Nov 30 2006 Pixel <pixel@mandriva.com> 4.4.6-11mdv2007.1
+ Revision: 88894
- rebuild for python  2.5
- add patches fixing #26545:
  o don't leave behind /usr/X11R6/lib/X11/app-defaults;456ac510 on error
  o fix segfault
- ignore getcwd failing (db_abshome will not be set,
  it may affect db/log/log_archive.c, but that should be ok) (#20897)
- fix "rpm -bs t.spec" returning buggy error message
  "t.spec: No such file or directory" when rpm-build is not installed
- fix free on invalid pointer after displaying "Unable to open temp file" (#27260)
- have a nice error message when chroot fails
  (instead of the dreaded: "enterChroot: Assertion `xx == 0' failed.")

  + Gwenole Beauchesne <gbeauchesne@mandriva.com>
    - Extend #27260 fix to its root cause as there are other instances of a
      similar bug in other sources (yet, unexposed/reported).

* Fri Sep 15 2006 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 4.4.6-10mdv2007.0
+ Revision: 61429
- Bump release number
- Improve previous patch: make it conditional on the environment variable RPM_IGNORE_SCRIPTLETS_FAILURE
- Allow preinstall scriptlets to fail and not interrupting the installation.
  This is a workaround for bug 25598.

* Sat Aug 19 2006 Olivier Thauvin <nanardon@mandriva.org> 4.4.6-9mdv2007.0
+ Revision: 56766
- bump release
- revert to my own chroot patch, thee second one is broken

* Sun Aug 13 2006 Olivier Thauvin <nanardon@mandriva.org> 4.4.6-8mdv2007.0
+ Revision: 55706
- bump release
- buildrequires lua-devel
- import mailscanner
- update patch with C. Welvaart fixes

  + Rafael Garcia-Suarez <rgarciasuarez@mandriva.com>
    - Fix typos

* Sat Jul 29 2006 Olivier Thauvin <nanardon@mandriva.org> 4.4.6-7mdv2007.0
+ Revision: 42481
- bump release
- add upstream patch97: fix dbenv
- patch96: fix #23774

* Thu Jul 27 2006 Olivier Thauvin <nanardon@mandriva.org> 4.4.6-6mdv2007.0
+ Revision: 42186
- fix rpmv3 patch: rpm version in the lead in 3 for both rpm 3 and 4
- fix #23075: patch 95, use tee -a

* Wed Jul 26 2006 Olivier Thauvin <nanardon@mandriva.org> 4.4.6-5mdv2007.0
+ Revision: 42052
- patch93: support rpm v3
- bump release
- ensure leaveChroot can't be run by another function which is not the the caller of enterChroot
- remove changelog from spec
- add patch 93 (disable by default, need tests) to fix issue in rpmdb when mixing 'rpm --root' and 'chroot rpm'
- update macros in the spec
- provide some /etc/rpm files
- -3mdv release
- fix patch in patch
- better rpmdb.h c++ fix
- Patch90: fix unchecked end of line in macro expand
- patch 89: make rpmdb.h compliant
- file in /etc are %%config
- patch 88: readd SOURCEPACKAGE tag to source rpm
- make no_dirname_dep patch configurable with a macro
- bunzip patch, merge rpm 4.4.6
- initial import of rpm
- initial import of rpm

  + Rafael Garcia-Suarez <rgarciasuarez@mandriva.com>
    - 4.4.6-4mdk
    - Patch by Pixel to use --wildcards when using tar to list all specfiles in a tar
      ball (this fixes rpm -t).
    - Add patch 91: avoids taking into account duplicates in file list
      when checking for unpackaged files

* Wed Jul 12 2006 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 4.4.6-4mdv2007.0
- Fix rpm -ta (Pixel)

* Thu Jun 22 2006 Olivier Thauvin <nanardon@mandriva.org> 4.4.6-3mdv2007.0
- patchs:
  - fix rpmdb.h c++ compilation (C. Welvaart)
  - fix unchecked end of string in macro expand (O. Thauvin)
  - fix check unpackaged files script (R. Garcia-Suarez)
- update macros provide by the spec used for bootstraping
- set some /etc/rpm/macros.* as config(noreplace)

* Mon Jun 12 2006 Olivier Thauvin <nanardon@mandriva.org> 4.4.6-2mdv2007.0
- Patch88: readd SOURCEPACKAGE tag into src.rpm

* Fri May 26 2006 Olivier Thauvin <nanardon@mandriva.org> 4.4.6-1mdv2007.0
- 4.4.6
- rediff patches
- add patch to disable dirnames dependencies for now

* Tue Mar 21 2006 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 4.4.5-2mdk
- Require latest rpm-mandriva-setup

* Tue Mar 14 2006 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 4.4.5-1mdk
- 4.4.5
- Remove patches 41 and 87, merged upstream
- Rediff patches 69 and 78
- Make rpm-build require libtool-base instead of libtool (bug #21162)
- Turn the triggerun in post scriptlet

* Tue Mar 07 2006 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 4.4.4-4mdk
- Patch 87

* Tue Feb 07 2006 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 4.4.4-3mdk
- Move popt(3) man page into libpopt-devel (bug 18161)
- Add coreutils in prerequisites (bug 19144)
- Fix dangling symlink (bug 6788)

* Tue Jan 17 2006 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 4.4.4-2mdk
- Patch 86: don't cache Depends DB (Olivier Thauvin)
- Bump requires on rpm-mandriva-setup

* Thu Jan 05 2006 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 4.4.4-1mdk
- New version 4.4.4
- Rediff patches 31, 49, 62, 69, 71, 78, 82, 84
- Remove patch 66 (fixed upstream)
- Remove patch 74 (no longer necessary, no legacy prereqs anymore)
- Remove patch 76 (should be unnecessary now that RH bug 151255 is fixed)
- Remove patch 79 (applied upstream)
- Remove patch 81 (does nothing)
- New subpackage perl-RPM, and patch 85 to install it in vendor dir
- Use static libneon, libsqlite3 and libopenssl
- Update condition for triggerun
- Add conditional BuildRequires on nptl-devel
- Disable popt tests
- Remove selinux
- Requires recent rpm-mandriva-setup for _rpmlock_path macro

* Sun Nov 13 2005 Olivier Thauvin <nanardon@mandriva.org> 4.4.2-6mdk
- rebuild for openssl (ask by Oden)

* Sun Oct 23 2005 Olivier Thauvin <nanardon@mandriva.org> 4.4.2-5mdk
- Fix #19392

* Fri Sep 16 2005 Gwenole Beauchesne <gbeauchesne@mandriva.com> 4.4.2-4mdk
- buildrequires: rpm-mandriva-setup-build
- fix simple coloring patch, aka merge it correctly
- re-add the no-doc-conflicts patch for colored packages

* Tue Aug 30 2005 Olivier Thauvin <nanardon@mandriva.org> 4.4.2-3mdk
- patch 80: fix #17774
- patch 81, 82: should fix ordering issue
- BuildRequires: bzip2-devel (thanks Christian)

* Sat Aug 20 2005 Frederic Lepied <flepied@mandriva.com> 4.4.2-2mdk
- 79: fix deadlock from RedHat bug #146549.

* Fri Jul 22 2005 Olivier Thauvin <nanardon@mandriva.org> 4.4.2-1mdk
- 4.4.2
- remove patch:
    52: merged upstream
    67: fixed upstream
    73: merged upstream
    78: merged upstream
    79: merged upstream
    32, 33, 36: no more need hack
- rename rpm-python to python-rpm    
- use fnctl when not using futex
- use nptl only on few arches (ppc* x86_64 pentium3,4/Athlon)

* Thu Jun 23 2005 Olivier Thauvin <nanardon@mandriva.org> 4.4.1-10mdk
- add requires to rpm-build after the rpm-mandriva-setup split

* Tue Jun 21 2005 Olivier Thauvin <nanardon@mandriva.org> 4.4.1-9mdk
- Enable NPTL and co
- rework patch77: allow %%_srcdefattr as macro for src.rpm
- Patch78: reread few macro between build
- Patch79: fix rpm --eval '%%' overflow

* Fri Jun 17 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 4.4.1-8mdk
- Move dependencies on unzip, make and elfutils from rpm to rpm-build

* Sun Jun 05 2005 Olivier Thauvin <nanardon@mandriva.org> 4.4.1-7mdk
- patch77: allow to set root/root as owner of files in src.rpm
- rebuild with neon 0.24 as it moved in main instead 0.25

* Thu Jun 02 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 4.4.1-6mdk
- Patch 76 : allow to rebuild db with --root option

* Wed May 18 2005 Olivier Thauvin <nanardon@mandriva.org> 4.4.1-5mdk
- update french translation
- disable NPTL system + --with to enable it
- --w/o pyhton switch
- remove db_private patch as it breaks concurrent access

* Mon May 16 2005 Olivier Thauvin <nanardon@mandriva.org> 4.4.1-4mdk
- really apply patch (I sucks)
- some cleaning

* Mon May 16 2005 Olivier Thauvin <nanardon@mandriva.org> 4.4.1-3mdk
- Patch71: Ordering transaction on erasure
- Patch72: rpm -[Ui] check files conflicts
- Patch73,74: Fedora patch, fixing bug

* Fri May 13 2005 Olivier Thauvin <nanardon@mandriva.org> 4.4.1-2mdk
- patch70: allow rpm -bb --short-circuit
- conflicts man-pages-pl < 0.4-9mdk
- move spec mode for emacs into rpm-mandriva-setup
- buildrequires
- remove locales files from libpopt

* Wed May 11 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 4.4.1-1mdk
- Adapt part of the coloring patch (patch 62)
- Fix a few French translations (patch 69)
- Require libneon 0.25

* Mon May 09 2005 Olivier Thauvin <nanardon@mandriva.org> 4.4.1-0.7mdk
- BuildRequires readline-devel (P.O. Karlsen)
- --disable-{posixmutexes,pthreadsmutexes} on sparc (P.O. Karlsen)
- patch68: being able to read old rpms
- update source url
- fix file list for ppc (C. Welvaart)

* Fri May 06 2005 Olivier Thauvin <nanardon@mandriva.org> 4.4.1-0.6mdk
- use system sqlite
- force -fPIC on amd64 (for popt)
- perform test for popt
- patch67 fix build with gcc4

* Wed May 04 2005 Olivier Thauvin <nanardon@mandriva.org> 4.4.1-0.5mdk
- workaround make -j

* Wed May 04 2005 Olivier Thauvin <nanardon@mandriva.org> 4.4.1-0.4mdk
- 4.4.1
- remove biarch, use mklibname (see 4.2.3-10mdk)
- do no longer patch the config, use /usr/lib/rpm/VENDOR/rpmrc instead
- require rpm-mandriva-setup
- remove many obsoletes patch
- do not longer provide update-alternative
- more defined macros in the spec, less hardcode patch

* Tue May 03 2005 Pixel <pixel@mandriva.com> 4.2.3-11mdk
- emacs spec mode:
  - use rpm-find-spec-version-with-shell by default, and enhance it
  - handle release built using mkrel macro (in rpm-increase-release-tag)

* Thu Apr 28 2005 Olivier Thauvin <nanardon@mandriva.org> 4.2.3-10mdk
- split libs into separated package to make rpm update easier for URPM

* Thu Mar 10 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.2.3-9mdk
- bump multiarch-utils requires
- ignore conflicts in gnome-doc html files, install the latest files

* Wed Mar 09 2005 Frederic Lepied <flepied@mandrakesoft.com> 4.2.3-8mdk
- fix tr call in mono patch (bug #14449)
- fix bzip2 call (bug #7663)
- encode ru man pages in KOI8-R (bug #10219 and #12613)

* Fri Feb 25 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.2.3-8mdk
- hack to always install the latest arch-independent gtk-doc html
  files and man pages, aka. don't conflict on biarch platforms

* Fri Feb 25 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.2.3-7mdk
- popt is now a biarch package

* Thu Feb 24 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.2.3-6mdk
- requires multiarch-utils >= 1.0.7-1mdk
- RPM_INSTALL_LANG support is obsolete for MDK >= 10.2 (rafael)

* Tue Feb 08 2005 Frederic Lepied <flepied@mandrakesoft.com> 4.2.3-5mdk
- added mkrel macro (Buchan)
- changed group System/X11 from System/XFree86

* Thu Jan 27 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.2.3-4mdk
- newer multiarch-utils requires
- generate package script autoreqs only if requested (#13268)
- don't install .delta.rpm directly, use applydeltarpm first (SuSE)

* Mon Jan 24 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.2.3-3mdk
- minor cleanups
- check for files that ought to be marked as %%multiarch

* Thu Jan 20 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.2.3-2mdk
- newer multiarch-utils requires
- enable and improve file coloring
  * use file colors even if still using the external dependencies generator
  * assign a color to *.so symlinks to mix -devel packages
  * assign a color to *.a archives to mix -{static,}-devel packages

* Fri Jan 14 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.2.3-1mdk
- multiarch-utils autoreq
- allow build of 32-bit RPMs on x86-64
- ppc64 fixes
- update from 4.2-branch
  * auto-relocation fixes on ia64
  * change default behavior to resolve file conflicts as LIFO
  * generate debuginfo for setuid binaries

* Fri Jan 07 2005 Frederic Lepied <flepied@mandrakesoft.com> 4.2.2-19mdk
- compile --with-glob to avoid a problem with the internal glob code.

* Thu Jan 06 2005 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 4.2.2-18mdk
- Add patch 60 (Guillaume Rousse): make find-requires ignore dependencies on
  linux-incompatible perl modules. (bug #12695)

* Mon Dec 06 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 4.2.2-17mdk
- Add patch 59, necessary for the smart package manager (new function
  rpmSingleHeaderFromFD() in the python bindings)

* Sat Dec 04 2004 Frederic Lepied <flepied@mandrakesoft.com> 4.2.2-16mdk
- rebuild for python 2.4

* Fri Aug 06 2004 Frederic Lepied <flepied@mandrakesoft.com> 4.2.2-15mdk
- use system zlib

* Thu Jul 29 2004 Frederic Lepied <flepied@mandrakesoft.com> 4.2.2-14mdk
- fix mono patch (bug #7201)

* Wed Jul 28 2004 Frederic Lepied <flepied@mandrakesoft.com> 4.2.2-13mdk
- use mono-find-requires and mono-find-provides if present (Götz Waschk) (bug #7201)

* Wed Jul 28 2004 Frederic Lepied <flepied@mandrakesoft.com> 4.2.2-12mdk
- use a correct implementation of cpuid (Gwenole)
- return None instead of [] in rpm-python (Paul Nasrat)
- add /var/spool/repackage (bug #9874)
- handle /usr/lib/gcc/ directories for devel() deps too (Gwenole)

* Thu May 20 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.2.2-10mdk
- switch back to x86_64 packages on 64-bit extended platforms

* Fri May 14 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.2.2-9mdk
- fix /usr/lib/rpmpopt symlink
- use -mtune=pentiumpro on any MDK >= 10.0

* Fri Apr 16 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 4.2.2-8mdk
- When unlocking the RPMLOCK file, don't forget to close(2) it too.
