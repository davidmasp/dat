
#import "@preview/grape-suite:1.0.0": exercise
#import exercise: project, task, subtask, todo

#show: project.with(
    title: "{{ name }}",

    university: [{{ affiliation1 }}],
    institute: [{{affiliation2}}],
    seminar: [{{affiliation3}}],

    abstract: lorem(100),
    show-outline: true,

    author: "{{ author }}",

    show-solutions: false
)


= Report object 1

== Results

=== I did this

#lorem(50)

=== and that...

#lorem(50)

== Methods

=== How did I do it?

#lorem(50)

= Report object 2

#lorem(50)


/// TO INCLUDE text outside the current report

// #include "../00_test/test.typ"


/// BIBLIOGRAPHY
// example of how to cite work

// See @harry and then go to @electronic

// #bibliography("../works.yaml")


