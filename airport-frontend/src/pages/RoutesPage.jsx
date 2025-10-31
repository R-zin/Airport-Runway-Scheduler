import React, { useState } from 'react'
import { Paper, Typography, Grid, TextField, Button, Divider, Alert, Snackbar } from '@mui/material'
import { api } from '../api/client'

export default function RoutesPage() {
  const [src, setSrc] = useState('JFK')
  const [dest, setDest] = useState('LAX')
  const [distance, setDistance] = useState(5)
  const [findSrc, setFindSrc] = useState('JFK')
  const [findDest, setFindDest] = useState('LHR')
  const [result, setResult] = useState(null)
  const [snack, setSnack] = useState({ open: false, message: '', severity: 'success' })

  const show = (message, severity = 'success') => setSnack({ open: true, message, severity })

  const handleAddRoute = async () => {
    if (!src || !dest || !distance) return show('Provide src, dest and distance', 'warning')
    await api.addRoute({ src, dest, distance: Number(distance) })
    show('Route added')
  }

  const handleFindRoute = async () => {
    const r = await api.findRoute({ src: findSrc, dest: findDest })
    setResult(r)
  }

  return (
    <Grid container spacing={3}>
      <Grid item xs={12} md={6}>
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6">Add Route</Typography>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12} sm={4}><TextField fullWidth label="Source" value={src} onChange={(e) => setSrc(e.target.value)} /></Grid>
            <Grid item xs={12} sm={4}><TextField fullWidth label="Destination" value={dest} onChange={(e) => setDest(e.target.value)} /></Grid>
            <Grid item xs={12} sm={4}><TextField fullWidth type="number" label="Distance" value={distance} onChange={(e) => setDistance(e.target.value)} /></Grid>
          </Grid>
          <Button sx={{ mt: 2 }} variant="contained" onClick={handleAddRoute}>Add</Button>
        </Paper>
      </Grid>

      <Grid item xs={12} md={6}>
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6">Find Shortest Route</Typography>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12} sm={6}><TextField fullWidth label="From" value={findSrc} onChange={(e) => setFindSrc(e.target.value)} /></Grid>
            <Grid item xs={12} sm={6}><TextField fullWidth label="To" value={findDest} onChange={(e) => setFindDest(e.target.value)} /></Grid>
          </Grid>
          <Button sx={{ mt: 2 }} variant="contained" onClick={handleFindRoute}>Find</Button>
          <Divider sx={{ my: 2 }} />
          {result && (
            <>
              <Typography variant="subtitle1">Path: {Array.isArray(result.Path) ? result.Path.join(' → ') : 'N/A'}</Typography>
              <Typography variant="subtitle2">Distance: {result.Distance}</Typography>
            </>
          )}
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


