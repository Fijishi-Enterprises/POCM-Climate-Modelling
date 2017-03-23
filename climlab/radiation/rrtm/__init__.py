''' climlab wrapper for RRTMG radiation schemes.

This is implemented with classes :class:`~climlab.radiation.rrtm.RRTMG_LW`, and
:class:`~climlab.radiation.rrtm.RRTMG_SW`,
as well as a container class :class:`~climlab.radiation.rrtm.RRTMG`
that has LW and SW radiation as subprocesses.

See <http://rtweb.aer.com/rrtm_frame.html> for more information about the RRTMG code.

    :Example:

        Here is a quick example of setting up a single-column
        Radiative-Convective model with fixed relative humidity::

            import climlab
            alb = 0.25
            #  State variables (Air and surface temperature)
            state = climlab.column_state(num_lev=30)
            #  Parent model process
            rcm = climlab.TimeDependentProcess(state=state)
            #  Fixed relative humidity
            h2o = climlab.radiation.ManabeWaterVapor(state=state)
            #  Couple water vapor to radiation
            rad = climlab.radiation.RRTMG(state=state, specific_humidity=h2o.q, albedo=alb)
            #  Convective adjustment
            conv = climlab.convection.ConvectiveAdjustment(state=state, adj_lapse_rate=6.5)
            #  Couple everything together
            rcm.add_subprocess('Radiation', rad)
            rcm.add_subprocess('WaterVapor', h2o)
            rcm.add_subprocess('Convection', conv)
            #  Run the model
            rcm.integrate_years(1)
            #  Check for energy balance
            print rcm.ASR - rcm.OLR

'''
from __future__ import division
#  Wrapping these imports in try/except to avoid failures during documentation building on readthedocs
try:
    #import _rrtmg_lw, _rrtmg_sw
    import _rrtmg_sw
    #  Get number of bands from fortran modules
    nbndsw = int(_rrtmg_sw.parrrsw.nbndsw)
    naerec = int(_rrtmg_sw.parrrsw.naerec)
    #nbndlw = int(_rrtmg_lw.parrrtm.nbndlw)
except:
    nbndsw = 1
    naerec = 1
    nbndlw = 1
    print 'Cannot import compiled RRTMG Fortran extensions, this module will not be functional.'
#  Get nbndlw from the new f90wrap module
#from _rrtmg_lw.parrrtm.parrrtm import nbndlw
#import _rrtmg_lw.parrrtm
#nbndlw = _rrtmg_lw.parrrtm.parrrtm.nbndlw
import _rrtmg_lw.rrtmg_lw
nbndlw = _rrtmg_lw.rrtmg_lw.parrrtm.nbndlw
from rrtmg import RRTMG
from rrtmg_lw import RRTMG_LW
from rrtmg_sw import RRTMG_SW
from utils import _climlab_to_rrtm, _rrtm_to_climlab
