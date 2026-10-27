# M09 reference solution and reasoning

Stop publication of new requests and prevent the interrupt/source from requeueing. Synchronize the relevant interrupt handling and cancel or flush the work with APIs appropriate to its type. Only after no callback can use the state may storage be freed. Include remove-under-load, probe-failure, repeated bind/unbind and pending-work tests. The plan must avoid waiting for work while holding a lock that the worker needs.
