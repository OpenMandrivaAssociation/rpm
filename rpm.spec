%define	_target_vendor mandriva

%bcond_with	bootstrap
%bcond_with	debug
# Use --with moondrake for Moondrake branding
# anything else for OpenMandriva branding
%bcond_with	moondrake

%bcond_without	ossp_uuid
%bcond_without	augeas
%bcond_with	docs

#XXX: this macro is a bit awkward, better can be done!
%if %{with bootstrap}
%bcond_with	perl
%bcond_with	python
%bcond_with	tcl
%bcond_with	squirrel
%bcond_with	embed
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

%define bdb db52

%define libver 5.4
%define minorver 10
%define srcver %{libver}.%{minorver}
#define	prereldate	20110712

%define librpmname %mklibname rpm %{libver}
%define librpmnamedevel %mklibname -d rpm
%define librpmstatic %mklibname -d -s rpm

Summary:	The RPM package management system
Name:		rpm
Epoch:		1
Version:	%{libver}.%{minorver}
Release:	%{?prereldate:0.%{prereldate}.}60
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
# GPG key used for signing OpenMandriva Association packages
Source100:	OMA-Cooker-PubKey.asc
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
Patch163:	rpm-5.4.10-openmandriva-name.patch
Patch1630:	rpm-5.4.10-new-moondrake-name.patch
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
Patch200:	rpm-5.4.10-armv7hl-rpm-macros-hardfloat-abi.patch
Patch201:       rpm-5.4.10-postpone_subpackage_build_failures.patch

# Do not generate pythonegg provides for python3 until we find a better solution
Patch202:       rpm-5.4.10-python3-egg-reqs.patch

# (tpg) do not build static libs by default
Patch203:	rpm-5.4.10-configure-disable-static.patch

# (bero) Add libpackage macro -- these lines are replicated into way too many spec files
Patch204:	rpm-5.4.10-libpackage-macro.patch
# fedya add aarch64 macro
Patch205:	0001-add-aarch64-macro.patch
Patch206:	0001-fix-aarch64-rpm5-multiarch-headers-scripting.patch
Patch207:	fix-config-sub-in-configure.patch
Patch210:	rpm-5.4.12-fix-rpmpython-module-import-init.patch
Patch211:	rpm-5.4.12-truncate-output-buffer-after-use.patch
Patch212:	rpm-5.4.10-cmake-dependency-generator.patch
Patch213:	0001-Add-support-of-armv6j-hardfloat-for-RaspberryPi-port.patch
Patch214:	rpm-5.4.10-only-print-python-debug-output-if-requested.patch
Patch215:	rpm-5.4.14-add-more-archs-to-arm-macro.patch
Patch216:	rpm-5.4.14-ruby-archdirs.patch
Patch217:	rpm-5.4.14-ruby-abi-versioned.patch
Patch218:	rpm-5.4.14-gem_helper-spec-arg.patch
Patch219:	rpm-5.4.14-rubygems2-support.patch

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
Requires:	coreutils
Requires:	update-alternatives
Requires:	%{bdb}_recover
Suggests:	%{bdb}-utils
Requires:	%{librpmname} = %{EVRD}
Conflicts:	rpm-build < 1:5.3.10-0.20110422.3
Requires(pre):	coreutils
%rename		rpmconstant
%rename		multiarch-utils
Obsoletes:	rpm-manbo-setup < 2-6
Provides:	rpm-manbo-setup = 2-6
Obsoletes:	rpm-mandriva-setup < 1.140-6
Provides:	rpm-mandriva-setup = 1.140-6
%rename		rpm-mandriva-setup
%rename		rpm-manbo-setup
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
Obsoletes:	rpm-manbo-setup-build < 2-6
Provides:	rpm-manbo-setup-build = 2-6
Obsoletes:	rpm-mandriva-setup-build < 1.140-6
Provides:	rpm-mandriva-setup-build = 1.140-6
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
%patch6 -p1 -b .keyserver~
%patch7 -p1 -b .libexec~
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
%if ! %{with moondrake}
%patch163 -p1 -b .ovm~
%else
%patch1630 -p1 -b .mdk~
%endif
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
%patch201 -p1 -b .subpackage_errors~
%patch202 -p1 -b .python3~
# (tpg) enable only for cooker
# omv2013.0 branch is not a cooker anymore so it is safe
# to push this
%if "%{distro_branch}" == "Cooker"
%patch203 -p1 -b .static~
%endif
%patch204 -p1 -b .libpackage~
%patch206 -p1 -b .aarch64_multiarch
%patch207 -p1 -b .update_config.subguess
%patch210 -p1 -b .rpmpythonmod~
%patch211 -p1 -b .rpmpythontrunc~
%patch212 -p1 -b .cmakedeps~
%patch214 -p1 -b .py_debugout~
%patch215 -p1 -b .armx~
%patch216 -p1 -b .rubyarchdirs~
%patch217 -p1 -b .rubyabiver~
%patch218 -p1 -b .gem_spec~
%patch219 -p1 -b .rubygems2~

# aclocal's AC_DEFUN fixing messes up a strange construct in iconv.m4
sed -i -e 's,aclocal -I,aclocal --dont-fix -I,g' autogen.sh
#required by P55, P80, P81, P94..
./autogen.sh

mkdir -p cpu-os-macros
tar -xf %{SOURCE3} -C cpu-os-macros
%patch145 -p1
%patch200 -p1
%patch205 -p1
%patch213 -p1

%build
%configure2_5x	--enable-nls \
		--with-pic \
        --enable-static \
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
# (tpg) this file name should be changed to something like distro.macros
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
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}" CCCDLFLAGS="-fno-PIE -fPIC"
sed -i -e 's,-fPIC -fno-PIE,-fno-PIE -fPIC,g' ../perl/Makefile.perl
%make
popd
%endif

%check
make check

%install

# (tpg) THIS IS VERY IMPORTANT !!!
cp %SOURCE100 .
mkdir -p %{buildroot}%{_sysconfdir}/RPM-GPG-KEYS
install -m644 %{SOURCE100} %{buildroot}%{_sysconfdir}/RPM-GPG-KEYS/OMA-Cooker-PubKey.asc

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
%{_sysconfdir}/RPM-GPG-KEYS/OMA-Cooker-PubKey.asc

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

%pubkey OMA-Cooker-PubKey.asc

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
