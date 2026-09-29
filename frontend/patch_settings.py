with open('src/pages/settings.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace mockdata import with hook
content = content.replace('import { stations } from "../data/mockdata";', 'import { useStationsData } from "../hooks/useStationsData";')

# Change default setting
content = content.replace('defaultStation: stations[0]?.id || ""', 'defaultStation: ""')

# Inject hook into Settings component
hook_injection = '''function Settings() {
  const { data: stationsData } = useStationsData();
  const stations = stationsData || [];
'''
content = content.replace('function Settings() {\n', hook_injection)

# Replace options map
old_options = '''            {stations.map((station) => (
              <option key={station.id} value={station.id}>
                {station.name}
              </option>
            ))}'''
new_options = '''            {stations.map((station) => (
              <option key={station.station_id} value={station.station_id}>
                {station.location} ({station.station_id})
              </option>
            ))}'''
content = content.replace(old_options, new_options)

with open('src/pages/settings.jsx', 'w', encoding='utf-8') as f:
    f.write(content)
