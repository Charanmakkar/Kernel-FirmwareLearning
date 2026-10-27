# Physical UART integration worksheet

Physical testing is pending. Fill these fields from the selected board manual before connecting hardware: board model and revision; connector name; TX pin; RX pin; signal-ground pin; logic voltage; pinmux setting; UART controller; Linux device path; adapter model; adapter voltage selection. This is an intentionally optional hardware route, not an incomplete software reference.

| Connection | Requirement |
|---|---|
| Adapter TX to board RX | Compatible logic voltage and selected UART RX pin |
| Adapter RX to board TX | Compatible logic voltage and selected UART TX pin |
| Adapter ground to board ground | Common signal reference |
| Adapter power output | Leave disconnected when both sides are powered independently |

Record oscilloscope or logic-analyzer evidence for bit period, idle level, framing, and disconnect recovery. Do not label PTY evidence as hardware validation.
