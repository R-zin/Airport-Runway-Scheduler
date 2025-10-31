import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { createTheme, ThemeProvider, CssBaseline, Container } from '@mui/material'
import NavBar from './components/NavBar'
import Flights from './pages/Flights'
import Runways from './pages/Runways'
import RoutesPage from './pages/RoutesPage'

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: { main: '#1a73e8' },
    secondary: { main: '#00bfa5' }
  },
  shape: { borderRadius: 10 }
})

export default function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <NavBar />
      <Container maxWidth="lg" sx={{ mt: 4, mb: 6 }}>
        <Routes>
          <Route path="/" element={<Navigate to="/flights" replace />} />
          <Route path="/flights" element={<Flights />} />
          <Route path="/runways" element={<Runways />} />
          <Route path="/routes" element={<RoutesPage />} />
          <Route path="*" element={<Navigate to="/flights" replace />} />
        </Routes>
      </Container>
    </ThemeProvider>
  )
}

