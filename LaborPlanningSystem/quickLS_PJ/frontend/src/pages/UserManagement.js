import React, { useState, useEffect } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { Button, TextField, Select, MenuItem, Box } from '@mui/material';
import axios from 'axios';

const UserManagement = () => {
  const [users, setUsers] = useState([]);
  const [newUser, setNewUser] = useState({
    username: '',
    password: '',
    role: 'manager'
  });

  // Fetch users
  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const response = await axios.get('/api/users', {
          headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
        });
        setUsers(response.data);
      } catch (error) {
        console.error('Error fetching users:', error);
      }
    };
    fetchUsers();
  }, []);

  // Add user
  const handleAddUser = async () => {
    try {
      await axios.post('/api/users', newUser, {
        headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
      });
      setUsers([...users, newUser.username]);
      setNewUser({ username: '', password: '', role: 'manager' });
    } catch (error) {
      console.error('Error adding user:', error);
    }
  };

  // Delete user
  const handleDeleteUser = async (username) => {
    try {
      await axios.delete(`/api/users/${username}`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
      });
      setUsers(users.filter(user => user !== username));
    } catch (error) {
      console.error('Error deleting user:', error);
    }
  };

  const columns = [
    { field: 'username', headerName: 'Username', width: 200 },
    {
      field: 'actions',
      headerName: 'Actions',
      width: 150,
      renderCell: (params) => (
        <Button
          color="error"
          onClick={() => handleDeleteUser(params.row.username)}
        >
          Delete
        </Button>
      )
    }
  ];

  return (
    <Box sx={{ height: 600, width: '100%' }}>
      <Box sx={{ mb: 2 }}>
        <TextField
          label="Username"
          value={newUser.username}
          onChange={(e) => setNewUser({ ...newUser, username: e.target.value })}
          sx={{ mr: 2 }}
        />
        <TextField
          label="Password"
          type="password"
          value={newUser.password}
          onChange={(e) => setNewUser({ ...newUser, password: e.target.value })}
          sx={{ mr: 2 }}
        />
        <Select
          value={newUser.role}
          onChange={(e) => setNewUser({ ...newUser, role: e.target.value })}
          sx={{ mr: 2 }}
        >
          <MenuItem value="manager">Manager</MenuItem>
          <MenuItem value="admin">Admin</MenuItem>
        </Select>
        <Button variant="contained" onClick={handleAddUser}>
          Add User
        </Button>
      </Box>
      <DataGrid
        rows={users.map(username => ({ username }))}
        columns={columns}
        pageSize={10}
        rowsPerPageOptions={[10]}
        getRowId={(row) => row.username}
      />
    </Box>
  );
};

export default UserManagement;