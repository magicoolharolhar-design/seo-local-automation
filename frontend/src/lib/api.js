const API_BASE = '/api'

async function request(url, options = {}) {
  const res = await fetch(`${API_BASE}${url}`, {
    headers: { 'Content-Type': 'application/json', ...options.headers },
    ...options,
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(err.detail || 'Erro na requisição')
  }
  return res.json()
}

export async function getHealth() {
  return request('/health')
}

export async function uploadCsv(file) {
  const form = new FormData()
  form.append('file', file)
  const res = await fetch(`${API_BASE}/upload-csv`, { method: 'POST', body: form })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(err.detail || 'Erro no upload')
  }
  return res.json()
}

export async function listUploadedFiles() {
  return request('/uploaded-files')
}

export async function previewCsv(filename) {
  return request(`/preview-csv?filename=${encodeURIComponent(filename)}`)
}

export async function generateSingle(data) {
  return request('/generate', { method: 'POST', body: JSON.stringify(data) })
}

export async function generateAll(filename) {
  return request('/generate-all', { method: 'POST', body: JSON.stringify({ filename }) })
}

export async function downloadFile(filename) {
  return `${API_BASE}/download/${encodeURIComponent(filename)}`
}

export async function getHistory() {
  return request('/history')
}

export async function updateSettings(data) {
  return request('/settings', { method: 'POST', body: JSON.stringify(data) })
}

export async function getSettings() {
  return request('/settings')
}
