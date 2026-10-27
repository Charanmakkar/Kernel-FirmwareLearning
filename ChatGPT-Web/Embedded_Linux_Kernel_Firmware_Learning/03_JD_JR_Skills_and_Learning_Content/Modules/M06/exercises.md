# M06 independent exercise

Timebox 90 minutes. Write a pipe reader that accepts multiple newline-delimited records, handles records split across reads, limits a record to 256 bytes and exits cleanly when the writer closes. Demonstrate a partial final record, an oversized record and interruption. Specify whether the partial final record is accepted.
