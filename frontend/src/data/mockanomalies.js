
export const anomalies = [
  {
    id: "ANM-001",
    stationId: "AWS-JAI-002",
    stationName: "Jaipur AWS",
    parameter: "Temperature",
    observedValue: 34.2,
    suggestedValue: 32.1,
    unit: "°C",
    severity: "Warning",
    detectedAt: "2026-09-20T10:30:00+05:30",
    suspectedFault: "Possible sensor drift",
    evidence: [
      "Reading differs from the demonstration baseline.",
      "Sensor calibration may need verification."
    ],
    confidence: 0.82,
    reviewStatus: "Pending"
  },
  {
    id: "ANM-002",
    stationId: "AWS-KOL-004",
    stationName: "Kolkata AWS",
    parameter: "Humidity",
    observedValue: 85,
    suggestedValue: 78,
    unit: "%",
    severity: "Faulty",
    detectedAt: "2026-09-20T11:15:00+05:30",
    suspectedFault: "Possible sensor inconsistency",
    evidence: [
      "Reading has been flagged in the demonstration dataset.",
      "Additional sensor and temporal checks are required."
    ],
    confidence: 0.76,
    reviewStatus: "Pending"
  }
];