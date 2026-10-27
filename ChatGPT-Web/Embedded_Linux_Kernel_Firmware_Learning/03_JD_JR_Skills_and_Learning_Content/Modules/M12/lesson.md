# M12 Bare metal startup peripherals and faults

## Objectives and prerequisites

Prerequisites: M04 M05 M11.

Explain reset-to-main, link memory correctly and design bounded peripheral handling and watchdog supervision.

## Lesson


Before main runs, startup establishes the processor's initial execution environment. On a Cortex-M system, the vector table supplies the initial stack pointer and exception entry addresses. Startup and the C runtime initialize data and zero-initialized storage, and board-specific initialization sets clocks and other essentials. The exact sequence is supplied by the selected device package; inspect it rather than replacing it with a generic internet file. [CMSIS]

A linker script and startup code form one contract. Symbols delimit data to copy from flash into RAM and bss to clear. Interrupt vectors must be placed where the processor expects them or where relocation config points. The stack grows into real memory and may collide with another region. Examine map output, reserve alignment correctly and measure stack high-water marks with an appropriate method; a successful link alone does not show enough runtime stack.

Configure a peripheral in a deliberate order: enable its clock, configure pins, reset/configure the peripheral, clear relevant pending status, prepare buffers/interrupt routing and then enable activity. The device reference manual decides the details. A timer can schedule periodic work without a blocking delay loop. PWM duty is not motor speed by itself; load, supply, feedback and control behavior matter. ADC readings need reference, calibration, sampling-time and input-network context.

An interrupt service routine, or ISR, should capture enough state to avoid data loss, acknowledge the source according to hardware rules and defer long processing. The nested vectored interrupt controller uses architecture-specific priority numbering and grouping; do not equate numerical priority values with intuitive high/low priority without reading the API contract. [NVIC]

A watchdog should be refreshed only after essential tasks show progress. A timer ISR that feeds it regardless of failed application work defeats its purpose. Define startup grace periods, reset-reason logging and a safe boot recovery path. A reset loop may indicate a bad configuration or persistent fault; record enough evidence without wearing out storage or repeatedly energizing actuators.

Fault handlers should preserve useful registers and fault status where supported, then enter a defined bounded state or reset policy. Printing from a HardFault handler through a driver that depends on interrupts can deadlock. A minimal retained crash record with an integrity check is often more useful than complicated output in a broken context.


## Worked lab and expected behavior


For the physical path, inspect the NUCLEO-F446RE board manual, STM32F446 reference manual, linker map and vendor startup file named in I05's hardware notes. Locate reset handler, vector table, data-copy and bss initialization. Observe a GPIO toggle from a timer and measure its period with a logic analyzer; a terminal print interval is not the same measurement.

On the host, review the equivalent bounded state-machine logic and unit tests, but record physical startup, peripheral and interrupt measurements as pending. If firmware faults before main, inspect stack/vector addresses, clock setup and memory placement before changing application logic.


## Independent work

Attempt [exercises.md](exercises.md) before opening [solutions.md](solutions.md).

## Review and interview connections

What happens before main? How do load and run addresses differ? Why can printf fail in an ISR? Interview bank: firmware startup and fault handling.

## Mastery checklist

- Explain the selected startup file.
- Read a map and stack budget.
- Bound ISR work.
- Demonstrate watchdog purpose and reset evidence.

## Primary references

[CMSIS] Arm startup contract. [NVIC] Arm interrupt controller APIs. [NUCLEO] ST board documentation. [LD] Linker scripts.
