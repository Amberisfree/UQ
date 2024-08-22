# Ubuntu Dockerfile
#
# https://github.com/dockerfile/ubuntu


# Pull base image and specify infrastructure's name for HPC
FROM --platform=linux/amd64 ubuntu:22.04


# Set up timezone
ENV TZ=UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update && apt-get install -y tzdata




# Create a user and group
RUN groupadd -g 1000 my_group && useradd -u 1000 -g 1000 -s /bin/bash my_user

# Set the working directory
WORKDIR /app

# Copy files to the container and change ownership
COPY --chown=my_user:my_group . /app



# Set environment variables.
#ENV HOME /root/home

ARG DEBIAN_FRONTEND=noninteractive

ENV PETSC_DIR /app/petsc
ENV PETSC_ARCH ubuntu-opt
ENV LANG en_US.UTF-8
ENV USER my_user 



# Install dependencies for Petsc and Pflotran
RUN \
  apt-get update && \
  apt-get install -y build-essential gfortran && \
  apt-get install -y software-properties-common && \
  apt-get install -y curl git htop man unzip nano wget && \
  apt-get install -y python3 python3-six python2 python-six flex bison 

# Install dependencies for Visualization tool
RUN \
  git clone https://github.com/OPM/ResInsight.git


# Install Octave and required packages
RUN apt-get install -y octave octave-parallel octave-optim octave-signal octave-control




#install Petsc 
RUN \
  git clone -b release https://bitbucket.org/opengosim/pflotran_ogs_1.8.git && \
  git clone https://gitlab.com/petsc/petsc.git petsc  

RUN \  
  cd petsc && \
  git checkout v3.19.1 && \
  ./configure --download-openmpi=yes --download-hdf5=yes --with-hdf5-fortran-bindings=yes --download-fblaslapack=yes --download-metis=yes  --download-cmake=yes --download-ptscotch=yes --download-hypre=yes --with-debugging=0 COPTFLAGS=-O3 CXXOPTFLAGS=-O3 FOPTFLAGS=-O3 &&\ 
  make PETSC_DIR=/app/petsc PETSC_ARCH=ubuntu-opt all && \
  #make check &&\ 
  cd ../ && \
  cd pflotran_ogs_1.8/src/pflotran &&\  
  make -j4 pflotran modern_gfortran=1 
  #make test 


# Add files.
ADD target /app/target/

# Change permissions of the 'target' directory
RUN chmod -R 777 /app/target



COPY server.py /app/server.py

# Run the simulation 
# RUN ./pft.sh Coarse_CCS_3DF.in 4
  
# Install UM-Bridge dependencies
RUN apt update && \
    DEBIAN_FRONTEND="noninteractive" apt install -y python3-pip python3-venv && \
    pip3 install umbridge && \
    pip3 install pandas numpy scipy

# Define default command to run the test model.
CMD python3 /app/server.py



