import React from 'react'
import AppBar from '@mui/material/AppBar'
import Toolbar from '@mui/material/Toolbar'
import Typography from '@mui/material/Typography'
import Button from '@mui/material/Button'
import { Link, useLocation } from 'react-router-dom'

export default function NavBar() {
  const location = useLocation()
  const isActive = (path) => location.pathname === path

  return (
    <AppBar position="static" color="primary">
      <Toolbar>
        <Typography variant="h6" sx={{ flexGrow: 1 }}>
          Airport Runway Scheduler
        </Typography>
        <Button component={Link} to="/flights" color={isActive('/flights') ? 'secondary' : 'inherit'}>
          Flights
        </Button>
        <Button component={Link} to="/runways" color={isActive('/runways') ? 'secondary' : 'inherit'}>
          Runways
        </Button>
        <Button component={Link} to="/routes" color={isActive('/routes') ? 'secondary' : 'inherit'}>
          Routes
        </Button>
      </Toolbar>
    </AppBar>
  )
}

