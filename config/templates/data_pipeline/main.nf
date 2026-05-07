
nextflow.enable.dsl=2

// general params
params.outdir = "results"
params.tmpdir = "${params.outdir}/TMP"
params.figdir = "${params.outdir}/figures"
params.tabdir = "${params.outdir}/tables"

// folder params
params.index = "$baseDir/index.csv"

// a temporal process
process XXXX {
  label 'short' 
  publishDir "${params.tmpdir}/XXXX", mode: 'symlink'
  input:
    tuple val(info), path(tab)
  output:
    tuple val(info), path("${info}_XXXXX.tab"), emit: tab
  script:
  """
  echo "XXXX" > ${info}_XXXXX.tab
  """
}

// a figure producing process
process YYYY {
  publishDir "${params.figdir}/YYY/", mode: 'copy', pattern: "*.png"
  publishDir "${params.figdir}/YYY/", mode: 'copy', pattern: "*.pdf"
  publishDir "${params.tabdir}/YYY/", mode: 'copy', pattern: "*.json"
  publishDir "${params.tabdir}/YYY/", mode: 'copy', pattern: "*.csv"
  label 'fullR'
  input:
    path(tabfiles, stageAs: "chrtabs/*")
  output:
    path("XXXX.csv")
    path("sex_determination.pdf")
  script: 
  """
  echo "XXXX" > XXXX.csv
  """
}

workflow {

  input_ch = channel.fromPath(params.index) \
      | splitCsv(header:true) \
      | map { row-> tuple(row.id, file(row.path)) } \
      | set{input_ch}

  XXXX(input_ch)
  YYYY(XXXX.out.tab)

}
