import React, { useState, useEffect } from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Button,
  Chip
} from '@mui/material';
import axios from 'axios';

const PendingChanges = () => {
  const [pendingChanges, setPendingChanges] = useState([]);

  // Fetch pending changes from Flask backend
  useEffect(() => {
    const fetchPendingChanges = async () => {
      try {
        const response = await axios.get('http://localhost:5000/temp-changes/pending');
        setPendingChanges(response.data);
      } catch (error) {
        console.error('Error fetching pending changes:', error);
      }
    };
    fetchPendingChanges();
  }, []);

  // Handle approve/reject actions
  const handleAction = async (changeId, action) => {
    try {
      await axios.post(`http://localhost:5000/temp-changes/${changeId}/${action}`);
      setPendingChanges(pendingChanges.filter(change => change.id !== changeId));
      alert(`Change ${action}d successfully!`);
    } catch (error) {
      alert(`Error ${action}ing change: ${error.response.data.error}`);
    }
  };

  return (
    <TableContainer component={Paper}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Change Type</TableCell>
            <TableCell>Login ID</TableCell>
            <TableCell>Requested By</TableCell>
            <TableCell>Expires At</TableCell>
            <TableCell>Actions</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {pendingChanges.map((change) => (
            <TableRow key={change.id}>
              <TableCell>
                <Chip
                  label={change.change_type}
                  color={change.change_type === 'add' ? 'success' : 'error'}
                />
              </TableCell>
              <TableCell>{change.login_id}</TableCell>
              <TableCell>{change.requested_by}</TableCell>
              <TableCell>{new Date(change.expires_at).toLocaleString()}</TableCell>
              <TableCell>
                <Button
                  variant="contained"
                  color="success"
                  onClick={() => handleAction(change.id, 'approve')}
                  sx={{ mr: 1 }}
                >
                  Approve
                </Button>
                <Button
                  variant="outlined"
                  color="error"
                  onClick={() => handleAction(change.id, 'reject')}
                >
                  Reject
                </Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default PendingChanges;