#!/usr/bin/env Rscript
args = commandArgs(trailingOnly=TRUE)

if (length(args)==0) {
  stop("Usage:  Rscript compute_7q10.r <station_name>", call.=FALSE)
}

ignore_missing <- FALSE

result <- fasstr::compute_frequency_quantile(station_number=args[1], roll_days=7, return_period=10, ignore_missing=FALSE)

cat(result)
