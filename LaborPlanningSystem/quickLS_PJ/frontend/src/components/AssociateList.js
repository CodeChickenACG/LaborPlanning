import React, { useState, useEffect } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import axios from 'axios';

const AssociateList = () => {
  const [associates, setAssociates] = useState([]);

  // Fetch associates from Flask backend
  useEffect(() => {
    const fetchAssociates = async () => {
      try {
        const response = await axios.get('http://localhost:5000/associates');
        setAssociates(response.data);
      } catch (error) {
        console.error('Error fetching associates:', error);
      }
    };
    fetchAssociates();
  }, []);

  // Define table columns
  const columns = [
    { field: 'login_id', headerName: 'Login ID', width: 150 },
    { field: 'name', headerName: 'Name', width: 200 },
    {
      field: 'permissions',
      headerName: 'Permissions',
      width: 300,
      renderCell: (params) => params.value.join(', ')
    },
  ];

  return (
    <div style={{ height: 600, width: '100%' }}>
      <DataGrid
        rows={associates}
        columns={columns}
        pageSize={10}
        rowsPerPageOptions={[10]}
        getRowId={(row) => row.login_id}
      />
    </div>
  );
};

export default AssociateList;