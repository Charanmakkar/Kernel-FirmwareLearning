# Research method and refresh policy

The program uses official project documentation and source, Linux man-pages/POSIX interface documentation, language committee material, and board/manufacturer references. Primary references were checked on 27 October 2026. The reference skills framework is authored for the three tracks; no employer posting is presented as the user's JD.

Version-dependent code is tied to a teaching baseline in each project's VERSIONS.md. The Linux 6.12, Buildroot 2025.02.1 and Yocto 5.0.9 examples are deliberately frozen for reproducibility. They are not claims about the latest patch level. For a new product or a refreshed learning environment, select a maintained release, inspect migration notes/source declarations, update the lock/configuration records and rerun the affected builds and acceptance tests.

The current online Buildroot manual and other rolling documentation can describe features absent from the pinned release. Use release-local manuals and exact source/configuration when executing the projects. Likewise, the QEMU master documentation explains emulation concepts; actual evidence records the installed executable version. A source link is not evidence that the code was executed.

The complete source lists for specialized projects are retained beside those projects. The consolidated source catalogue deduplicates URLs while preserving original titles and claims. Bibliography identifiers in the lessons refer to Core_References.md. Interview and project files also contain direct references so they remain useful independently.

Refresh after a toolchain, kernel, BSP, board revision, datasheet revision or build-system change. Review source API declarations, configuration symbols, register behavior and relevant security advisories. Record the new build and target evidence rather than carrying forward old pass labels. Hardware behavior is claimed only for the named tested setup.
