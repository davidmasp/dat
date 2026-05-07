#!/usr/bin/env Rscript

# Minimal starter script for building a sample sheet or index file that can
# be consumed by an external Nextflow pipeline.

index <- data.frame(
  sample_id = c("sample_a", "sample_b"),
  fastq_1 = c("data/sample_a_R1.fastq.gz", "data/sample_b_R1.fastq.gz"),
  fastq_2 = c("data/sample_a_R2.fastq.gz", "data/sample_b_R2.fastq.gz")
)

write.csv(index, file = "index.csv", row.names = FALSE)
