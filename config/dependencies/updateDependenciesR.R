#!/usr/bin/env Rscript

# Name: updateDependenciesR
# Author: DMP
# Description: 
# Searches over the file structure of the project for pkg dependencies.
# It generates a list of dependencies as dependenciesR.txt
# Note, to avoid recurrence nightmare with multiple directories is recommended
# to run the code in a freshly cloned repo.

# imports -----------------------------------------------------------------

if (!require(renv, quietly = TRUE)){
  install.packages("renv")
}

if (!require(fs, quietly = TRUE)){
  install.packages("fs")
}

# list all files
# this should be the root dir of the project
all_files = fs::dir_ls("../../", recurse = TRUE, glob = "*.R")

deps_df = renv::dependencies(all_files)

writeLines(deps_df$Package, con = "dependenciesR.txt")
