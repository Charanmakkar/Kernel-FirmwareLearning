# M08 reference solution and reasoning

Use file/readelf on the executable, verify its interpreter path inside the target root and confirm architecture. For boot failures, work from earliest verified stage: power/console/boot media before early logs; bootloader image/load addresses before kernel; root device, filesystem and built-in drivers for mount; executable/runtime/configuration for init or service. Every hypothesis should name an observation that can falsify it.
