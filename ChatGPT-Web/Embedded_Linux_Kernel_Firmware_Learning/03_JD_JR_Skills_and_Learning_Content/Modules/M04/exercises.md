# M04 independent exercise

Timebox 60 minutes. Implement a move-only C++17 owner for a POSIX file descriptor. Add get(), release() and a destructor. Test moving, releasing, invalid descriptor destruction and scope exit. Separately explain why memcpy of a live std::string object is invalid ownership handling.
