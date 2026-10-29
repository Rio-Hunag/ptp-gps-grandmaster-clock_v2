<p align="center">
  <img
    src="https://capsule-render.vercel.app/api?type=waving&color=0:141E30,50:243B55,100:3A6073&height=200&section=header&text=GPS-Assisted%20PTP&fontSize=38&fontColor=ffffff&animation=fadeIn&fontAlignY=38&desc=Linux%20%7C%20Precision%20Time%20Synchronization&descAlignY=60&descSize=13"
    width="100%"
    alt="GPS-Assisted PTP Project Banner"
  />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black" alt="Linux"/>
  <img src="https://img.shields.io/badge/Raspberry%20Pi-C51A4A?style=for-the-badge&logo=raspberrypi&logoColor=white" alt="Raspberry Pi"/>
  <img src="https://img.shields.io/badge/LinuxPTP-243B55?style=for-the-badge" alt="LinuxPTP"/>
  <img src="https://img.shields.io/badge/GPS%20%2F%20PPS-3A6073?style=for-the-badge" alt="GPS PPS"/>
  <img src="https://img.shields.io/badge/Chrony-2C5364?style=for-the-badge" alt="Chrony"/>
</p>

<h2 align="center">GPS-Assisted PTP Time Synchronization</h2>

<p align="center">
  Exploring the relationship between GPS/PPS time references,
  LinuxPTP configuration, network topology, and clock synchronization.
</p>

<p align="center">
  <a href="#-project-overview">Overview</a> ·
  <a href="#-system-architecture">Architecture</a> ·
  <a href="#-configuration-templates">Configuration</a> ·
  <a href="#-historical-experimental-observations">Observations</a>
</p>

---

##  Project Overview

This project investigates GPS-assisted time synchronization using a Raspberry Pi, a GPS receiver, a pulse-per-second (PPS) signal, and LinuxPTP.

The main focus is understanding how time references, clock configuration, timestamping capabilities, and network topology influence Precision Time Protocol (PTP) behavior.

The repository provides system documentation, example configuration templates, and historical experimental notes. It is intended as an engineering reference rather than a turnkey system installer.

##  Engineering Focus

<table>
  <tr>
    <td width="50%" valign="top">
      <h3> GPS & PPS</h3>
      Understand the roles of GPS-derived time information and PPS timing signals in a Linux-based synchronization setup.
    </td>
    <td width="50%" valign="top">
      <h3> PTP Configuration</h3>
      Explore LinuxPTP configuration and the relationships among time sources, system clocks, and PTP devices.
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3> Network Effects</h3>
      Investigate how network topology and queueing can affect PTP path delay and clock-offset observations.
    </td>
    <td width="50%" valign="top">
      <h3>🔬 Reproducible Experiments</h3>
      Identify the configurations, logs, and measurement conditions needed to compare synchronization behavior.
    </td>
  </tr>
</table>

##  System Architecture

The following diagram illustrates the conceptual relationship between GPS/PPS references, Linux clock configuration, and PTP distribution. The exact clock hierarchy and physical connections depend on the original experimental setup.

```mermaid
flowchart TD
    GPS["GPS Receiver"]

    GPS -->|NMEA Data| TIME["GPS Service / Time Reference"]
    GPS -->|PPS Signal| PPS["PPS Device / GPIO"]

    TIME -. "Configured time source" .-> CLOCK["Clock Configuration"]
    PPS -. "Configured PPS reference" .-> CLOCK

    CLOCK -. "Depends on system setup" .-> PTP["LinuxPTP / ptp4l"]
    PTP --> ETH["Ethernet / PTP Network"]
    ETH --> CLIENT["PTP Client"]

    LOGS["System and ptp4l Logs"] --> ANALYSIS["Measurement Analysis"]

    style GPS fill:#243B55,color:#ffffff,stroke:#3A6073
    style PTP fill:#176B67,color:#ffffff,stroke:#2D9C91
    style CLIENT fill:#3A6073,color:#ffffff,stroke:#141E30
    style ANALYSIS fill:#243B55,color:#ffffff,stroke:#3A6073
