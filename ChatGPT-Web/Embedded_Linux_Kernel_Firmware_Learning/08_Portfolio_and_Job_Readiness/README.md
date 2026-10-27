# Portfolio and job readiness

Build the portfolio from work you can reproduce and explain. Supplied reference implementations and logs establish what this package contains; they do not establish your contribution or proficiency. Use [Readiness_Gate.md](Readiness_Gate.md) before treating a topic as interview ready.

## Project README template

For one strong project, replace each bracketed field with your own evidence. These are intentional personal-evidence fields, not implied achievements.

```text
Project and problem: [specific user or engineering need]
Scope: [implemented behavior and explicit limits]
My contribution: [files, decisions, tests and investigations I performed]
Dependencies: [upstream components, versions and attribution]
Architecture: [components, interfaces, owners and persistent state]
Build and run: [commands from a clean checkout]
Acceptance: [requirement ID, stimulus, expected result, test]
Results: [observed outcome, environment and evidence path]
Failure investigation: [symptom, hypotheses, discriminating test, fix]
Limitations: [pending target, timing, security or durability checks]
Next improvement: [one justified change and its proposed test]
```

Use one diagram when it clarifies interfaces or failure boundaries. Keep raw logs and measurement data alongside the summarizing explanation. Record whether an execution used a host, user-mode emulator, full guest or physical board; those environments provide different evidence.

## Ten minute demonstration

Spend one minute on the problem and scope, two on architecture and ownership, three on a reproducible normal run, two on an injected failure and recovery, and two on results and limitations. Prepare a fallback log in case the environment is unavailable, and label playback as recorded evidence. The demonstration should show why a decision matters, not just that an executable prints output.

For B03, a useful defense is fragmentation, cancellation cleanup and protocol freshness limits. For I02, explain wait predicates and lifetime, then distinguish object compilation from guest execution. For a capstone, connect each mandatory requirement to its acceptance test. Choose a project aligned with the target role rather than presenting fifteen shallow demos.

## Evidence inventory

Maintain a row per claim: claim, your contribution, source commit, environment, command, input, observed result, raw artifact, reviewer and pending checks. If a number lacks a measurement record, omit it. Keep failed attempts when they explain a decision; they are valuable evidence of engineering judgment.

## Resume and project explanation templates

Use: “Implemented [component] in [language/platform] to [required behavior]; verified [specific cases] using [method].” For debugging: “Investigated [observed failure], identified [mechanism] through [evidence], and added [regression].” For measurements: “Changed [design] and observed [metric] from [baseline] to [result] under [stated workload].” Fill these only after doing the work and retaining evidence.

An honest learning-project bullet may mention a simulation or educational driver. Do not convert it into production deployment, customer impact, years of experience or hardware validation. List AI assistance and reused components accurately when asked about contribution. Prepare to modify a small requirement live and explain why the tests still apply.
