# GPS-Assisted PTP Precision Time Synchronization System

## Overview

This project explores precision time synchronization using a Raspberry Pi, a GPS receiver, a pulse-per-second (PPS) signal, and LinuxPTP.

The project focuses on the relationship between GPS-based time references, Precision Time Protocol (PTP), network topology, and synchronization behavior. It also documents configuration considerations and historical observations from the original experimental work.

The repository currently provides project documentation and example configuration templates. It does not include a complete, executable log-analysis utility or a packaged set of experimental log files.

## Project Objectives

- Explore the use of GPS and PPS signals as time references for a Linux-based synchronization system.
- Investigate the LinuxPTP Grandmaster workflow and PTP synchronization behavior.
- Examine how network topology may affect PTP path delay and clock offset.
- Document configuration considerations for Chrony, LinuxPTP, and system-clock synchronization.
- Identify the experimental conditions and supporting evidence needed for reproducible measurements.

## System Architecture

The following diagram illustrates the conceptual system architecture. The actual clock hierarchy, device connections, and service configuration should be verified against the original experimental setup.

```text
GPS Receiver
    |
    +---- NMEA ----> GPS Service / Time Reference
    |
    +---- PPS -----> GPIO / PPS Device
                         |
                         v
                  Linux Clock Setup
                         |
                         v
                      LinuxPTP
                       ptp4l
                         |
                         v
                  Ethernet Network
                         |
                         v
                     PTP Client
```

The precise role of each component depends on the system configuration. GPS time acquisition, PPS handling, system-clock discipline, and PTP synchronization are related but distinct functions.

## Repository Structure

```text
ptp-gps-grandmaster-clock/
├── README.md
├── requirements.txt
├── configs/
│   ├── chrony.conf.example
│   └── ptp4l.conf.example
└── tests/
    └── test_parse_ptp_logs.py
```

This structure reflects the intended repository layout. The test file is listed as a repository artifact, but its execution and compatibility with the current implementation have not been verified as part of this documentation update.

## Technologies

- **Raspberry Pi:** Hardware platform for the original synchronization project.
- **GPS Receiver:** Provides satellite-derived time information.
- **PPS Signal:** Provides a precise timing pulse for supported hardware and software configurations.
- **LinuxPTP:** Provides PTP functionality, including the `ptp4l` service.
- **Chrony:** Supports time-source management and system-clock synchronization where configured.
- **Python:** Relevant to potential log-analysis and data-processing extensions.

## Experimental Design

Meaningful comparisons of PTP synchronization behavior require consistent measurement conditions and clearly documented configurations.

The following factors should be recorded when conducting experiments:

1. **Network Topology:** Direct Ethernet connections, connections through a conventional network switch, and other tested configurations.
2. **Timestamping Mode:** Software or hardware timestamping, including network-interface capabilities.
3. **Time-Source Status:** GPS reception, PPS availability, and any interruptions to the reference signal.
4. **Clock Configuration:** The roles and relationships of Chrony, `ptp4l`, and `phc2sys`, where applicable.
5. **Measurement Conditions:** Experiment duration, sample count, discarded records, and relevant system logs.
6. **Statistical Methodology:** Definitions of clock offset and path delay, together with the calculation methods used.

These details are necessary to distinguish changes caused by network conditions from changes caused by clock configuration, timestamping behavior, or measurement methodology.

## Historical Observations

Notes from the original project recorded a PTP path-delay increase from **16,931 ns to 45,601 ns**. The increase was associated with queuing delay introduced by a network device that was not PTP-aware.

The original project also recorded clock-offset values of approximately **±30 ns to ±100 ns** under the reported configuration.

These figures are historical observations, not newly verified results from this repository update. Their interpretation depends on the original logs, experimental conditions, timestamping mode, clock configuration, and calculation methodology.

Before presenting these values as independently verified experimental results, the original evidence should be reviewed and the measurements reproduced where possible. Without sufficient supporting evidence, they should be treated as historical project notes rather than guaranteed system performance.

## Configuration Notes

The files under `configs/` are example templates. They are not universal configurations and should not be applied directly without review.

Before using or adapting them, verify:

- GPS and PPS device paths and the required drivers.
- Network-interface names and hardware timestamping support.
- Clock relationships and operating roles among Chrony, `ptp4l`, and `phc2sys`.
- Network settings, access controls, and firewall rules.
- Whether PTP configuration values accurately reflect the actual time-source status.
- Compatibility with the installed LinuxPTP and Chrony versions.

Back up existing configuration files before making changes. Avoid running multiple clock-disciplining services without understanding their interactions and the intended clock hierarchy.

## Limitations

- This repository documents the synchronization project and provides example configuration templates; it does not automatically configure the complete system.
- The current repository documentation does not establish that a standalone log-analysis utility is available.
- Historical observations have not been independently revalidated as part of this documentation update.
- Actual synchronization performance depends on hardware capabilities, clock sources, network conditions, timestamping mode, and configuration.
- The conceptual architecture may differ from the final physical implementation and should be checked against the original setup.

## Future Improvements

- Add a reproducible log-analysis utility with documented input formats and statistical calculations.
- Add unit tests and representative log samples to validate parsing behavior.
- Record the original experimental logs and configuration versions where available.
- Compare direct Ethernet connections with different network-device configurations under controlled conditions.
- Add plots of clock-offset and path-delay trends using verified measurement data.
- Document experiment procedures, software versions, and hardware configurations to improve reproducibility.

## Conclusion

This project investigates GPS-assisted time synchronization and the behavior of PTP in a Linux-based environment. Its main technical focus is the interaction between time references, clock configuration, timestamping, and network path delay.

Further validation and reproducible experimental evidence are needed to establish the reported synchronization performance and support quantitative comparisons across network configurations.
