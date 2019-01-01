from tools.msvc import enable_vs2017_env
from tools.android import build_android_instance
from tools.common import zipdir
from tools.cmake import gen_cmake_package
import os, subprocess, sys, platform, zipfile

curdir = os.path.abspath(os.path.dirname(__file__))
print(curdir)

lib_types = ['static', 'shared']
archs = ['x64', 'armv7', 'arm64']
os_name_l = platform.system().lower()

pk_configs = [
    {
        'name': 'zlib',
        'platforms': ['win64'],
        'type': 'shared_lib',
        'win64': 
        {
            'debug':    'zlib.lib',
            'release':  'zlib.lib',
            'debugso':  'zlib.dll',
            'releaseso':'zlib.dll',
        }
    },
    {
        'name': 'libzip',
        'platforms': ['win64'],
        'type': 'static_lib',
        'win64': 
        {
            'debug':    'libzip.lib',
            'release':  'libzip.lib',
        }
    },
    {
        'name': 'ssl',
        'platforms': ['win64'],
        'type': 'shared_lib',
        'win64': 
        {
            'debug':    'libssl.lib',
            'release':  'libssl.lib',
            'debugso':  'libssl-1_1-x64.dll',
            'releaseso':'libssl-1_1-x64.dll',
        }
    },
    {
        'name': 'crypto',
        'platforms': ['win64'],
        'type': 'shared_lib',
        'win64': 
        {
            'debug':    'libcrypto.lib',
            'release':  'libcrypto.lib',
            'debugso':  'libcrypto-1_1-x64.dll',
            'releaseso':'libcrypto-1_1-x64.dll',
        }
    },
    {
        'name': 'pcre2',
        'platforms': ['win64'],
        'type': 'static_lib',
        'win64': 
        {
            'debug':    'pcre2-8.lib',
            'release':  'pcre2-8.lib'
        }
    },
    {
        'name': 'c-ares',
        'platforms': ['win64'],
        'type': 'static_lib',
        'win64': 
        {
            'debug':    'cares.lib',
            'release':  'cares.lib',
        }
    },
    {
        'name': 'imobiledevice',
        'platforms': ['win64'],
        'type': 'shared_lib',
        'win64': 
        {
            'debug':    'libimobiledevice.lib',
            'release':  'libimobiledevice.lib',
            'debugso':  'libimobiledevice.dll',
            'releaseso':'libimobiledevice.dll',
        }
    },
]

# lib_type could be 'static' or 'shared'
def build_install_dir(lib_type = 'shared'):
    return os.path.join(curdir, 'build', os_name_l, lib_type)

def build_zlib_vs2017(lib_type = 'shared'):
    build_dir = os.path.join(curdir, 'build', 'cmake', 'z_' + lib_type)
    install_dir = build_install_dir(lib_type)
    cmake_process = subprocess.Popen([
        'cmake',
        '-GVisual Studio 15 2017 Win64',
        '-H{0}'.format(os.path.join(curdir, 'zlib-1.2.11')),
        '-B{0}'.format(build_dir),
        '-DCMAKE_INSTALL_PREFIX={0}'.format(install_dir)
    ],shell=True)
    cmake_process.wait()
    cmake_process = subprocess.Popen([
        'cmake',
        '--build',
        build_dir,
        '--config',
        'RelWithDebInfo',
        '--target',
        'install'
    ],shell=True)
    cmake_process.wait()

def build_openssl_windows_vs2017(lib_type = 'shared'):
    enable_vs2017_env('x64')
    build_dir = os.path.join(curdir, 'build/openssl_build.dir', lib_type)
    if not os.path.exists(build_dir):
        os.makedirs(build_dir)
    os.chdir(build_dir)
    if not os.path.exists(os.path.join(build_dir,'makefile')):
        install_dir = build_install_dir(lib_type)
        bld_cmd = ['perl', 
            os.path.join(curdir,'openssl-1.1.0/Configure'),
            'VC-WIN64A', 'no-asm', 'zlib',
            '--with-zlib-include={0}'.format(os.path.join(install_dir, 'include')),
            '--with-zlib-lib={0}'.format(os.path.join(install_dir, 'lib', 'zlib.lib')),
            '--prefix={0}'.format(install_dir)]
        if lib_type == 'static':
            bld_cmd.append('no-shared')
        p = subprocess.Popen(bld_cmd, 
            shell=True)
        p.wait()
    p = subprocess.Popen(['nmake', 'build_libs'], 
    shell=True)
    p.wait()
    p = subprocess.Popen(['nmake', 'install_dev'], 
    shell=True)
    p.wait()
    p = subprocess.Popen(['nmake', 'install_runtime'], 
    shell=True)
    p.wait()

def build_openssl_osx64(lib_type = 'shared'):
    build_dir = os.path.join(curdir, 'build/openssl_build.dir', lib_type)
    if not os.path.exists(build_dir):
        os.makedirs(build_dir)
    os.chdir(build_dir)
    if not os.path.exists(os.path.join(build_dir,'Makefile')):
        install_dir = build_install_dir(lib_type)
        bld_cmd = ['perl', 
            os.path.join(curdir,'openssl-1.1.0/Configure'),
            'darwin64-x86_64-cc', 'no-asm',
            '--prefix={0}'.format(install_dir)]
        if lib_type == 'static':
            bld_cmd.append('no-shared')
        p = subprocess.Popen(bld_cmd)
        p.wait()
    p = subprocess.Popen(['make', '-j', '8', 'build_libs'])
    p.wait()
    p = subprocess.Popen(['make', 'install_dev'])
    p.wait()

def build_cmake_vs2017(lib_type = 'shared'):
    build_dir = os.path.join(curdir, 'build', 'cmake', lib_type)
    install_dir = build_install_dir(lib_type)
    openssl_inc = os.path.join(install_dir, 'include').replace('\\', '/')
    openssl_libdir = os.path.join(install_dir, 'lib').replace('\\', '/')
    ssl_lib = os.path.join(openssl_libdir, 'libssl.lib').replace('\\', '/')
    crypto_lib = os.path.join(openssl_libdir, 'libcrypto.lib').replace('\\', '/')
    command = [
        'cmake',
        '-GVisual Studio 15 2017 Win64',
        '-H{0}'.format(curdir.replace('\\', '/')),
        '-B{0}'.format(build_dir.replace('\\', '/')),
        '-DOPENSSL_INCLUDE_DIR={0}'.format(openssl_inc.replace('\\', '/')),
        '-DOPENSSL_SSL_LIBRARY={0}'.format(ssl_lib),
        '-DOPENSSL_CRYPTO_LIBRARY={0}'.format(crypto_lib),
        '-DOPENSSL_LIBRARIES="' +ssl_lib+';'+crypto_lib + '"',
        '-DOPENSSL_ROOT_DIR={0}'.format(install_dir.replace('\\', '/')),
        '-DZLIB_INCLUDE_DIR={0}'.format(openssl_inc),
        '-DZLIB_LIBRARY={0}'.format(os.path.join(openssl_libdir, 'zlib.lib').replace('\\', '/')),
        '-DEVENT__DISABLE_TESTS=1',
        '-DEVENT__DISABLE_REGRESS=1',
        '-DEVENT__DISABLE_SAMPLES=1',
        '-DPCRE2_BUILD_TESTS=0',
        '-DPCRE2_BUILD_PCRE2GREP=0',
        '-DCMAKE_BUILD_TYPE=RelWithDebInfo',
        '-DCMAKE_INSTALL_PREFIX={0}'.format(install_dir.replace('\\', '/'))
    ]
    print command
    cmake_process = subprocess.Popen(command,shell=True)
    cmake_process.wait()
    cmake_process = subprocess.Popen([
        'cmake',
        '--build',
        build_dir,
        '--config',
        'RelWithDebInfo',
        '--target',
        'install'
    ],shell=True)
    cmake_process.wait()

def build_cmake_osx64(lib_type = 'shared'):
    build_dir = os.path.join(curdir, 'build', 'cmake', lib_type)
    install_dir = build_install_dir(lib_type)
    openssl_inc = os.path.join(install_dir, 'include')
    openssl_libdir = os.path.join(install_dir, 'lib')
    cmake_process = subprocess.Popen([
        'cmake',
        '-GXcode',
        '-H{0}'.format(curdir),
        '-B{0}'.format(build_dir),
        '-DOPENSSL_INC={0}'.format(openssl_inc.replace('\\', '/')),
        '-DOPENSSL_LIBDIR={0}'.format(openssl_libdir.replace('\\', '/')),
        '-DEVENT__DISABLE_TESTS=1',
        '-DEVENT__DISABLE_REGRESS=1',
        '-DEVENT__DISABLE_SAMPLES=1',
        '-DPCRE2_BUILD_TESTS=0',
        '-DPCRE2_BUILD_PCRE2GREP=0',
        '-DCMAKE_BUILD_TYPE=RelWithDebInfo',
        '-DCMAKE_INSTALL_PREFIX={0}'.format(install_dir)
    ])
    cmake_process.wait()
    cmake_process = subprocess.Popen([
        'cmake',
        '--build',
        build_dir,
        '--config',
        'RelWithDebInfo',
        '--target',
        'install'
    ])
    cmake_process.wait()

def build_windows(lib_type = 'shared'):
    build_zlib_vs2017(lib_type)
    build_openssl_windows_vs2017(lib_type)
    build_cmake_vs2017(lib_type)
    gen_cmake_package(os.path.join(curdir, 'build', 'windows', lib_type, 'third_party_clibs.cmake'), pk_configs)
    archive_name = os.path.join(curdir, 'build', 'third_party_clibs_windows_{0}.zip'.format(lib_type))
    zipf = zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED)
    zipdir(os.path.join(curdir, 'build', 'windows', lib_type), zipf)
    zipf.close()

def build_osx(lib_type = 'shared'):
    build_openssl_osx64(lib_type)
    archive_name = os.path.join(curdir, 'build', 'third_party_clibs_darwin64_{0}.zip'.format(lib_type))
    zipf = zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED)
    zipdir(os.path.join(curdir, 'build', 'darwin', lib_type), zipf)
    zipf.close()

if os_name_l == 'windows':
    build_windows('shared')
    build_windows('static')
elif os_name_l == 'linux':
    build_android_instance('arm64-v8a', 'gnustl_shared', [])
    pass
elif os_name_l == 'darwin':
    build_osx('static')
    build_osx('shared')
