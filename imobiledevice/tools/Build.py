from Download import download_and_extract
import os, platform, subprocess

cur_dir = os.path.dirname(__file__)
root_dir = os.path.dirname(cur_dir)

build_dir = os.path.join(root_dir, 'build', platform.system().lower())
ssl_down_dir = os.path.join(build_dir, 'openssl')
download_and_extract('https://ci.appveyor.com/api/projects/tomicyo/openssl-ci/artifacts/artifacts/openssl_windows_md_shared.zip', ssl_down_dir)

lib_posix_mapping = {
    'debug': 'win64_vc150d',
    'release': 'win64_vc150r'
} 

config_mapping = {
    'debug': 'Debug',
    'release': 'Release'
}

def build_x64(config, src, artifact_dir):
    bld = os.path.join(src, 'build', 'win64', config)
    ins = os.path.join(src, 'artifacts', 'win64_' + config)
    
    P = subprocess.Popen(['cmake', 
        '-GVisual Studio 15 2017 Win64',
        '-H{0}'.format(src),
        '-B{0}'.format(bld),
        '-DCMAKE_BUILD_TYPE={0}'.format(config_mapping[config]),
        '-DCMAKE_INSTALL_PREFIX={0}'.format(ins)
        ])
    P.wait()

    B = subprocess.Popen(['cmake',
        '--build', bld,
        '--config', config_mapping[config],
        '--target', 'install'
        ])
    B.wait()

build_x64('release', root_dir, build_dir)