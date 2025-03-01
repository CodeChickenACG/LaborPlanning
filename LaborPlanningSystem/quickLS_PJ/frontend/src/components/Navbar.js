import React from 'react';
import { AppBar, Toolbar, Button } from '@mui/material';
import { Link, useNavigate } from 'react-router-dom';

const Navbar = ({ user, setUser }) => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('role');
    setUser(null);
    navigate('/login');
  };

  return (
    <AppBar position="static">
      <Toolbar>
        {user && (
          <>
            <Button color="inherit" component={Link} to="/">
              Associates
            </Button>
            {user.role === 'manager' && (
              <>
                <Button color="inherit" component={Link} to="/requests">
                  Labor Requests
                </Button>
                <Button color="inherit" component={Link} to="/assign">
                  Labor Assign
                </Button>
              </>
            )}
            {user.role === 'admin' && (
              <Button color="inherit" component={Link} to="/approvals">
                Approvals
              </Button>
            )}
            <Button color="inherit" onClick={handleLogout} sx={{ ml: 'auto' }}>
              Logout
            </Button>
          </>
        )}
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;