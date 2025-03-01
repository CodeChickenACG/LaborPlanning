import React, { useState } from 'react';
import {
  Box,
  Button,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Chip,
  Grid
} from '@mui/material';
import axios from 'axios';

const TempChangeRequest = () => {
  const [formData, setFormData] = useState({
    change_type: 'add',
    login_id: '',
    name: '',
    permissions: [],
    requested_by: ''
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:5000/temp-changes', formData);
      alert('Request submitted successfully!');
      setFormData({
        change_type: 'add',
        login_id: '',
        name: '',
        permissions: [],
        requested_by: ''
      });
    } catch (error) {
      alert('Error submitting request: ' + error.response.data.error);
    }
  };

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ mt: 3 }}>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <FormControl fullWidth>
            <InputLabel>Change Type</InputLabel>
            <Select
              value={formData.change_type}
              onChange={(e) => setFormData({...formData, change_type: e.target.value})}
            >
              <MenuItem value="add">Add Associate</MenuItem>
              <MenuItem value="remove">Remove Associate</MenuItem>
            </Select>
          </FormControl>
        </Grid>

        <Grid item xs={12}>
          <TextField
            fullWidth
            label="Login ID"
            value={formData.login_id}
            onChange={(e) => setFormData({...formData, login_id: e.target.value})}
            required
          />
        </Grid>

        {formData.change_type === 'add' && (
          <>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Name"
                value={formData.name}
                onChange={(e) => setFormData({...formData, name: e.target.value})}
                required
              />
            </Grid>
            <Grid item xs={12}>
              <FormControl fullWidth>
                <InputLabel>Permissions</InputLabel>
                <Select
                  multiple
                  value={formData.permissions}
                  onChange={(e) => setFormData({...formData, permissions: e.target.value})}
                  renderValue={(selected) => (
                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                      {selected.map((value) => (
                        <Chip key={value} label={value} />
                      ))}
                    </Box>
                  )}
                >
                  {['Stow', 'TTB', 'Pick', 'Pack', 'ProblemSolve'].map((perm) => (
                    <MenuItem key={perm} value={perm}>{perm}</MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
          </>
        )}

        <Grid item xs={12}>
          <TextField
            fullWidth
            label="Requested By"
            value={formData.requested_by}
            onChange={(e) => setFormData({...formData, requested_by: e.target.value})}
            required
          />
        </Grid>

        <Grid item xs={12}>
          <Button type="submit" variant="contained" color="primary">
            Submit Request
          </Button>
        </Grid>
      </Grid>
    </Box>
  );
};

export default TempChangeRequest;