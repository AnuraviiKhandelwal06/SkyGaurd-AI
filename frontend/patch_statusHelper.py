content = '''export function normalizeStatus(rawStatus, anomalyType = '') {
  const statusStr = (rawStatus || '').toLowerCase();
  
  if (statusStr === 'critical' || statusStr === 'faulty') {
    return 'Faulty';
  }
  
  if (statusStr === 'warning') {
    return 'Warning';
  }
  
  // resolved, healthy, normal, pristine, etc.
  return 'Healthy';
}

export function getStatusColor(status) {
  const norm = normalizeStatus(status);
  if (norm === 'Warning') return 'orange';
  if (norm === 'Faulty') return 'red';
  return 'green';
}
'''
with open('src/utils/statusHelper.js', 'w', encoding='utf-8') as f:
    f.write(content)
