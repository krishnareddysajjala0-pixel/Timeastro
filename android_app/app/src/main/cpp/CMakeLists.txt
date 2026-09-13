cmake_minimum_required(VERSION 3.22.1)

project("swisseph")

add_compile_options(-Wno-error=format-security -Wno-format-security)

set(SWE_SOURCES
    libswe/swecl.c
    libswe/swedate.c
    libswe/swehouse.c
    libswe/swemini.c
    libswe/swemmoon.c
    libswe/swemplan.c
    libswe/sweph.c
    libswe/swephlib.c
    libswe/swehel.c
    libswe/swejpl.c
)

add_library(swisseph SHARED ${SWE_SOURCES})

# Enable 16 KB ELF alignment for Android 15+ / modern ARM & x86_64 devices
target_link_options(swisseph PRIVATE "-Wl,-z,max-page-size=16384")

target_include_directories(swisseph PUBLIC libswe)
