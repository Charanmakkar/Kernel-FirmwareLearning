# Skill assessment suite

Begin with [Diagnostic](questions/Diagnostic.md). Do not read its [answer key](answers/Diagnostic_Key.md) until your timed attempt is complete. Scores are not assigned in advance.

Use [Topic quizzes](questions/Topic_Quizzes.md), [Phase exits](questions/Phase_Exit_Tests.md), [Timed coding](questions/Timed_Coding_Tests.md), [Debugging challenges](questions/Debugging_Challenges.md), [Role mocks](questions/Role_Mock_Interviews.md), and the [Final practical](questions/Final_Practical_and_Defense.md). Complete [Scoring and evidence rules](Scoring_and_Evidence.md) before interpreting results. Record results in [Evidence tracker](Evidence_Tracker.csv).

Reference implementations and answers are intentionally separated under `answers/`. The files in `fixtures/` include deliberately broken source and synthetic traces. They are assessment inputs, not project implementations or evidence from real hardware. Do not run broken examples on a production device.

For the 30 portable coding reference routines, compile `answers/coding_reference.c` with the command in its header. The POSIX Q061 example is `answers/posix_reference.c`. Actual validation results and sanitizer limitations are recorded in [Reference validation](answers/VALIDATION.md).

An independent attempt forbids AI and answer keys. An AI-assisted attempt is separately labeled and must retain prompts, accepted changes, verification, and a later independent explanation. Neither attempt substitutes for real hardware checks.
