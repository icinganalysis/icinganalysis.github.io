def make_inp_file(TINF=268.15, PINF=100000.0, VINF=90.0, DPD=20.0, CHORD=0.941, LWC=0.54, AOA=0.0, TSTOP=60.0, FLWC=1.0,
                  description="", case_inp="case.inp", RH=100.0, TSTART=0, ITIMFL=1, IBOD=1, IFLO=1, DSMN=0.0004,
                  NPL=24, RHOP=1000.0, IGRID=0, IBOE=0, IDEICE=0, IHTC=0, SREF=0, FPRT=2, HPRT=1, BPRT=1, EPRT=1,
                  MPRT=1, TPRT=0, IDBF=0, KWARN=0, ice_density=917, sweep=0, flap=None, comment=None, case='', SLD=0,
                  ICP=0, IBETA=0, IQEX=0, IBOOT=0, GRAV=9.8):
    """
    Make a LEWICE input file (version 3.2.2)

    Default values are the defaults from the LEWICE manual.

    The LEWICE manual is available at https://ntrs.nasa.gov/citations/20080048307 (version 3.2.2)

    :param TINF: Ambient static temperature, K
    :param p: Ambient static pressure, Pa
    :param VINF: airspeed, m/s
    :param DPD: drop diameters, micrometer
    :param CHORD: airfoil chord length, m
    :param LWC: liquid water content, g/m^3
    :param AOA: angle of attack, degree
    :param TSTOP: time in icing, s
    :param FLWC: fraction liquid water content for each drop bin
    :param description: A description of the case (one line)
    :param case_inp: name for the input file (default: "case.inp")
    :param RH: Relative humidity, percent
    :param ITIMFL:
    :param IBOD:
    :param IFLO:
    :param DSMN:
    :param NPL:
    :param RHOP:
    :param IGRID:
    :param IBOE:
    :param IDEICE:
    :param SREF:
    :param FPRT:
    :param HPRT:
    :param BPRT:
    :param EPRT:
    :param MPRT:
    :param TPRT:
    :param IDBF:
    :param KWARN:
    :return:
    """
    flwc_text = make_flwc_text(FLWC)
    dpd_text = make_flwc_text(DPD)
    # fmt: off
    template = f"""{description}  
&LEW20
ITIMFL =  {ITIMFL:.0f}
TSTART =  {TSTART:.1f}
TSTOP  =  {TSTOP:.1f}
IBOD   =  {IBOD:.0f}
IFLO   =  {IFLO:.0f}
DSMN   =  {DSMN:f}
NPL    =  {NPL:.0f}
RHOP   =  {RHOP:f}
IGRID  =  {IGRID:.0f}
IBOE   =  {IBOE:.0f}
IDEICE =  {IDEICE:.0f}
IHTC   =  {IHTC:.0f}
&END
&DIST
FLWC   =  {flwc_text}
DPD    =  {dpd_text}
&END
&ICE1
CHORD  =  {CHORD:.4f}
AOA    =  {AOA:.3f}
VINF   =  {VINF:.2f}
LWC    =  {LWC:.3f}
TINF   =  {TINF:.3f}
PINF   =  {PINF:.1f}
RH     =  {RH:.1f}
SREF   =  {SREF}
&END
&LPRNT
FPRT   =  {FPRT:.0f}
HPRT   =  {HPRT:.0f}
BPRT   =  {BPRT:.0f}
EPRT   =  {EPRT:.0f}
MPRT   =  {MPRT:.0f}
TPRT   =  {TPRT:.0f}
IDBF   =  {IDBF:.0f}
KWARN  =  {KWARN:.0f}
&END
&RDATA
&END
&BOOT
&END
"""
    # fmt: on
    pre_lines = []
    if comment is not None:
        pre_lines.append(f"comment = {comment}")
    pre_lines.append('# LEWICE ignores input outside of an "&" block')
    pre_lines.append('# Values that affected the inputs can be documented here')
    pre_lines.append(f'ice_density = {ice_density: .0f}')
    pre_lines.append(f'sweep  = {sweep: .1f}')
    pre_lines.append(f'case  = {case}')
    if flap is not None:
        pre_lines.append(f"flap   =  {flap:.1f}")
    pre_lines = '\n'.join(pre_lines)
    with open(case_inp, "w") as fd:
        fd.writelines(pre_lines)
        fd.writelines(template)
    return case_inp
