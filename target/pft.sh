# Please update this with the full path of your pflotran installation:
PFT_PATH="/app/pflotran_ogs_1.8"
PETSC_DIR="/app/petsc"
PETSC_ARCH="ubuntu-opt"
# For example:
# PFT_PATH="/home/myusername/pflotran"

# Please ensure the following variables are defined:
# PETSC_DIR
# PETSC_ARCH
# see "Installing and Running on Ubuntu" page for more information
#
# Don't forget to make this executable with chmod +x pft.sh

# ********************************************************************

# Check if mpiexec is available
MPIEXEC="$PETSC_DIR/$PETSC_ARCH/bin/mpiexec"

if [ ! -x "$MPIEXEC" ]; then
  echo "Error: $MPIEXEC does not exist or is not executable."
  exit 1
fi

# Run the simulation
"$MPIEXEC" -n "$2" "$PFT_PATH/src/pflotran/pflotran" -pflotranin "$1"
# mpirun -n "$2" "$PFT_PATH/src/pflotran/pflotran" -pflotranin "$1"
# "$PFT_PATH/src/pflotran/pflotran" -pflotranin "$1"