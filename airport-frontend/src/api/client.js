const BASE_URL = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'

async function request(path, { method = 'GET', body, headers } = {}) {
  const res = await fetch(`${BASE_URL}${path}`, {
    method,
    headers: {
      'Content-Type': 'application/json',
      ...(headers || {})
    },
    body: body ? JSON.stringify(body) : undefined
  })
  if (!res.ok) {
    const text = await res.text()
    throw new Error(text || `Request failed: ${res.status}`)
  }
  const contentType = res.headers.get('content-type') || ''
  if (contentType.includes('application/json')) return res.json()
  return res.text()
}

export const api = {
  // Flights
  addFlight: (payload) => request('/flights/add_flight', { method: 'POST', body: payload }),
  scheduleList: () => request('/flights/list_scheduled_flights'),
  allFlights: () => request('/flight/get_all_flights'),
  cancelFlight: (payload) => request('/flights/cancel_flight', { method: 'POST', body: payload }),
  assignRunway: () => request('/flights/assign_runway'),
  cancelledList: () => request('/flights/cancelled_list'),

  // Runways
  runwayStatus: () => request('/runways/status'),
  clearDeparted: () => request('/runways/clear_departed'),

  // Routes
  addRoute: (payload) => request('/route/add_route', { method: 'POST', body: payload }),
  findRoute: (payload) => request('/route/find_route', { method: 'POST', body: payload })
}


