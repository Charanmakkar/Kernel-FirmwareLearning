# M10 independent exercise

Timebox 90 minutes. Review an educational FIFO driver that removes bytes before copy_to_user and returns EFAULT when the copy partly fails. Explain its data-loss behavior, choose documented semantics and propose a safe test. Then define poll results for empty/full/shutdown states.
