# GPS-Assisted PTP Precision Time Synchronization System

A Raspberry Pi-based project exploring precision time synchronization using a GPS receiver, a pulse-per-second (PPS) signal, and LinuxPTP. The project focuses on network time synchronization, path-delay analysis, and reproducible analysis of synchronization logs.

> **Data Integrity Statement**
>
> This repository contains an executable Python log-analysis utility, unit tests, and sample log files. The logs under `tests/fixtures/` are synthetic data created to test the parser and **are not measurements collected from physical hardware**.
>
> Historical observations from the original project, including a path-delay increase from 16,931 ns to 45,601 ns and clock-offset values of approximately ±30 ns to ±100 ns, have not been revalidated through new hardware experiments during this repository update. Before publishing these figures as experimental results, verify the original logs, measurement conditions, and calculation methods, and include supporting evidence in `results/`.

## Project Objectives

- Integrate a GPS time reference and PPS signal to investigate Linux system-clock synchronization and the PTP Grandmaster workflow.
- Compare the effects of different network topologies on PTP path delay and clock offset.
- Develop a Python utility to extract clock-offset and path-delay measurements from `ptp4l` logs and calculate descriptive statistics.
- Use automated tests to verify how the log parser handles valid records, empty input, and malformed data.

## System Architecture

The following diagram illustrates the conceptual architecture. Confirm the actual data paths, physical connections, and clock sources against the original experimental setup.

```text
GPS Receiver ── NMEA ──> GPS Service / Time Source
      |
      └──── PPS ──────> GPIO / PPS Device
                              |
                              v
                     Linux System Clock
                       Synchronization
                              |
                              v
                         LinuxPTP
                           ptp4l
                              |
                              v
                      Ethernet / PTP Client

ptp4l Logs ──> Python Parser ──> Statistical Summary / CSV
```

## Repository Structure

```text
ptp-gps-grandmaster-clock/
├── README.md
├── requirements.txt
├── configs/
│   ├── chrony.conf.example
│   └── ptp4l.conf.example
├── scripts/
│   └── parse_ptp_logs.py
├── tests/
│   ├── test_parse_ptp_logs.py
│   └── fixtures/
│       ├── normal.log
│       └── malformed.log
└── results/
    └── README.md
```

## Running the Log Analysis Utility

**Requirement:** Python 3.10 or later.

### 1. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Linux or macOS:

```bash
source .venv/bin/activate
```

Activate it in Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

The parser uses the Python standard library and does not require third-party packages.

### 3. Analyze a Sample Log

```bash
python scripts/parse_ptp_logs.py tests/fixtures/normal.log
```

### 4. Export Parsed Measurements to CSV

```bash
python scripts/parse_ptp_logs.py tests/fixtures/normal.log --csv results/parsed.csv
```

### 5. Export Summary Statistics to JSON

```bash
python scripts/parse_ptp_logs.py tests/fixtures/normal.log --json results/summary.json
```

> **Note:** The sample logs are synthetic test data. Their output can be used to verify the parser's behavior, but it must not be interpreted as evidence of real-world synchronization accuracy.

## Statistical Metrics

For successfully parsed records, the utility calculates the following metrics:

- **Sample Count:** Number of valid records successfully extracted from the log.
- **Mean Clock Offset:** Arithmetic mean of the signed clock-offset values.
- **RMS Clock Offset:** Root mean square of the clock-offset values, representing their overall magnitude.
- **Maximum Absolute Clock Offset:** Largest absolute clock-offset value among all samples.
- **Offset Standard Deviation:** Population standard deviation, calculated using `ddof=0`.
- **Path-Delay Statistics:** Mean, minimum, and maximum values calculated from the `path delay` field.

These metrics describe different aspects of the measurements and should not be used interchangeably.

The utility analyzes fields recorded in the input logs. It does not independently verify GPS lock status, end-to-end PTP synchronization accuracy, or hardware timestamping capabilities.

## Running Automated Tests

Run the unit tests from the repository root:

```bash
python -m unittest discover -s tests -v
```

The test suite covers valid records, negative clock offsets, empty input, malformed log lines, and statistical calculations.

## Experimental Design and Results

To make comparisons meaningful and reproducible, record the following conditions for each experiment:

1. **Network Topology:** Direct Ethernet connections, connections through a conventional network switch, and any other tested configurations.
2. **Timestamping Mode:** Software or hardware timestamping, including interface capabilities and startup logs.
3. **Time-Source Status:** GPS/PPS status and whether the reference signal was lost during the experiment.
4. **Measurement Conditions:** Experiment start and end times, sample count, and number of discarded records.
5. **Statistical Methodology:** Explicit definitions of clock offset, path delay, and the statistical metrics used.

Historical project notes recorded a path-delay increase from **16,931 ns to 45,601 ns**. The change was associated with queuing delay introduced by a network device that was not PTP-aware.

Before publishing this observation as a verified experimental result, include the original logs, network-topology photographs or diagrams, and calculation methodology. If the supporting evidence is unavailable, retain the figures only as clearly identified historical observations rather than results from the current repository version.

## Configuration Notes

The files under `configs/` are **reference templates**, not universal configurations that can be applied directly to every device.

Before using them, verify the following:

- GPS device paths, PPS device paths, and the relevant drivers.
- Network interface names and hardware timestamping support.
- Clock relationships and operating roles among `chrony`, `ptp4l`, and `phc2sys`.
- Network subnets, access controls, and firewall rules.
- Whether PTP settings, including clock-class declarations, accurately reflect the actual time-source status.

Back up existing system configurations and validate all settings against the documentation for the installed LinuxPTP and Chrony versions.

Do not enable potentially conflicting clock-disciplining processes without understanding their interactions and the intended clock hierarchy.

## Limitations

- The parser supports the `ptp4l` log format targeted by the current implementation. Other LinuxPTP versions or log formats may require additional parsing rules.
- Analysis results depend on the completeness and correctness of the input logs.
- Synthetic test data does not replace physical hardware testing.
- This repository does not automatically configure the GPS receiver, PPS device, network interface, or system services.

## Future Improvements

- Expand parser coverage with log samples and tests from additional LinuxPTP versions.
- Generate reproducible comparison reports for different network topologies.
- Add visualization of clock-offset and path-delay trends.
- Record experimental environments, configuration versions, and checksums for original log files.
