// Original C++17 teaching example. Linux POSIX descriptor ownership.
#include <cassert>
#include <cerrno>
#include <fcntl.h>
#include <unistd.h>
#include <utility>
#include <iostream>

class fd_owner {
    int fd_ = -1;
    void cleanup() noexcept {
        if (fd_ >= 0) {
            const int saved = errno;
            // Linux releases the descriptor even for most close errors.
            // Retrying could close a descriptor reused by another thread.
            (void)::close(fd_);
            errno = saved;
        }
        fd_ = -1;
    }
public:
    explicit fd_owner(int fd = -1) noexcept : fd_(fd) {}
    ~fd_owner() { cleanup(); }
    fd_owner(const fd_owner&) = delete;
    fd_owner& operator=(const fd_owner&) = delete;
    fd_owner(fd_owner&& other) noexcept : fd_(other.release()) {}
    fd_owner& operator=(fd_owner&& other) noexcept {
        if (this != &other) { cleanup(); fd_ = other.release(); }
        return *this;
    }
    int get() const noexcept { return fd_; }
    int release() noexcept { const int result=fd_; fd_=-1; return result; }
};

int main() {
    int p[2];
    assert(::pipe(p)==0);
    {
        fd_owner first(p[0]);
        fd_owner second(std::move(first));
        assert(first.get()==-1 && second.get()==p[0]);
        fd_owner third;
        third=std::move(second);
        assert(second.get()==-1 && third.get()==p[0]);
        assert(::fcntl(third.get(),F_GETFD)!=-1);
    }
    errno=0;
    assert(::fcntl(p[0],F_GETFD)==-1 && errno==EBADF);
    {
        fd_owner writer(p[1]);
        int released=writer.release();
        assert(writer.get()==-1 && released==p[1]);
        assert(::fcntl(released,F_GETFD)!=-1);
        assert(::close(released)==0);
    }
    {
        fd_owner invalid;
        errno=123;
    }
    assert(errno==123);
    std::cout << "fd_owner: move, release, scope cleanup, invalid owner passed\n";
}
