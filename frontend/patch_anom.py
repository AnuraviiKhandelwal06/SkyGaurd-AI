import re

with open('src/pages/anomalydetection.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

correction_start = content.find('          {/* Data correction */}')
correction_end = content.find('        </>\n      )}\n\n    </div>')

if correction_start != -1 and correction_end != -1:
    correction_html = content[correction_start:correction_end]
    new_correction_html = '''          {/* Data correction */}
          {normalizeStatus(selected.status) === "Warning" ? (
            <section className="bg-white rounded-xl border border-gray-200 p-6">
              <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <Wrench className="text-teal-600" />
                Data Correction
              </h2>
              <div className="bg-yellow-50 text-yellow-800 p-4 rounded-lg">
                <p className="font-semibold">Genuine event, no correction needed.</p>
              </div>
            </section>
          ) : (
''' + correction_html.replace('          {/* Data correction */}', '') + '''
          )}
'''
    new_content = content[:correction_start] + new_correction_html + content[correction_end:]
    
    with open('src/pages/anomalydetection.jsx', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Patched anomalydetection.jsx")
else:
    print("Could not find block")
