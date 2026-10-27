# M12 reference solution and reasoning

Each critical task advances a progress token after completing its required work; the supervisor checks all required tokens within a defined window and feeds only if they progressed. A task that loops while repeatedly setting a Boolean is weak evidence; use sequence/time conditions tied to actual completion. Persist reset reason with a bounded write policy, and on repeated failures enter recovery. Hardware reset timing and output state require board measurement.
