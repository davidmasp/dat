
nextflow.enable.dsl=2

// general parsm
today = new Date().format('yyyy-MM-dd')

params.outdir = "results/"
params.figdir = "figures/"
params.tmpdir = "TMP"
params.tabdir = "tables"

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
  publishDir "${params.figdir}/YYY/${today}", mode: 'copy', pattern: "*.pdf"
  publishDir "${params.tabdir}/YYY/${today}", mode: 'copy', pattern: "*.json"
  publishDir "${params.tabdir}/YYY/${today}", mode: 'copy', pattern: "*.csv"
  label 'fullR'
  input:
    path(tabfiles, stageAs: "chrtabs/*")
  output:
    path("XXXX.csv")
    path("sex_determination.pdf")
  script: 
  """
  echo "XXXX" > ${info}_XXXXX.tab
  """
}

workflow {

  Channel.fromPath(params.index) \
      | splitCsv(header:true) \
      | map { row-> tuple(row.id, file(row.path)) } \
      | set{input_ch}

  XXXX(input_ch)

}
