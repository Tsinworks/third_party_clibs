
def gen_static_lib_target(name, lib_path_prefix, conf):
    cmake_src = '''
add_library({&target} STATIC IMPORTED)
set_property(TARGET {&target} APPEND PROPERTY IMPORTED_CONFIGURATIONS DEBUG)
set_property(TARGET {&target} APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties({&target} PROPERTIES 
    IMPORTED_LOCATION_DEBUG "${install_prefix}/lib/{&target_debug_lib}"
    IMPORTED_LOCATION_RELEASE "${install_prefix}/lib/{&target_release_lib}"
#    IMPORTED_LINK_INTERFACE_LANGUAGES_DEBUG "CXX"
    INTERFACE_INCLUDE_DIRECTORIES "${install_prefix}/include")
    '''.replace('{&target}', name).replace('{&target_debug_lib}', conf['debug']).replace('{&target_release_lib}', conf['release'])
    return cmake_src

def gen_shared_lib_target(name, lib_path_prefix, conf):
    return '''
add_library({&target} SHARED IMPORTED)
set_property(TARGET {&target} APPEND PROPERTY IMPORTED_CONFIGURATIONS DEBUG)
set_property(TARGET {&target} APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties({&target} PROPERTIES 
    IMPORTED_LOCATION_DEBUG "${install_prefix}/bin/{&target_debug_so}"
    IMPORTED_IMPLIB_DEBUG "${install_prefix}/lib/{&target_debug_lib}"
    IMPORTED_LOCATION_RELEASE "${install_prefix}/bin/{&target_release_so}"
    IMPORTED_IMPLIB_RELEASE "${install_prefix}/lib/{&target_release_lib}"
    INTERFACE_INCLUDE_DIRECTORIES "${install_prefix}/include"
)
    '''.replace('{&target}', name).replace('{&target_debug_lib}', conf['debug']).replace('{&target_release_lib}', conf['release']) \
        .replace('{&target_debug_so}', conf['debugso']) \
        .replace('{&target_release_so}', conf['releaseso'])

def gen_host_exe_target(name, bin_path_prefix, conf):
    return '''
add_executable({&target} IMPORTED)
    '''.replace('{&target}', name)

target_type_action = {
    'shared_lib': gen_shared_lib_target,
    'static_lib': gen_static_lib_target,
    'program':    gen_host_exe_target,
}


def gen_cmake_package(path, pk_configs):
    cpf = open(path, 'w')
    cpf.write('get_filename_component(install_prefix "${CMAKE_CURRENT_LIST_DIR}" ABSOLUTE)\n')

    for item in pk_configs:
        item_name = item['name']
        item_type = item['type']
        item_conf = item['win64']
        cpf.write(target_type_action[item_type](item_name, 'lib', item_conf))

    cpf.close()