"""
Generate benchmarking data for the Beam problem.
"""
from __future__ import print_function

import numpy as np

from om_bench.bench import Bench

from openmdao.api import ScipyOptimizeDriver, pyOptSparseDriver
from openmdao.test_suite.test_examples.beam_optimization.multipoint_beam_group import MultipointBeamGroup


class BeamBench(Bench):

    def setup(self, problem, ndv, nstate, nproc, flag):
        E = 1.
        L = 1.
        b = 0.1
        volume = 0.01
        num_elements = 50 * nstate
        num_cp = ndv
        num_load_cases = 32

        problem.model = MultipointBeamGroup(E=E, L=L, b=b, volume=volume, num_elements=num_elements,
                                            num_cp=num_cp, num_load_cases=num_load_cases)

        problem.driver = pyOptSparseDriver()
        problem.driver.options['optimizer'] = 'SNOPT'
        #problem.driver.options['tol'] = 1e-9
        #problem.driver.options['disp'] = True

    def post_run(problem):
        # Check stuff here.
        pass


if __name__ == "__main__":

    desvars = [1, 2, 4, 8, 16, 32]
    desvars = [item * 40 for item in desvars]
    states = [1]
    procs = [1]

    bench = BeamBench(desvars, states, procs, name='beam')
    bench.num_averages = 5
    bench.walltime = 1
    bench.time_nonlinear = False
    bench.time_linear = False
    bench.time_driver = True
    bench.single_batch = True

    bench.run_benchmark()


