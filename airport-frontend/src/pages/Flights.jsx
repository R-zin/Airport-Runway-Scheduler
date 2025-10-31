import React, { useEffect, useMemo, useState } from 'react'
import { Box, Grid, Paper, TextField, FormControlLabel, Switch, Button, Typography, Divider, Snackbar, Alert, Chip, Stack } from '@mui/material'
import { api } from '../api/client'

export default function Flights() {
  const [flightNo, setFlightNo] = useState('')
  const [destination, setDestination] = useState('')
  const [timeStr, setTimeStr] = useState('12:00')
  const [isEmergency, setIsEmergency] = useState(false)
  const [scheduled, setScheduled] = useState([])
  const [allFlights, setAllFlights] = useState([])
  const [cancelled, setCancelled] = useState([])
  const [snack, setSnack] = useState({ open: false, message: '', severity: 'success' })

  const show = (message, severity = 'success') => setSnack({ open: true, message, severity })

  const loadData = async () => {
    const [s, a, c] = await Promise.all([
      api.scheduleList(),
      api.allFlights(),
      api.cancelledList()
    ])
    setScheduled(s.data || [])
    setAllFlights(a.data || [])
    setCancelled(c.cancelled_list || [])
  }

  useEffect(() => {
    loadData().catch(err => show(err.message, 'error'))
  }, [])

  const handleAdd = async () => {
    if (!flightNo || !destination || !timeStr) return show('Fill all fields', 'warning')
    await api.addFlight({ flight_no: flightNo, destination, time_str: timeStr, is_emergency: isEmergency })
    await loadData()
    show(`Flight ${flightNo} added`)
    setFlightNo(''); setDestination('')
  }

  const handleCancel = async (id) => {
    await api.cancelFlight({ flight_no: id })
    await loadData()
    show(`Cancelled ${id}`)
  }

  const handleAssign = async () => {
    await api.assignRunway()
    await loadData()
    show('Runway allocation done')
  }

  const FlightCard = ({ f }) => (
    <Paper sx={{ p: 2, mb: 1 }}>
      <Stack direction="row" spacing={2} alignItems="center" justifyContent="space-between">
        <Box>
          <Typography variant="subtitle1">{f.flight_no || f.flight_number}</Typography>
          <Typography variant="body2" color="text.secondary">
            {f.destination} • {f.departure_time}
          </Typography>
        </Box>
        <Stack direction="row" spacing={1}>
          {f.Emergency_flight || f.is_emergency ? <Chip color="error" label="EMERGENCY" /> : null}
          <Chip label={f.status || 'Waiting'} color={(f.status || '').includes('Runway') ? 'primary' : 'default'} />
        </Stack>
        {f.status !== 'Cancelled' && (
          <Button variant="outlined" color="error" onClick={() => handleCancel(f.flight_no || f.flight_number)}>Cancel</Button>
        )}
      </Stack>
    </Paper>
  )

  return (
    <Grid container spacing={3}>
      <Grid item xs={12} md={6}>
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" sx={{ mb: 2 }}>Add Flight</Typography>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6}>
              <TextField fullWidth label="Flight No" value={flightNo} onChange={(e) => setFlightNo(e.target.value)} />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField fullWidth label="Destination" value={destination} onChange={(e) => setDestination(e.target.value)} />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField fullWidth type="time" label="Departure Time" value={timeStr} onChange={(e) => setTimeStr(e.target.value)} InputLabelProps={{ shrink: true }} />
            </Grid>
            <Grid item xs={12} sm={6}>
              <FormControlLabel control={<Switch checked={isEmergency} onChange={(e) => setIsEmergency(e.target.checked)} />} label="Emergency" />
            </Grid>
          </Grid>
          <Box sx={{ mt: 2, display: 'flex', gap: 1 }}>
            <Button variant="contained" onClick={handleAdd}>Add Flight</Button>
            <Button variant="outlined" onClick={handleAssign}>Assign Runways</Button>
          </Box>
        </Paper>
      </Grid>

      <Grid item xs={12} md={6}>
        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6">Scheduled Flights</Typography>
          <Divider sx={{ my: 1 }} />
          <Box>
            {(scheduled || []).map((f, idx) => (
              <FlightCard key={`s-${idx}`} f={f} />
            ))}
            {(!scheduled || scheduled.length === 0) && <Typography color="text.secondary">No flights waiting</Typography>}
          </Box>
        </Paper>

        <Paper sx={{ p: 3 }}>
          <Typography variant="h6">All Flights</Typography>
          <Divider sx={{ my: 1 }} />
          <Box>
            {(allFlights || []).map((f, idx) => (
              <FlightCard key={`a-${idx}`} f={f} />
            ))}
            {(!allFlights || allFlights.length === 0) && <Typography color="text.secondary">No flights yet</Typography>}
          </Box>
        </Paper>
      </Grid>

      <Grid item xs={12}>
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6">Cancelled Flights</Typography>
          <Divider sx={{ my: 1 }} />
          <Box>
            {(cancelled || []).map((f, idx) => (
              <FlightCard key={`c-${idx}`} f={f} />
            ))}
            {(!cancelled || cancelled.length === 0) && <Typography color="text.secondary">No cancellations</Typography>}
          </Box>
        </Paper>
      </Grid>

      <Snackbar open={snack.open} autoHideDuration={3000} onClose={() => setSnack(s => ({ ...s, open: false }))}>
        <Alert onClose={() => setSnack(s => ({ ...s, open: false }))} severity={snack.severity} sx={{ width: '100%' }}>
          {snack.message}
        </Alert>
      </Snackbar>
    </Grid>
  )
}


