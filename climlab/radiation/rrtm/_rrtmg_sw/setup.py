from __future__ import print_function
from os.path import join, abspath


def configuration(parent_package='', top_path=None):
    global config
    from numpy.distutils.misc_util import Configuration
    from numpy.distutils.fcompiler import get_default_fcompiler, CompilerNotFound

    build = True
    try:
        # figure out which compiler we're going to use
        compiler = get_default_fcompiler()
        # set some fortran compiler-dependent flags
        f90flags = []
        if compiler == 'gnu95':
            f90flags.append('-fno-range-check')
            f90flags.append('-ffree-form')
            f90flags.append('-fPIC')
        elif compiler == 'intel' or compiler == 'intelem':
            f90flags.append('-132')
        #  Need zero-level optimization to avoid build problems with rrtmg_sw_k_g.f90
        #f90flags.append('-O0')
        #  Suppress all compiler warnings (avoid huge CI log files)
        f90flags.append('-w')
    except CompilerNotFound:
        print('No Fortran compiler found, not building the RRTMG_SW radiation module!')
        build = False

    config = Configuration(package_name='_rrtmg_sw', parent_name=parent_package, top_path=top_path)
    modules = ['parkind.f90',
                'parrrsw.f90',
                'rrsw_aer.f90',
                'rrsw_cld.f90',
                'rrsw_con.f90',
                'rrsw_kg16.f90',
                'rrsw_kg17.f90',
                'rrsw_kg18.f90',
                'rrsw_kg19.f90',
                'rrsw_kg20.f90',
                'rrsw_kg21.f90',
                'rrsw_kg22.f90',
                'rrsw_kg23.f90',
                'rrsw_kg24.f90',
                'rrsw_kg25.f90',
                'rrsw_kg26.f90',
                'rrsw_kg27.f90',
                'rrsw_kg28.f90',
                'rrsw_kg29.f90',
                'rrsw_ncpar.f90',
                'rrsw_ref.f90',
                'rrsw_tbl.f90',
                'rrsw_vsn.f90',
                'rrsw_wvn.f90',]
    src = ['rrtmg_sw_k_g.f90',
           'mcica_random_numbers.f90',
           'mcica_subcol_gen_sw.f90',
           'rrtmg_sw_vrtqdr.f90',
           'rrtmg_sw_reftra.f90',
           'rrtmg_sw_taumol.f90',
           'rrtmg_sw_spcvmc.f90',
           'rrtmg_sw_setcoef.f90',
           'rrtmg_sw_init.f90',
           'rrtmg_sw_cldprmc.f90',
           'rrtmg_sw_rad.f90',]
    unoptimized_src = ['rrtmg_sw_k_g.f90']
    mod_src = ['rrtmg_sw_rad.f90',]
    if build:
        import subprocess
        thispath = config.local_path
        object_file_list = []
        #  Compile all source to object .o files
        gfortran_call = ['gfortran', '-c', ] + f90flags
        try:
            for item in modules:
                optflag = '-O3'
                output_file = item[:-3]+'o'
                object_file_list.append(output_file)
                fullname = join(thispath,'rrtmg_sw_v4.0','gcm_model','modules',item)
                subprocess.call(gfortran_call + [fullname] + [optflag] + ['-o'] + [output_file])
            for item in src:
                if item in mod_src:
                    fullname = join(thispath,'sourcemods',item)
                else:
                    fullname = join(thispath,'rrtmg_sw_v4.0','gcm_model','src',item)
                if item in unoptimized_src:
                    optflag = '-O0'
                else:
                    optflag = '-O3'
                output_file = item[:-3]+'o'
                object_file_list.append(output_file)
                subprocess.call(gfortran_call + [fullname] + [optflag] + ['-o'] + [output_file])
        except:
            print('There was a problem with compiling rrtmg_lw objects.')
        sourcelist = [join(thispath,'_rrtmg_sw.pyf'),
                      join(thispath,'Driver.f90')]
        link_args_list = object_file_list #+ [ldflags]
        config.add_extension(name='_rrtmg_sw',
                             sources=[sourcelist],
                             extra_f90_compile_args=f90flags + ['-O3'],
                            f2py_options=['--quiet'],
                            extra_link_args=link_args_list,
                            )
    return config

if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(configuration=configuration)
