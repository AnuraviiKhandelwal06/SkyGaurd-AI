import re

with open('src/pages/sensorhealth.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace chartData creation
old_chart = '''  const chartData = [
    { name: "Jan", health: 100 },
    { name: "Feb", health: 100 },
    { name: "Mar", health: 100 },
    { name: "Apr", health: 95 },
    { name: "May", health: 98 },
    { name: "Jun", health: 92 },
    { name: "Jul", health: 90 },
    { name: "Aug", health: 85 },
    { name: "Sep", health: 88 },
    { name: "Oct", health: 80 },
    { name: "Nov", health: 82 },
    { name: "Dec", health: healthData?.health_score_pct || 100 }
  ];'''

new_chart = '''  const chartData = (healthData?.degradation_trend && healthData.degradation_trend.length > 0) 
    ? healthData.degradation_trend 
    : [{ name: "No data available", health: healthData?.health_score_pct || 0 }];'''

content = content.replace(old_chart, new_chart)

with open('src/pages/sensorhealth.jsx', 'w', encoding='utf-8') as f:
    f.write(content)
