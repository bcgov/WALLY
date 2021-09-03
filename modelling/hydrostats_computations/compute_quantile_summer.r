#!/usr/bin/env Rscript
args = commandArgs(trailingOnly=TRUE)

if (length(args)!=3) {
  stop("Usage:  Rscript compute_quantile.r <station_name> <roll_days> <return_period>", call.=FALSE)
}

ignore_missing <- FALSE
roll_days <- as.numeric(args[2])
return_period <- as.numeric(args[3])

result <- fasstr::compute_frequency_quantile(station_number=args[1], roll_days=roll_days, return_period=return_period, ignore_missing=FALSE, months=6:9)

cat(result)
