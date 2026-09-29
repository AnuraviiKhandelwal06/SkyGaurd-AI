import re

with open('src/hooks/useStationsData.js', 'r', encoding='utf-8') as f:
    content = f.read()

new_effect = '''  useEffect(() => {
    fetchData();
    let pollMs = 30000;
    try {
      const saved = JSON.parse(localStorage.getItem("skyguard-settings") || "{}");
      if (saved.refreshInterval) {
        pollMs = parseInt(saved.refreshInterval, 10) * 1000;
      }
    } catch(e) {}
    const interval = setInterval(fetchData, pollMs);
    return () => clearInterval(interval);
  }, [fetchData]);'''

content = re.sub(r'  useEffect\(\(\) => \{\n    fetchData\(\);\n    const interval = setInterval\(fetchData, 30000\); // 30s polling\n    return \(\) => clearInterval\(interval\);\n  \}, \[fetchData\]\);', new_effect, content, flags=re.DOTALL)

with open('src/hooks/useStationsData.js', 'w', encoding='utf-8') as f:
    f.write(content)
