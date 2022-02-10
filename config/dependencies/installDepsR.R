#!/usr/bin/env Rscript

# Name: installDepsR.R
# Author: DMP
# Description:

# pre-imports ---------------------------------------------------------------

if (!require("BiocManager", quietly = TRUE))
  install.packages("BiocManager", repos = "http://cran.us.r-project.org")

if (!require("available", quietly = TRUE))
  install.packages("available", repos = "http://cran.us.r-project.org")

library(available)

if (!require("remotes", quietly = TRUE))
  install.packages("remotes", repos = "http://cran.us.r-project.org")

library(remotes)

list_of_installed_packages = rownames(installed.packages())
pkg = readLines("dependenciesR.txt")

pkg = pkg[!pkg %in% list_of_installed_packages]

install_pkg <- function(pkg_name) {
  if (!available_on_cran(name = pkg_name)){
    install.packages(pkg_name, repos = "http://cran.us.r-project.org")
  } else if (!available_on_bioc(pkg_name)) {
    BiocManager::install(pkg_name)
  } else {
    print(glue::glue("installing {pkg_name}"))
    slug = glue::glue("davidmasp/{pkg_name}@develop")
    remotes::install_github(slug,upgrade = "never", quiet = TRUE)
  }
}

if (length(pkg) > 0){
        purrr::walk(pkg, install_pkg)
} else {
        print("all deps are installed!")
}
