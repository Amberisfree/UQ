import umbridge
import subprocess
import os
import logging
import pandas as pd
import numpy as np

# Set up logging
logging.basicConfig(level=logging.INFO)

class PFLOTRANModel(umbridge.Model):
    def __init__(self):
        super().__init__("pflotran_simulation")
        self.input_file_path = "/app/target/ccs_3df.grdecl"
        self.simulation_script = "/app/target/pft.sh"
        self.simulation_input = "/app/target/Coarse_CCS_3DF.in"
        self.output_file_path = "/app/target/Coarse_CCS_3DF-mas.dat"
        self.output_csv_path = "/app/target/Coarse_CCS_3DF.csv"

    def get_input_sizes(self, config):
        return [12]  # 12 parameters for each layer

    def get_output_sizes(self, config):
        return [2]  # 2 output result

    def __call__(self, parameters, config):
        try:
            # Prepare the input file for PFLOTRAN based on parameters
            self.prepare_input_file(parameters[0])
            logging.info("Input file prepared successfully.")

            # Run the PFLOTRAN simulation
            self.run_simulation()
            logging.info("Simulation ran successfully.")

            # Process the output file to extract results
            result = self.process_output_file()
            logging.info("Output processed successfully.")

            return result
        except Exception as e:
            logging.error(f"Error during simulation: {e}")
            raise

    def process_output_file(self):
        # Converts a -mas.dat into a .csv file
        replacements = {' "':",",'"':'','  ':',',' -':',-'}

        infile = self.output_file_path
        outfile= self.output_csv_path

        with open(infile) as infile, open(outfile, 'w') as outfile:
            for line in infile:
                for src, target in replacements.items():
                    line = line.replace(src, target)
                outfile.write(line[1:])

        # Extract feature from .csv file
        df=pd.read_csv(self.output_csv_path)
        result_a=float(df["Field fgit [m^3]"].iloc[-1])
        result_c=float(df["rgip_NOG [m^3] 1"].iloc[-1])

        result=[[result_a, result_c]]
        return result


    def run_simulation(self):
        #handle the input error, check its accuracy on commandline
        print(os.system( "cat" +" "+ self.simulation_input))
        try:
            #result = subprocess.run([self.simulation_script, self.simulation_input, 4], capture_output=True, text=True)
            #result=os.system(self.simulation_script + " "+  self.simulation_input + " "+ "4")
            #os.system(self.simulation_script + " "+  self.simulation_input + " "+ "2")
            os.system(self.simulation_script + " "+  self.simulation_input )

            # if result != 0:
            #     print(result)
            #     logging.error(f"Simulation script failed: {result.stderr}")
            #     raise RuntimeError("Simulation script failed.")
            # logging.info("Simulation script output: " + result.stdout)
        except Exception as e:
            logging.error(f"Error running simulation: {e}")
            raise

    def prepare_input_file(self, porosities):
        try:
            input_data = f"""
            DIMENS
            30 30 12 /

            external_file ccs_3df_geom.grdecl

            -- Control zone
            EQUALS
            FIPNOGO 5 1 7 1 7 2* /
            /

            -- Set Porosities per layer
            EQUALS
            """
            for i, porosity in enumerate(porosities, start=1):
                input_data += f"    PORO    {porosity:.2f}    4*    {i}    {i}    /\n"

            input_data += """
            /

            -- Set Permeability values per layer
            EQUALS
            """
            for i, porosity in enumerate(porosities, start=1):
                permeability = 10 ** (15.6 * porosity - 0.9)
                input_data += f"    PERMX    {permeability:.2f}    4*    {i}    {i}    /\n"

            input_data += """
            /

          -- Copy values to other perm directions
            COPY
            PERMX PERMY /
            PERMX PERMZ /
            /

            -- Apply KvKh correction
            MULTIPLY
            PERMZ 0.1 /  -- <== PARAMETER TO TUNE
            /

            FAULTS
            FAULTA              1       1       22      22      1       12      Y-      /
            FAULTA      2       2       21      21      1       12      Y-      /
            FAULTA      3       3       20      20      1       12      Y-      /
            FAULTA      4       4       19      19      1       12      Y-      /
            FAULTA      5       5       18      18      1       12      Y-      /
            FAULTA      6       6       17      17      1       12      Y-      /
            FAULTA      7       7       16      16      1       12      Y-      /
            FAULTA      8       8       15      15      1       12      Y-      /
            FAULTA      9       9       14      14      1       12      Y-      /
            FAULTA      10      10      13      13      1       12      Y-      /
            FAULTA      11      11      12      12      1       12      Y-      /
            FAULTA      12      12      11      11      1       12      Y-      /
            FAULTA      13      13      10      10      1       12      Y-      /
            FAULTA      14      14      9       9       1       12      Y-      /
            FAULTA      15      15      8       8       1       12      Y-      /
            FAULTA      16      16      7       7       1       12      Y-      /
            FAULTA      17      17      6       6       1       12      Y-      /
            FAULTA      18      18      5       5       1       12      Y-      /
            FAULTA      19      19      4       4       1       12      Y-      /
            FAULTA      20      20      3       3       1       12      Y-      /
            FAULTA      21      21      2       2       1       12      Y-      /
            FAULTA      22      22      1       1       1       12      Y-      /

            FAULTA      1       1       22      22      1       12      X-      /
            FAULTA      2       2       21      21      1       12      X-      /
            FAULTA      3       3       20      20      1       12      X-      /
            FAULTA      4       4       19      19      1       12      X-      /
            FAULTA      5       5       18      18      1       12      X-      /
            FAULTA      6       6       17      17      1       12      X-      /
            FAULTA      7       7       16      16      1       12      X-      /
            FAULTA      8       8       15      15      1       12      X-      /
            FAULTA      9       9       14      14      1       12      X-      /
            FAULTA      10      10      13      13      1       12      X-      /
            FAULTA      11      11      12      12      1       12      X-      /
            FAULTA      12      12      11      11      1       12      X-      /
            FAULTA      13      13      10      10      1       12      X-      /
            FAULTA      14      14      9       9       1       12      X-      /
            FAULTA      15      15      8       8       1       12      X-      /
            FAULTA      16      16      7       7       1       12      X-      /
            FAULTA      17      17      6       6       1       12      X-      /
            FAULTA      18      18      5       5       1       12      X-      /
            FAULTA      19      19      4       4       1       12      X-      /
            FAULTA      20      20      3       3       1       12      X-      /
            FAULTA      21      21      2       2       1       12      X-      /
            FAULTA      22      22      1       1       1       12      X-      /


            FAULTB      17      17      2       2       1       12      X-      /
            FAULTB      18      18      4       4       1       12      X-      /
            FAULTB      19      19      6       6       1       12      X-      /
            FAULTB      20      20      8       8       1       12      X-      /
            FAULTB      21      21      10      10      1       12      X-      /
            FAULTB      22      22      12      12      1       12      X-      /
            FAULTB      23      23      14      14      1       12      X-      /
            FAULTB      24      24      16      16      1       12      X-      /
            FAULTB      25      25      18      18      1       12      X-      /
            FAULTB      26      26      20      20      1       12      X-      /
            FAULTB      27      27      22      22      1       12      X-      /
            FAULTB      28      28      24      24      1       12      X-      /
            FAULTB      29      29      26      26      1       12      X-      /
            FAULTB      30      30      28      28      1       12      X-      /



            FAULTB      16      16      1       1       1       12      Y       /
            FAULTB      17      17      3       3       1       12      Y       /
            FAULTB      18      18      5       5       1       12      Y       /
            FAULTB      19      19      7       7       1       12      Y       /
            FAULTB      20      20      9       9       1       12      Y       /
            FAULTB      21      21      11      11      1       12      Y       /
            FAULTB      22      22      13      13      1       12      Y       /
            FAULTB      23      23      15      15      1       12      Y       /
            FAULTB      24      24      17      17      1       12      Y       /
            FAULTB      25      25      19      19      1       12      Y       /
            FAULTB      26      26      21      21      1       12      Y       /
            FAULTB      27      27      23      23      1       12      Y       /
            FAULTB      28      28      25      25      1       12      Y       /
            FAULTB      29      29      27      27      1       12      Y       /
            FAULTB      30      30      29      29      1       12      Y       /

            FAULTB      16      16      1       1       1       12      X-      /
            FAULTB      17      17      3       3       1       12      X-      /
            FAULTB      18      18      5       5       1       12      X-      /
            FAULTB      19      19      7       7       1       12      X-      /
            FAULTB      20      20      9       9       1       12      X-      /
            FAULTB      21      21      11      11      1       12      X-      /
            FAULTB      22      22      13      13      1       12      X-      /
            FAULTB      23      23      15      15      1       12      X-      /
            FAULTB      24      24      17      17      1       12      X-      /
            FAULTB      25      25      19      19      1       12      X-      /
            FAULTB      26      26      21      21      1       12      X-      /
            FAULTB      27      27      23      23      1       12      X-      /
            FAULTB      28      28      25      25      1       12      X-      /
            FAULTB      29      29      27      27      1       12      X-      /
            FAULTB      30      30      29      29      1       12      X-      /

            /

            -- Control the transmissibility of the faults
            MULTFLT
            FAULTA 1.0 / -- Upper fault -- <== PARAMETER TO TUNE
            FAULTB 1.0 / -- Lower fault -- <== PARAMETER TO TUNE
            /

            -- Dykstra-Parsons coefficient to add some heterogeneity
            dpcf
            0.02  42 /


            """

            with open(self.input_file_path, "w") as f:
                f.write(input_data)
            logging.info("Input file written successfully.")
        except Exception as e:
            logging.error(f"Error preparing input file: {e}")
            raise

    def supports_evaluate(self):
        return True


# Instantiate the model
pflotran_model = PFLOTRANModel()


port = int(os.getenv("PORT"))
# Serve the model using UM-Bridge
umbridge.serve_models([pflotran_model], port)