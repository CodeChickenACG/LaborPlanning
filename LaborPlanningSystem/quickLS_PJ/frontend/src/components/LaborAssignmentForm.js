import React, { useState } from 'react';
import { TextField, Button, Grid, Typography, Paper, Select, MenuItem, InputLabel, FormControl, Box, List, ListItem, ListItemText, IconButton } from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import axios from 'axios';

const LaborAssignmentForm = () => {
  const [logins, setLogins] = useState('');
  const [selectedPath, setSelectedPath] = useState('');
  const [numNeeded, setNumNeeded] = useState('');
  const [requirements, setRequirements] = useState([]);
  const [assignments, setAssignments] = useState(null);
  const [unassigned, setUnassigned] = useState([]);
  const [error, setError] = useState('');

  // Example list of paths (you can fetch this from the backend if needed)
  const paths = ['pick', 'ttb', 'pack', 'ship', 'receive'];

  const handleAddRequirement = () => {
    if (selectedPath && numNeeded) {
      setRequirements([...requirements, { path: selectedPath, num: parseInt(numNeeded, 10) }]);
      setSelectedPath('');
      setNumNeeded('');
    }
  };

  const handleRemoveRequirement = (index) => {
    const updatedRequirements = requirements.filter((_, i) => i !== index);
    setRequirements(updatedRequirements);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Parse logins
    const loginList = logins.split('\n').map(login => login.trim()).filter(login => login);

    // Convert requirements to a dictionary
    const requirementsDict = requirements.reduce((acc, req) => {
      acc[req.path] = req.num;
      return acc;
    }, {});

    try {
      const response = await axios.post('http://localhost:5000/assign-labor', {
        logins: loginList,
        requirements: requirementsDict,
      });
      setAssignments(response.data.assignments);
      setUnassigned(response.data.unassigned);
      setError('');
    } catch (err) {
      setError('Failed to assign labor. Please check your input and try again.');
      console.error(err);
    }
  };

  return (
    <Paper elevation={3} sx={{ p: 3, mt: 4 }}>
      <Typography variant="h5" gutterBottom>
        Assign Labor
      </Typography>
      <form onSubmit={handleSubmit}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <TextField
              label="Logins (one per line)"
              multiline
              rows={4}
              fullWidth
              value={logins}
              onChange={(e) => setLogins(e.target.value)}
              required
            />
          </Grid>
          <Grid item xs={6}>
            <FormControl fullWidth>
              <InputLabel>Select Path</InputLabel>
              <Select
                value={selectedPath}
                onChange={(e) => setSelectedPath(e.target.value)}
                label="Select Path"
                required
              >
                {paths.map((path, index) => (
                  <MenuItem key={index} value={path}>
                    {path}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={4}>
            <TextField
              label="Number Needed"
              type="number"
              fullWidth
              value={numNeeded}
              onChange={(e) => setNumNeeded(e.target.value)}
              required
            />
          </Grid>
          <Grid item xs={2}>
            <Button
              variant="contained"
              color="primary"
              onClick={handleAddRequirement}
              sx={{ height: '100%' }}
            >
              Add
            </Button>
          </Grid>
          <Grid item xs={12}>
            <Typography variant="h6">Selected Requirements</Typography>
            <List>
              {requirements.map((req, index) => (
                <ListItem
                  key={index}
                  secondaryAction={
                    <IconButton edge="end" onClick={() => handleRemoveRequirement(index)}>
                      <DeleteIcon />
                    </IconButton>
                  }
                >
                  <ListItemText primary={`${req.path}: ${req.num}`} />
                </ListItem>
              ))}
            </List>
          </Grid>
          <Grid item xs={12}>
            <Button type="submit" variant="contained" color="primary">
              Assign Labor
            </Button>
          </Grid>
        </Grid>
      </form>

      {error && <Typography color="error" sx={{ mt: 2 }}>{error}</Typography>}

      {assignments && (
        <Box sx={{ mt: 3 }}>
          <Typography variant="h6">Assignments</Typography>
          <pre>{JSON.stringify(assignments, null, 2)}</pre>
        </Box>
      )}

      {unassigned.length > 0 && (
        <Box sx={{ mt: 3 }}>
          <Typography variant="h6">Unassigned Logins</Typography>
          <ul>
            {unassigned.map((login, index) => (
              <li key={index}>{login}</li>
            ))}
          </ul>
        </Box>
      )}
    </Paper>
  );
};

export default LaborAssignmentForm;