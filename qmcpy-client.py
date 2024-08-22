import argparse
import qmcpy as qp
from qmcpy.integrand.um_bridge_wrapper import UMBridgeWrapper
import numpy as np
import umbridge

# Read URL from command line argument
parser = argparse.ArgumentParser(description='QMCPy with UM-Bridge model demo.')
parser.add_argument('url', metavar='url', type=str,
                    help='the URL at which the model is running, for example http://localhost:4242')
args = parser.parse_args()
print(f"Connecting to host URL {args.url}")

# Set up umbridge model and model config
model = umbridge.HTTPModel(args.url, "pflotran_simulation")
config = {}
print(f"Model is set up {model}.")

# Get input dimension from model
d = model.get_input_sizes(config)[0]
print(f"Model input size is {d}.")

# Choose a distribution to sample via QMC
dnb2 = qp.DigitalNetB2(dimension=d)
gauss_sobol = qp.Gaussian(sampler=dnb2, mean=0.20, covariance=0.079)

#throw away any value which is negative

#Use Uniform with range

print(f"Sampling distribution are {dnb2} and {gauss_sobol} .")


integrand = UMBridgeWrapper(gauss_sobol, model, config, parallel=False)
print(f"UMBridgeWrapper is already set up.")

qmc_sobol_algorithm = qp.CubQMCSobolG(integrand, abs_tol=1e-3)
print(f"Cube_QMC_SOBOL algorthim is already set up.")

solution, data = qmc_sobol_algorithm.integrate()

print(solution)
print(data)