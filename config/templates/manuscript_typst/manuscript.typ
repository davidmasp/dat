#import "@preview/grape-suite:1.0.0": exercise
#import exercise: project, task, subtask, todo

#show: project.with(
  title: "Manuscript Title",

  university: [Affiliation 1],
  institute: [Affiliation 2],
  seminar: [Affiliation 3],

  abstract: lorem(80),
  show-outline: true,

  author: "Author Name",

  show-solutions: false,
)

= Introduction

#lorem(80)

= Results

== Main finding

#lorem(60)

= Methods

#lorem(60)

= Discussion

#lorem(60)

// Local artifacts can be referenced from the manuscript folder, for example:
// #figure(
//   image("artifacts/main_artifacts/figure01/panel_a.pdf"),
//   caption: [Example imported panel],
// )

// Shared text can be included from the reports root when useful:
// #include "../main_MM/analysis1.typ"

// Bibliography example:
// #bibliography("../works.yaml")
