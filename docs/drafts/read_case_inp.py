

def read_case_dot_inp(file):
    """
    Parse a LEWICE input file

    The return dict contains all values defined the manual (version 3.2.2).
    If a name is found in the input file, the default values is over-written with the value found.

    In addition, a description value is included (first line in the file if not blank)

    :param file: input file name (such as "case1.inp")
    :return: dict of values found
            d = {  # default values from manual
            "ITIMFL": 1,
            "TSTART": 0,
            "TSTOP": 60,
            "IBOD": 1,
            "IFLO": 1,
            "DSMN": 4e-4,
            "NPL": 24,
            "RHOP": 1000,
            "SLD": 0,
            "IGRID": 0,
            "IDEICE": 0,
            "ICP": 0,
            "IBETA": 0,
            "IHTC": 0,
            "IQEX": 0,
            "IBOOT": 0,
            "FLWC": [1.],
            "DPD": [20.],
            "CHORD": 0.9144,
            "AOA": 0,
            "VINF": 90,
            "LWC": 0.54,
            "TINF": 268.15,
            "PINF": 100000,
            "RH": 100.,
            "GRAV": 9.8,
            "SREF": 0,
            "FPRT": 1,
            "HPRT": 1,
            "BPRT": 1,
            "EPRT": 0,
            "MPRT": 0,
            "TPRT": 0,
            "IDBF": 0,
            "KWARN: 0"
            "description": '',
            }

    """
    d = {  # default values from manual
        "ITIMFL": 1,
        "TSTART": 0,
        "TSTOP": 60,
        "IBOD": 1,
        "IFLO": 1,
        "DSMN": 4e-4,
        "NPL": 24,
        "RHOP": 1000,
        "SLD": 0,
        "IGRID": 0,
        "IDEICE": 0,
        "ICP": 0,
        "IBETA": 0,
        "IHTC": 0,
        "IQEX": 0,
        "IBOOT": 0,
        "FLWC": [1.0],
        "DPD": [20.0],
        "CHORD": 0.9144,
        "AOA": 0,
        "VINF": 90,
        "LWC": 0.54,
        "TINF": 268.15,
        "PINF": 100000,
        "RH": 100.0,
        "GRAV": 9.8,
        "SREF": 0,
        "FPRT": 1,
        "HPRT": 1,
        "BPRT": 1,
        "EPRT": 0,
        "MPRT": 0,
        "TPRT": 0,
        "IDBF": 0,
        "KWARN": 0,
        "description": "",
    }
    with open(file, "r") as fd:
        lines = fd.readlines()
        for i, line in enumerate(lines):
            row_values = [
                _.strip(',') for _ in line.strip().split(" ") if _ not in ("", "=")
            ]  # values separated by a variable number of spaces
            if row_values:  # ignore blank lines
                if i == 0 and (
                    len(row_values) == 1 or (not is_floatable(row_values[1]))
                ):
                    d["description"] = line.strip()
                    continue
                for name in (  # LEW20 namelist
                    "ITIMFL",
                    "TSTOP",
                    "IBOD",
                    "IFLO",
                    "DSMN",
                    "NPL",
                    "RHOP",
                    "SLD",
                    "IGRID",
                    "IBOE",
                    "IDEICE",
                    "ICP",
                    "IBETA",
                    "IHTC",
                    "IQEX",
                    "IBOOT",
                ):
                    if name in row_values[0]:
                        if name[0] in "IN":
                            d[name] = int(float(row_values[1]))
                        else:
                            d[name] = float(row_values[1])
                for name in (  # DIST namelist
                    "FLWC",
                    "DPD",
                ):
                    if name in row_values[0]:
                        d[name] = [float(_) for _ in row_values[1].split(",") if _ != '']
                for name in (  # ICE1 namelist
                    "CHORD",
                    "AOA",
                    "VINF",
                    "LWC",
                    "TINF",
                    "PINF",
                    "RH",
                    "GRAV",
                    "SREF",
                ):
                    if name in row_values[0]:
                        if name in ("SREF",):
                            d[name] = int(float(row_values[1]))
                        else:
                            d[name] = float(row_values[1])
                for name in (  # LPRINT namelist
                    "FPRT",
                    "HPRT",
                    "BPRT",
                    "EPRT",
                    "MPRT",
                    "TPRT",
                    "IDBF",
                    "KWARN",
                ):
                    if len(row_values) > 1:
                        print(row_values)
                        d[name] = int(float(row_values[1]))
        return d
