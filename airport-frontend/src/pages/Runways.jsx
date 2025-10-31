import React, { useEffect, useState } from 'react'
import { Paper, Typography, Box, Grid, Button, Divider, Chip, Stack } from '@mui/material'
import { api } from '../api/client'

export default function Runways() {
  const [runways, setRunways] = useState([])

  const load = async () => {
    const res = await api.runwayStatus()
    setRunways(res.data || [])
  }

  useEffect(() => { load().catch(console.error) }, [])

  const clearDeparted = async () => {
    await api.clearDeparted()
    await load()
  }

  return (
    <Box>
      <Paper sx={{ p: 3, mb: 3 }}>
        <Stack direction="row" justifyContent="space-between" alignItems="center">
          <Typography variant="h6">Runway Status</Typography>
          <Button variant="outlined" onClick={clearDeparted}>Clear Departed</Button>
        </Stack>
        <Divider sx={{ my: 2 }} />
        <Grid container spacing={2}>
          {(runways || []).map((r, idx) => (
            <Grid item xs={12} sm={6} md={4} key={idx}>
              <Paper sx={{ p: 2 }}>
                <Typography variant="subtitle1">Runway {r.runway_no}</Typography>
                <Typography color={r.flight_no ? 'text.primary' : 'text.secondary'}>
                  {r.flight_no ? `Occupied by ${r.flight_no}` : 'Available'}
                </Typography>
              </Paper>
            </Grid>
          ))}
        </Grid>
      </Paper>
    </Box>
  )
}


