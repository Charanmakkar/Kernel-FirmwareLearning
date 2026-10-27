# M10 reference solution and reasoning

A partial user copy can lose bytes already dequeued. Choose an implementation that commits only the transferred portion or a documented transactional policy with suitable buffering and locks. Do not retain a spinlock across user access. Define readable when data exists, writable when capacity exists, and hangup/error conditions according to teardown. Test with ordinary small buffers and controlled invalid user pages in a disposable guest; never claim a host mock establishes uaccess correctness.
