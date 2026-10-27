# M07 reference solution and reasoning

Keep every predicate read and write under the same mutex. Wait in a while loop and return from the loop only when work or the shutdown rule permits progress. Broadcast on shutdown, then join before destroying mutexes/conditions. A second consumer may consume the item between another waiter being signalled and acquiring the mutex; that waiter must recheck. Tests should verify the aggregate record sequence/count rather than a scheduler-specific order between consumers.
