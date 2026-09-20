
export const sensorHealth = [
  {
    stationId: "AWS-DEL-001",
    sensors: [
      { type: "Temperature", health: 98, status: "Healthy" },
      { type: "Pressure", health: 96, status: "Healthy" },
      { type: "Humidity", health: 97, status: "Healthy" }
    ]
  },
  {
    stationId: "AWS-JAI-002",
    sensors: [
      { type: "Temperature", health: 72, status: "Warning" },
      { type: "Pressure", health: 95, status: "Healthy" },
      { type: "Humidity", health: 94, status: "Healthy" }
    ]
  },
  {
    stationId: "AWS-MUM-003",
    sensors: [
      { type: "Temperature", health: 97, status: "Healthy" },
      { type: "Pressure", health: 98, status: "Healthy" },
      { type: "Humidity", health: 96, status: "Healthy" }
    ]
  },
  {
    stationId: "AWS-KOL-004",
    sensors: [
      { type: "Temperature", health: 94, status: "Healthy" },
      { type: "Pressure", health: 93, status: "Healthy" },
      { type: "Humidity", health: 38, status: "Faulty" }
    ]
  },
  {
    stationId: "AWS-BLR-005",
    sensors: [
      { type: "Temperature", health: 96, status: "Healthy" },
      { type: "Pressure", health: 97, status: "Healthy" },
      { type: "Humidity", health: 95, status: "Healthy" }
    ]
  }
];