# M04 reference solution and reasoning

Initialize the descriptor to -1. Delete copy construction and copy assignment. Move construction takes the descriptor and resets the source to -1. Move assignment first releases the destination resource when objects differ, then takes the source. release() returns the integer and leaves -1; the caller now owns cleanup. Do not retry close blindly after EINTR on Linux because descriptor reuse can make a retry close an unrelated resource. std::string must be copied/moved through its language-defined operations, not raw bytes.
