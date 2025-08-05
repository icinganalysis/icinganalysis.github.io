import os


def count_problems(d=os.getcwd()):

    print(d)

    f = os.path.join(d, 'junk.dat')

    with open(f, 'r') as fd:
        lines = fd.readlines()
    problem_count = 0
    shed_count = 0
    phase_count = 0
    dm = 0
    dim = 0
    for line in lines:
        if 'program is having problems with this case.' in line:
            problem_count += 1
        if 'ice has shed' in line:
            shed_count += 1
        if 'phase change algorithm did not converge' in line:
            phase_count += 1
        if "mass of water/unit span coming in" in line.lower():
            vs =[_ for _ in line.split(' ') if _]
            dm += float(vs[-2])
        if 'mass of ice/unit span freezing this time step =' in line.lower():
            vs =[_ for _ in line.split(' ') if _]
            dim += float(vs[-2])

    return problem_count, shed_count, phase_count, dm, dim


if __name__ == '__main__':

    # problems_count = count_problems('/home/theepdinker/PycharmProjects/icinganalysis.github.io/icinganalysis/lewice/USAx_030_IDEICE2')

    problems_count = count_problems('/home/theepdinker/PycharmProjects/icinganalysis.github.io/icinganalysis/lewice/NACA0018_IDEICE0')
    print(problems_count)
