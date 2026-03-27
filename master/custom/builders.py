from dataclasses import dataclass
from typing import Optional

from custom.factories import (
    BaseBuild,
    UnixBuild,
    UnixPerfBuild,
    UnixOddballsBuild,
    RHEL8Build,
    CentOS9Build,
    FedoraStableBuild,
    FedoraRawhideBuild,
    FedoraRawhideFreedthreadingBuild,
    UnixAsanBuild,
    UnixAsanDebugBuild,
    UnixBigmemBuild,
    UnixTraceRefsBuild,
    UnixRefleakBuild,
    UnixNoGilBuild,
    UnixNoGilRefleakBuild,
    MacOSAsanNoGilBuild,
    ClangUnixBuild,
    ClangUbsanLinuxBuild,
    ClangUbsanFunctionLinuxBuild,
    ClangUnixInstalledBuild,
    SharedUnixBuild,
    SlowDebugUnixBuild,
    SlowNonDebugUnixBuild,
    SlowNonDebugUnixBuild15BitDigits,
    SlowUnixInstalledBuild,
    NonDebugUnixBuild,
    UnixInstalledBuild,
    LTONonDebugUnixBuild,
    LTOPGONonDebugBuild,
    RHEL8NoBuiltinHashesUnixBuild,
    RHEL8NoBuiltinHashesUnixBuildExceptBlake2,
    CentOS9NoBuiltinHashesUnixBuild,
    CentOS9NoBuiltinHashesUnixBuildExceptBlake2,
    Windows64Build,
    Windows64BigmemBuild,
    Windows64NoGilBuild,
    Windows64PGOBuild,
    Windows64PGONoGilBuild,
    Windows64RefleakBuild,
    Windows64ReleaseBuild,
    MacOSArmWithBrewBuild,
    MacOSArmWithBrewNoGilBuild,
    MacOSArmWithBrewNoGilRefleakBuild,
    WindowsARM64Build,
    WindowsARM64ReleaseBuild,
    Wasm32WasiCrossBuild,
    Wasm32WasiPreview1DebugBuild,
    IOSARM64SimulatorBuild,
    AndroidBuild,
    EmscriptenBuild,
    ValgrindBuild,
)
from custom.workers import CPythonWorker

# A builder can be marked as stable when at least the 10 latest builds are
# successful, but it's way better to wait at least for at least one week of
# successful builds before considering to mark a builder as stable.
STABLE = "stable"

# New builders should always be marked as unstable. If a stable builder starts
# to fail randomly, it can be downgraded to unstable if it is not a Tier-1 or
# Tier-2 builder.
UNSTABLE = "unstable"

# https://peps.python.org/pep-0011/ defines Platform Support Tiers
TIER_1 = "tier-1"
TIER_2 = "tier-2"
TIER_3 = "tier-3"
NO_TIER = None


@dataclass
class CPythonBuilder:

    name: str
    factory: BaseBuild
    stability: str
    tier: Optional[str]
    workers: list[CPythonWorker]

_builders = None

def get_builders(settings, workers):
    global _builders
    if _builders is not None:
        return _builders
    # Override with a default simple worker if we are using local workers
    if settings.use_local_worker:
        return [
            CPythonBuilder(
                "Test Builder",
                globals().get(settings.local_worker_buildfactory, UnixBuild),
                STABLE,
                NO_TIER,
                [workers[0]],
            ),
        ]

    workers_by_name = {w.name: w for w in workers}

    def get_workers(name=None, tags=None):
        if name is not None:
            return [workers_by_name[name]]
        if tags is None:
            raise ValueError('must provide either name or tags')
        return [w for w in workers if tags.issubset(w.tags)]

    w = get_workers
    cpb = CPythonBuilder
    _builders = [
        # -- Stable Tier-1 builders ------------------------------------------
        # Linux x86-64 GCC
        cpb(
            "AMD64 Debian root",
            UnixBuild,
            STABLE,
            TIER_1,
            w("angelico-debian-amd64"),
        ),
        cpb(
            "AMD64 Ubuntu Shared",
            SharedUnixBuild,
            STABLE,
            TIER_1,
            w("bolen-ubuntu"),
        ),
        cpb(
            "AMD64 Fedora Stable",
            FedoraStableBuild,
            STABLE,
            TIER_1,
            w("cstratak-fedora-stable-x86_64"),
        ),
        cpb(
            "AMD64 Fedora Stable Refleaks",
            UnixRefleakBuild,
            STABLE,
            TIER_1,
            w("cstratak-fedora-stable-x86_64"),
        ),
        cpb(
            "AMD64 Fedora Stable LTO",
            LTONonDebugUnixBuild,
            STABLE,
            TIER_1,
            w("cstratak-fedora-stable-x86_64"),
        ),
        cpb(
            "AMD64 Fedora Stable LTO + PGO",
            LTOPGONonDebugBuild,
            STABLE,
            TIER_1,
            w("cstratak-fedora-stable-x86_64"),
        ),
        cpb(
            "AMD64 RHEL8",
            RHEL8Build,
            STABLE,
            TIER_1,
            w("cstratak-RHEL8-x86_64"),
        ),
        cpb(
            "AMD64 RHEL8 Refleaks",
            UnixRefleakBuild,
            STABLE,
            TIER_1,
            w("cstratak-RHEL8-x86_64"),
        ),
        cpb(
            "AMD64 RHEL8 LTO",
            LTONonDebugUnixBuild,
            STABLE,
            TIER_1,
            w("cstratak-RHEL8-x86_64"),
        ),
        cpb(
            "AMD64 RHEL8 LTO + PGO",
            LTOPGONonDebugBuild,
            STABLE,
            TIER_1,
            w("cstratak-RHEL8-x86_64"),
        ),
        cpb(
            "AMD64 CentOS9 NoGIL",
            UnixNoGilBuild,
            STABLE,
            TIER_1,
            w("itamaro-centos-aws"),
        ),
        cpb(
            "AMD64 CentOS9 NoGIL Refleaks",
            UnixNoGilRefleakBuild,
            STABLE,
            TIER_1,
            w("itamaro-centos-aws"),
        ),

        # Windows x86-64 MSVC
        cpb(
            "AMD64 Windows10",
            Windows64Build,
            STABLE,
            TIER_1,
            w("bolen-windows10"),
        ),
        cpb(
            "AMD64 Windows11 Bigmem",
            Windows64BigmemBuild,
            STABLE,
            TIER_1,
            w("ambv-bb-win11"),
        ),
        cpb(
            "AMD64 Windows11 Non-Debug",
            Windows64ReleaseBuild,
            STABLE,
            TIER_1,
            w("ware-win11"),
        ),
        cpb(
            "AMD64 Windows11 Refleaks",
            Windows64RefleakBuild,
            STABLE,
            TIER_1,
            w("ware-win11"),
        ),
        cpb(
            "AMD64 Windows Server 2022 NoGIL",
            Windows64NoGilBuild,
            STABLE,
            TIER_1,
            w("itamaro-win64-srv-22-aws"),
        ),
        cpb(
            "AMD64 Windows PGO NoGIL",
            Windows64PGONoGilBuild,
            STABLE,
            TIER_1,
            w("itamaro-win64-srv-22-aws"),
        ),

        # -- Stable Tier-2 builder ------------------------------------------
        # Fedora Linux x86-64 Clang
        cpb(
            "AMD64 Fedora Stable Clang",
            ClangUnixBuild,
            STABLE,
            TIER_2,
            w("cstratak-fedora-stable-x86_64"),
        ),
        cpb(
            "AMD64 Fedora Stable Clang Installed",
            ClangUnixInstalledBuild,
            STABLE,
            TIER_2,
            w("cstratak-fedora-stable-x86_64"),
        ),

        # Fedora Linux ppc64le GCC
        cpb(
            "PPC64LE Fedora Stable",
            FedoraStableBuild,
            STABLE,
            TIER_2,
            w("cstratak-fedora-stable-ppc64le"),
        ),
        cpb(
            "PPC64LE Fedora Stable Refleaks",
            UnixRefleakBuild,
            STABLE,
            TIER_2,
            w("cstratak-fedora-stable-ppc64le"),
        ),
        cpb(
            "PPC64LE Fedora Stable LTO",
            LTONonDebugUnixBuild,
            STABLE,
            TIER_2,
            w("cstratak-fedora-stable-ppc64le"),
        ),
        cpb(
            "PPC64LE Fedora Stable LTO + PGO",
            LTOPGONonDebugBuild,
            STABLE,
            TIER_2,
            w("cstratak-fedora-stable-ppc64le"),
        ),

        # RHEL8 ppc64le GCC
        cpb(
            "PPC64LE RHEL8",
            RHEL8Build,
            STABLE,
            TIER_2,
            w("cstratak-RHEL8-ppc64le"),
        ),
        cpb(
            "PPC64LE RHEL8 Refleaks",
            UnixRefleakBuild,
            STABLE,
            TIER_2,
            w("cstratak-RHEL8-ppc64le"),
        ),
        cpb(
            "PPC64LE RHEL8 LTO",
            LTONonDebugUnixBuild,
            STABLE,
            TIER_2,
            w("cstratak-RHEL8-ppc64le"),
        ),
        cpb(
            "PPC64LE RHEL8 LTO + PGO",
            LTOPGONonDebugBuild,
            STABLE,
            TIER_2,
            w("cstratak-RHEL8-ppc64le"),
        ),

        # macOS aarch64 clang
        cpb(
            "ARM64 macOS",
            MacOSArmWithBrewBuild,
            STABLE,
            TIER_2,
            w("pablogsal-macos-m1"),
        ),
        cpb(
            "ARM64 MacOS M1 NoGIL",
            MacOSArmWithBrewNoGilBuild,
            STABLE,
            TIER_2,
            w("itamaro-macos-arm64-aws"),
        ),
        cpb(
            "ARM64 MacOS M1 Refleaks NoGIL",
            MacOSArmWithBrewNoGilRefleakBuild,
            STABLE,
            TIER_2,
            w("itamaro-macos-arm64-aws"),
        ),

        # macOS x86-64 clang
        cpb(
            "x86-64 macOS",
            UnixBuild,
            STABLE,
            TIER_2,
            w("billenstein-macos"),
        ),
        cpb(
            "x86-64 MacOS Intel NoGIL",
            UnixNoGilBuild,
            STABLE,
            TIER_2,
            w("itamaro-macos-intel-aws"),
        ),
        cpb(
            "x86-64 MacOS Intel ASAN NoGIL",
            MacOSAsanNoGilBuild,
            STABLE,
            TIER_2,
            w("itamaro-macos-intel-aws"),
        ),

        # WASI
        cpb(
            "wasm32-wasi Non-Debug",
            Wasm32WasiCrossBuild,
            STABLE,
            TIER_2,
            w("bcannon-wasi"),
        ),
        cpb(
            "wasm32-wasi",
            Wasm32WasiPreview1DebugBuild,
            STABLE,
            TIER_2,
            w("bcannon-wasi"),
        ),

        # -- Stable Tier-3 builder ------------------------------------------
        # Fedora Linux s390x GCC/Clang
        cpb(
            "s390x Fedora Stable",
            UnixBuild,
            STABLE,
            TIER_3,
            w("cstratak-fedora-stable-s390x"),
        ),
        cpb(
            "s390x Fedora Stable Refleaks",
            UnixRefleakBuild,
            STABLE,
            TIER_3,
            w("cstratak-fedora-stable-s390x"),
        ),
        cpb(
            "s390x Fedora Stable Clang",
            ClangUnixBuild,
            STABLE,
            TIER_3,
            w("cstratak-fedora-stable-s390x"),
        ),
        cpb(
            "s390x Fedora Stable Clang Installed",
            ClangUnixInstalledBuild,
            STABLE,
            TIER_3,
            w("cstratak-fedora-stable-s390x"),
        ),
        cpb(
            "s390x Fedora Stable LTO",
            LTONonDebugUnixBuild,
            STABLE,
            TIER_3,
            w("cstratak-fedora-stable-s390x"),
        ),
        cpb(
            "s390x Fedora Stable LTO + PGO",
            LTOPGONonDebugBuild,
            STABLE,
            TIER_3,
            w("cstratak-fedora-stable-s390x"),
        ),

        # RHEL9 GCC
        cpb(
            "s390x RHEL9",
            UnixBuild,
            STABLE,
            TIER_3,
            w("cstratak-rhel9-s390x"),
        ),
        cpb(
            "s390x RHEL9 Refleaks",
            UnixRefleakBuild,
            STABLE,
            TIER_3,
            w("cstratak-rhel9-s390x"),
        ),
        cpb(
            "s390x RHEL9 LTO",
            LTONonDebugUnixBuild,
            STABLE,
            TIER_3,
            w("cstratak-rhel9-s390x"),
        ),
        cpb(
            "s390x RHEL9 LTO + PGO",
            LTOPGONonDebugBuild,
            STABLE,
            TIER_3,
            w("cstratak-rhel9-s390x"),
        ),

        # RHEL8 GCC
        cpb(
            "s390x RHEL8",
            UnixBuild,
            STABLE,
            TIER_3,
            w("cstratak-rhel8-s390x"),
        ),
        cpb(
            "s390x RHEL8 Refleaks",
            UnixRefleakBuild,
            STABLE,
            TIER_3,
            w("cstratak-rhel8-s390x"),
        ),
        cpb(
            "s390x RHEL8 LTO",
            LTONonDebugUnixBuild,
            STABLE,
            TIER_3,
            w("cstratak-rhel8-s390x"),
        ),
        cpb(
            "s390x RHEL8 LTO + PGO",
            LTOPGONonDebugBuild,
            STABLE,
            TIER_3,
            w("cstratak-rhel8-s390x"),
        ),

        # Fedora Linux ppc64le Clang
        cpb(
            "PPC64LE Fedora Stable Clang",
            ClangUnixBuild,
            STABLE,
            TIER_3,
            w("cstratak-fedora-stable-ppc64le"),
        ),
        cpb(
            "PPC64LE Fedora Stable Clang Installed",
            ClangUnixInstalledBuild,
            STABLE,
            TIER_3,
            w("cstratak-fedora-stable-ppc64le"),
        ),

        # Linux armv7l (32-bit) GCC
        cpb(
            "ARM Raspbian",
            SlowNonDebugUnixBuild15BitDigits,
            STABLE,
            TIER_3,
            w("gps-raspbian"),
        ),

        # Linux armv8 (64-bit) GCC
        cpb(
            "ARM64 Raspbian",
            SlowNonDebugUnixBuild,
            STABLE,
            TIER_3,
            w("stan-raspbian"),
        ),
        cpb(
            "ARM64 Raspbian Debug",
            SlowDebugUnixBuild,
            STABLE,
            TIER_3,
            w("savannah-raspbian"),
        ),

        # FreeBSD x86-64 clang
        cpb(
            "AMD64 FreeBSD",
            UnixBuild,
            STABLE,
            TIER_3,
            w("ware-freebsd"),
        ),
        cpb(
            "AMD64 FreeBSD Refleaks",
            UnixRefleakBuild,
            STABLE,
            TIER_3,
            w("ware-freebsd"),
        ),
        cpb(
            "AMD64 FreeBSD14",
            UnixBuild,
            STABLE,
            TIER_3,
            w("opsec-fbsd14"),
        ),

        # Windows aarch64 MSVC
        cpb(
            "ARM64 Windows",
            WindowsARM64Build,
            STABLE,
            TIER_3,
            w("linaro-win-arm64"),
        ),
        cpb(
            "ARM64 Windows Non-Debug",
            WindowsARM64ReleaseBuild,
            STABLE,
            TIER_3,
            w("linaro-win-arm64"),
        ),

        # iOS
        cpb(
            "iOS ARM64 Simulator",
            IOSARM64SimulatorBuild,
            STABLE,
            TIER_3,
            w("rkm-arm64-ios-simulator"),
        ),

        # Android
        cpb(
            "aarch64 Android",
            AndroidBuild,
            STABLE,
            TIER_3,
            w("mhsmith-android-aarch64"),
        ),
        cpb(
            "AMD64 Android",
            AndroidBuild,
            STABLE,
            TIER_3,
            w("mhsmith-android-x86_64"),
        ),

        # -- Stable No Tier builders ----------------------------------------
        # Linux x86-64 GCC musl
        cpb(
            "AMD64 Alpine Linux",
            UnixBuild,
            STABLE,
            NO_TIER,
            w("ware-alpine"),
        ),

        # Linux x86-64 GCC/Clang
        # Special builds: FIPS, ASAN, UBSAN, TraceRefs, Perf, etc.
        cpb(
            "AMD64 RHEL8 FIPS Only Blake2 Builtin Hash",
            RHEL8NoBuiltinHashesUnixBuildExceptBlake2,
            STABLE,
            NO_TIER,
            w("cstratak-RHEL8-fips-x86_64"),
        ),
        cpb(
            "AMD64 Arch Linux Asan",
            UnixAsanBuild,
            STABLE,
            NO_TIER,
            w("pablogsal-arch-x86_64"),
        ),
        cpb(
            "AMD64 Arch Linux Asan Debug",
            UnixAsanDebugBuild,
            STABLE,
            NO_TIER,
            w("pablogsal-arch-x86_64"),
        ),
        cpb(
            "AMD64 Arch Linux TraceRefs",
            UnixTraceRefsBuild,
            STABLE,
            NO_TIER,
            w("pablogsal-arch-x86_64"),
        ),
        cpb(
            "AMD64 Arch Linux Perf",
            UnixPerfBuild,
            STABLE,
            NO_TIER,
            w("pablogsal-arch-x86_64"),
        ),
        cpb(
            "ARM Raspbian Linux Asan",
            UnixAsanBuild,
            STABLE,
            NO_TIER,
            w("pablogsal-rasp"),
        ),
        # UBSAN with -fno-sanitize=function, without which we currently fail
        # (as tracked in gh-111178). The full "AMD64 Arch Linux Usan" is
        # unstable, below
        cpb(
            "AMD64 Arch Linux Usan Function",
            ClangUbsanFunctionLinuxBuild,
            STABLE,
            NO_TIER,
            w("pablogsal-arch-x86_64"),
        ),

        # Linux x86 (32-bit) GCC
        cpb(
            "x86 Debian Non-Debug with X",
            NonDebugUnixBuild,
            STABLE,
            NO_TIER,
            w("ware-debian-x86"),
        ),
        cpb(
            "x86 Debian Installed with X",
            UnixInstalledBuild,
            STABLE,
            NO_TIER,
            w("ware-debian-x86"),
        ),

        # -- Unstable Tier-1 builders ---------------------------------------
        # Ubuntu Linux AArch64
        cpb(
            "aarch64 Ubuntu 24.04 BigMem",
            UnixBigmemBuild,
            UNSTABLE,
            TIER_1,
            w("diegorusso-aarch64-bigmem"),
        ),

        # Tests that require the 'tzdata' and 'xpickle' resources
        cpb(
            "aarch64 Ubuntu Oddballs",
            UnixOddballsBuild,
            UNSTABLE,
            TIER_1,
            w("stan-aarch64-ubuntu"),
        ),

        # Linux x86-64 GCC
        # Fedora Rawhide is unstable
        cpb(
            "AMD64 Fedora Rawhide",
            FedoraRawhideBuild,
            UNSTABLE,
            TIER_1,
            w("cstratak-fedora-rawhide-x86_64"),
        ),
        cpb(
            "AMD64 Fedora Rawhide Refleaks",
            UnixRefleakBuild,
            UNSTABLE,
            TIER_1,
            w("cstratak-fedora-rawhide-x86_64"),
        ),
        cpb(
            "AMD64 Fedora Rawhide LTO",
            LTONonDebugUnixBuild,
            UNSTABLE,
            TIER_1,
            w("cstratak-fedora-rawhide-x86_64"),
        ),
        cpb(
            "AMD64 Fedora Rawhide LTO + PGO",
            LTOPGONonDebugBuild,
            UNSTABLE,
            TIER_1,
            w("cstratak-fedora-rawhide-x86_64"),
        ),

        cpb(
            "AMD64 Ubuntu",
            UnixBuild,
            UNSTABLE,
            TIER_1,
            w("skumaran-ubuntu-x86_64"),
        ),

        cpb(
            "AMD64 RHEL8 FIPS No Builtin Hashes",
            RHEL8NoBuiltinHashesUnixBuild,
            UNSTABLE,
            TIER_1,
            w("cstratak-RHEL8-fips-x86_64"),
        ),

        cpb(
            "AMD64 CentOS9",
            CentOS9Build,
            UNSTABLE,
            TIER_1,
            w("cstratak-CentOS9-x86_64"),
        ),
        cpb(
            "AMD64 CentOS9 Refleaks",
            UnixRefleakBuild,
            UNSTABLE,
            TIER_1,
            w("cstratak-CentOS9-x86_64"),
        ),
        cpb(
            "AMD64 CentOS9 LTO",
            LTONonDebugUnixBuild,
            UNSTABLE,
            TIER_1,
            w("cstratak-CentOS9-x86_64"),
        ),
        cpb(
            "AMD64 CentOS9 LTO + PGO",
            LTOPGONonDebugBuild,
            UNSTABLE,
            TIER_1,
            w("cstratak-CentOS9-x86_64"),
        ),
        cpb(
            "AMD64 CentOS9 FIPS Only Blake2 Builtin Hash",
            CentOS9NoBuiltinHashesUnixBuildExceptBlake2,
            UNSTABLE,
            TIER_1,
            w("cstratak-CentOS9-fips-x86_64"),
        ),
        cpb(
            "AMD64 CentOS9 FIPS No Builtin Hashes",
            CentOS9NoBuiltinHashesUnixBuild,
            UNSTABLE,
            TIER_1,
            w("cstratak-CentOS9-fips-x86_64"),
        ),

        cpb(
            "AMD64 Arch Linux Valgrind",
            ValgrindBuild,
            UNSTABLE,
            TIER_1,
            w("pablogsal-arch-x86_64"),
        ),

        # Windows MSVC
        cpb(
            "AMD64 Windows PGO",
            Windows64PGOBuild,
            UNSTABLE,
            TIER_1,
            w("bolen-windows10"),
        ),

        # -- Unstable Tier-2 builders ---------------------------------------
        # Linux x86-64 Clang
        # Fedora Rawhide is unstable
        # UBSan is a special build
        cpb(
            "AMD64 Fedora Rawhide Clang",
            ClangUnixBuild,
            UNSTABLE,
            TIER_2,
            w("cstratak-fedora-rawhide-x86_64"),
        ),
        cpb(
            "AMD64 Fedora Rawhide Clang Installed",
            ClangUnixInstalledBuild,
            UNSTABLE,
            TIER_2,
            w("cstratak-fedora-rawhide-x86_64"),
        ),

        # Fedora Linux ppc64le GCC
        # Fedora Rawhide is unstable
        cpb(
            "PPC64LE Fedora Rawhide",
            FedoraRawhideBuild,
            UNSTABLE,
            TIER_2,
            w("cstratak-fedora-rawhide-ppc64le"),
        ),
        cpb(
            "PPC64LE Fedora Rawhide Refleaks",
            UnixRefleakBuild,
            UNSTABLE,
            TIER_2,
            w("cstratak-fedora-rawhide-ppc64le"),
        ),
        cpb(
            "PPC64LE Fedora Rawhide LTO",
            LTONonDebugUnixBuild,
            UNSTABLE,
            TIER_2,
            w("cstratak-fedora-rawhide-ppc64le"),
        ),
        cpb(
            "PPC64LE Fedora Rawhide LTO + PGO",
            LTOPGONonDebugBuild,
            UNSTABLE,
            TIER_2,
            w("cstratak-fedora-rawhide-ppc64le"),
        ),

        # CentOS Stream 9 Linux ppc64le GCC
        cpb(
            "PPC64LE CentOS9",
            CentOS9Build,
            UNSTABLE,
            TIER_2,
            w("cstratak-CentOS9-ppc64le"),
        ),
        cpb(
            "PPC64LE CentOS9 Refleaks",
            UnixRefleakBuild,
            UNSTABLE,
            TIER_2,
            w("cstratak-CentOS9-ppc64le"),
        ),
        cpb(
            "PPC64LE CentOS9 LTO",
            LTONonDebugUnixBuild,
            UNSTABLE,
            TIER_2,
            w("cstratak-CentOS9-ppc64le"),
        ),
        cpb(
            "PPC64LE CentOS9 LTO + PGO",
            LTOPGONonDebugBuild,
            UNSTABLE,
            TIER_2,
            w("cstratak-CentOS9-ppc64le"),
        ),

        # Fedora Linux aarch64 GCC/Clang
        # Fedora Rawhide is unstable
        cpb(
            "aarch64 Fedora Rawhide",
            FedoraRawhideBuild,
            UNSTABLE,
            TIER_2,
            w("cstratak-fedora-rawhide-aarch64"),
        ),
        cpb(
            "aarch64 Fedora Rawhide Refleaks",
            UnixRefleakBuild,
            UNSTABLE,
            TIER_2,
            w("cstratak-fedora-rawhide-aarch64"),
        ),
        cpb(
            "aarch64 Fedora Rawhide Clang",
            ClangUnixBuild,
            UNSTABLE,
            TIER_2,
            w("cstratak-fedora-rawhide-aarch64"),
        ),
        cpb(
            "aarch64 Fedora Rawhide Clang Installed",
            ClangUnixInstalledBuild,
            UNSTABLE,
            TIER_2,
            w("cstratak-fedora-rawhide-aarch64"),
        ),
        cpb(
            "aarch64 Fedora Rawhide LTO",
            LTONonDebugUnixBuild,
            UNSTABLE,
            TIER_2,
            w("cstratak-fedora-rawhide-aarch64"),
        ),
        cpb(
            "aarch64 Fedora Rawhide LTO + PGO",
            LTOPGONonDebugBuild,
            UNSTABLE,
            TIER_2,
            w("cstratak-fedora-rawhide-aarch64"),
        ),

        # Fedora Linux aarch64 GCC/clang
        # (marked unstable for a hardware migration)
        cpb(
            "aarch64 Fedora Stable",
            FedoraStableBuild,
            UNSTABLE,
            TIER_2,
            w("cstratak-fedora-stable-aarch64"),
        ),
        cpb(
            "aarch64 Fedora Stable Refleaks",
            UnixRefleakBuild,
            UNSTABLE,
            TIER_2,
            w("cstratak-fedora-stable-aarch64"),
        ),
        cpb(
            "aarch64 Fedora Stable Clang",
            ClangUnixBuild,
            UNSTABLE,
            TIER_2,
            w("cstratak-fedora-stable-aarch64"),
        ),
        cpb(
            "aarch64 Fedora Stable Clang Installed",
            ClangUnixInstalledBuild,
            UNSTABLE,
            TIER_2,
            w("cstratak-fedora-stable-aarch64"),
        ),
        cpb(
            "aarch64 Fedora Stable LTO",
            LTONonDebugUnixBuild,
            UNSTABLE,
            TIER_2,
            w("cstratak-fedora-stable-aarch64"),
        ),
        cpb(
            "aarch64 Fedora Stable LTO + PGO",
            LTOPGONonDebugBuild,
            UNSTABLE,
            TIER_2,
            w("cstratak-fedora-stable-aarch64"),
        ),

        # RHEL8 aarch64 GCC
        # (marked unstable for a hardware migration)
        cpb(
            "aarch64 RHEL8",
            RHEL8Build,
            UNSTABLE,
            TIER_2,
            w("cstratak-RHEL8-aarch64"),
        ),
        cpb(
            "aarch64 RHEL8 Refleaks",
            UnixRefleakBuild,
            UNSTABLE,
            TIER_2,
            w("cstratak-RHEL8-aarch64"),
        ),
        cpb(
            "aarch64 RHEL8 LTO",
            LTONonDebugUnixBuild,
            UNSTABLE,
            TIER_2,
            w("cstratak-RHEL8-aarch64"),
        ),
        cpb(
            "aarch64 RHEL8 LTO + PGO",
            LTOPGONonDebugBuild,
            UNSTABLE,
            TIER_2,
            w("cstratak-RHEL8-aarch64"),
        ),

        # CentOS Stream 9 Linux aarch64 GCC
        cpb(
            "aarch64 CentOS9 Refleaks",
            UnixRefleakBuild,
            UNSTABLE,
            TIER_2,
            w("cstratak-CentOS9-aarch64"),
        ),
        cpb(
            "aarch64 CentOS9 LTO",
            LTONonDebugUnixBuild,
            UNSTABLE,
            TIER_2,
            w("cstratak-CentOS9-aarch64"),
        ),
        cpb(
            "aarch64 CentOS9 LTO + PGO",
            LTOPGONonDebugBuild,
            UNSTABLE,
            TIER_2,
            w("cstratak-CentOS9-aarch64"),
        ),

        # WebAssembly
        cpb(
            "wasm32 WASI 8Core",
            Wasm32WasiCrossBuild,
            UNSTABLE,
            TIER_2,
            w("kushaldas-wasi"),
        ),

        # -- Unstable Tier-3 builders ---------------------------------------
        # Linux ppc64le Clang
        # Fedora Rawhide is unstable
        cpb(
            "PPC64LE Fedora Rawhide Clang",
            ClangUnixBuild,
            UNSTABLE,
            TIER_3,
            w("cstratak-fedora-rawhide-ppc64le"),
        ),
        cpb(
            "PPC64LE Fedora Rawhide Clang Installed",
            ClangUnixInstalledBuild,
            UNSTABLE,
            TIER_3,
            w("cstratak-fedora-rawhide-ppc64le"),
        ),

        # Linux s390x GCC/Clang
        cpb(
            "s390x Fedora Rawhide",
            UnixBuild,
            UNSTABLE,
            TIER_3,
            w("cstratak-fedora-rawhide-s390x"),
        ),
        cpb(
            "s390x Fedora Rawhide Refleaks",
            UnixRefleakBuild,
            UNSTABLE,
            TIER_3,
            w("cstratak-fedora-rawhide-s390x"),
        ),
        cpb(
            "s390x Fedora Rawhide Clang",
            ClangUnixBuild,
            UNSTABLE,
            TIER_3,
            w("cstratak-fedora-rawhide-s390x"),
        ),
        cpb(
            "s390x Fedora Rawhide Clang Installed",
            ClangUnixInstalledBuild,
            UNSTABLE,
            TIER_3,
            w("cstratak-fedora-rawhide-s390x"),
        ),
        cpb(
            "s390x Fedora Rawhide LTO",
            LTONonDebugUnixBuild,
            UNSTABLE,
            TIER_3,
            w("cstratak-fedora-rawhide-s390x"),
        ),
        cpb(
            "s390x Fedora Rawhide LTO + PGO",
            LTOPGONonDebugBuild,
            UNSTABLE,
            TIER_3,
            w("cstratak-fedora-rawhide-s390x"),
        ),

        # FreBSD x86-64 clang
        # FreeBSD 15 is CURRENT: development branch (at 2023-10-17)
        cpb(
            "AMD64 FreeBSD15",
            UnixBuild,
            UNSTABLE,
            TIER_3,
            w("opsec-fbsd15"),
        ),
        # FreeBSD 16 is CURRENT: development branch (at 2026-01-09)
        cpb(
            "AMD64 FreeBSD16",
            UnixBuild,
            UNSTABLE,
            TIER_3,
            w("opsec-fbsd16"),
        ),

        # Emscripten
        cpb(
            "WASM Emscripten",
            EmscriptenBuild,
            UNSTABLE,
            TIER_3,
            w("rkm-emscripten"),
        ),

        # -- Unstable No Tier builders --------------------------------------
        # Linux x86-64 GCC musl Freethreading
        cpb(
            "AMD64 Alpine Linux NoGIL",
            UnixNoGilBuild,
            UNSTABLE,
            NO_TIER,
            w("ware-alpine"),
        ),
        # Linux GCC Fedora Rawhide Freethreading builders
        cpb(
            "AMD64 Fedora Rawhide NoGIL",
            FedoraRawhideFreedthreadingBuild,
            UNSTABLE,
            NO_TIER,
            w("cstratak-fedora-rawhide-x86_64"),
        ),
        cpb(
            "aarch64 Fedora Rawhide NoGIL",
            FedoraRawhideFreedthreadingBuild,
            UNSTABLE,
            NO_TIER,
            w("cstratak-fedora-rawhide-aarch64"),
        ),
        cpb(
            "PPC64LE Fedora Rawhide NoGIL",
            FedoraRawhideFreedthreadingBuild,
            UNSTABLE,
            NO_TIER,
            w("cstratak-fedora-rawhide-ppc64le"),
        ),
        cpb(
            "s390x Fedora Rawhide NoGIL",
            FedoraRawhideFreedthreadingBuild,
            UNSTABLE,
            NO_TIER,
            w("cstratak-fedora-rawhide-s390x"),
        ),
        # Linux GCC Fedora Rawhide Freethreading refleak builders
        cpb(
            "AMD64 Fedora Rawhide NoGIL refleaks",
            UnixNoGilRefleakBuild,
            UNSTABLE,
            NO_TIER,
            w("cstratak-fedora-rawhide-x86_64"),
        ),
        cpb(
            "aarch64 Fedora Rawhide NoGIL refleaks",
            UnixNoGilRefleakBuild,
            UNSTABLE,
            NO_TIER,
            w("cstratak-fedora-rawhide-aarch64"),
        ),
        cpb(
            "PPC64LE Fedora Rawhide NoGIL refleaks",
            UnixNoGilRefleakBuild,
            UNSTABLE,
            NO_TIER,
            w("cstratak-fedora-rawhide-ppc64le"),
        ),
        cpb(
            "s390x Fedora Rawhide NoGIL refleaks",
            UnixNoGilRefleakBuild,
            UNSTABLE,
            NO_TIER,
            w("cstratak-fedora-rawhide-s390x"),
        ),

        # Linux x86-64 NixOS Unstable
        cpb(
            "AMD64 NixOS Unstable",
            UnixBuild,
            UNSTABLE,
            NO_TIER,
            "malvex-nixos-x86_64",
        ),
        cpb(
            "AMD64 NixOS Unstable Refleaks",
            UnixRefleakBuild,
            UNSTABLE,
            NO_TIER,
            "malvex-nixos-x86_64",
        ),
        cpb(
            "AMD64 NixOS Unstable Perf",
            UnixPerfBuild,
            UNSTABLE,
            NO_TIER,
            "malvex-nixos-x86_64",
        ),

        # Solaris sparcv9
        cpb(
            "SPARCv9 Oracle Solaris 11.4",
            UnixBuild,
            UNSTABLE,
            NO_TIER,
            w("kulikjak-solaris-sparcv9"),
        ),

        # riscv64 GCC
        cpb(
            "riscv64 Ubuntu23",
            SlowUnixInstalledBuild,
            UNSTABLE,
            NO_TIER,
            w("onder-riscv64"),
        ),

        # Arch Usan (see stable "AMD64 Arch Linux Usan Function" above)
        cpb(
            "AMD64 Arch Linux Usan",
            ClangUbsanLinuxBuild,
            UNSTABLE,
            NO_TIER,
            w("pablogsal-arch-x86_64"),
        ),
    ]

    return _builders


def get_builder_tier(builder: str) -> str:
    # Strip trailing branch name
    import re
    builder = re.sub(r" 3\.[x\d]+$", "", builder)

    for b in _builders or []:
        if b.name == builder:
            return b.tier or "no tier"

    return "unknown tier"


# Match builder name (excluding the branch name) of builders that should only
# run on the main and PR branches.
ONLY_MAIN_BRANCH = (
    "ARM64 Windows",
    "Windows PGO",
    "AMD64 Arch Linux Perf",
    "AMD64 Arch Linux Valgrind",
)
