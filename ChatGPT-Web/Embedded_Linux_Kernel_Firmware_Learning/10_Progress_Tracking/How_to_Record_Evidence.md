# Record learning evidence

Keep learner progress separate from package validation. The supplied implementation logs describe checks performed while producing the package. They do not establish your current proficiency. Your tracker begins at not assessed.

For each assessment save the task, your attempt, source version, exact commands, tool versions, raw outputs, elapsed time, assistance allowed/used, score, critical failures and next correction. Use a stable evidence path in the tracker. Preserve the failed version when practical so a reviewer can see that the regression test catches the original defect.

Use five learner states: not assessed, learning, implemented with assistance, independently demonstrated and needs refresh. Mark independently demonstrated only after completing a new variant without reference code and explaining the result. Revisit important skills after two and six weeks using different input data. An unrun test is recorded as not run; it is never a pass.

The score is subordinate to critical gates. A memory overwrite, proven data race, invalid lifetime, acceptance of an unsafe stale command or invented evidence blocks a pass until corrected. If a tool is unavailable, record the missing check and use another method only for the portion it can actually establish.
