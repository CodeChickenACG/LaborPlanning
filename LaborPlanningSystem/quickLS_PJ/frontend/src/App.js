import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { CssBaseline, Container } from '@mui/material';
import Navbar from './components/Navbar';
import Login from './components/Login';
import Associates from './pages/Associates';
import LaborRequests from './pages/LaborRequests';
import LaborAssign from './pages/LaborAssign';  // Add this line
import Approvals from './pages/Approvals';
import UserManagement from './pages/UserManagement';

function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    const role = localStorage.getItem('role');
    if (token && role) {
      setUser({ role });
    }
  }, []);

  const ProtectedRoute = ({ children, requiredRole }) => {
    if (!user) {
      return <Navigate to="/login" />;
    }
    if (requiredRole && user.role !== requiredRole) {
      return <Navigate to="/" />;
    }
    return children;
  };

  return (
    <Router>
      <CssBaseline />
      <Navbar user={user} setUser={setUser} />
      <Container maxWidth="lg" sx={{ mt: 4 }}>
        <Routes>
          <Route path="/login" element={<Login setUser={setUser} />} />
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <Associates />
              </ProtectedRoute>
            }
          />
          <Route
            path="/requests"
            element={
              <ProtectedRoute requiredRole="manager">
                <LaborRequests />
              </ProtectedRoute>
            }
          />
          <Route
            path="/assign"
            element={
              <ProtectedRoute requiredRole="manager">
                <LaborAssign />
              </ProtectedRoute>
            }
          />
          <Route
            path="/approvals"
            element={
              <ProtectedRoute requiredRole="admin">
                <Approvals />
              </ProtectedRoute>
            }
          />
          <Route
            path="/users"
            element={
              <ProtectedRoute requiredRole="admin">
                <UserManagement />
              </ProtectedRoute>
            }
          />
        </Routes>
      </Container>
    </Router>
  );
}

export default App;