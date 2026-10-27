CXX ?= g++
CXXFLAGS = -std=c++17 -Wall -Wextra -Wpedantic -Werror -g
.PHONY: test clean
test: fd_owner
	./fd_owner
fd_owner: fd_owner.cpp
	$(CXX) $(CXXFLAGS) $< -o $@
clean:
	rm -f fd_owner
