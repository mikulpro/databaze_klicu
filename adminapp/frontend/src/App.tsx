import React, { useState } from 'react';
import logo from './logo.svg';
import {
  Container,
  TextField,
  Typography,
  Button,
  Box,
  Grid,
} from "@mui/material";
import './App.css';

interface LoginState {
  email: string;
  password: string;
}

const App: React.FC = () => {
  const [loginState, setLoginState] = useState<LoginState>({
    email: "",
    password: "",
  });

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;
    setLoginState((prevState) => ({ ...prevState, [name]: value }));
  };

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    console.log("Email:", loginState.email, "Password:", loginState.password);
    // Perform authentication here
  };

  return (
    <Container maxWidth="xs">
      <Box className="container">
        <Typography component="h1" variant="h5">
          Login
        </Typography>
        <Box component="form" onSubmit={handleSubmit} className="form">
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <TextField
                required
                fullWidth
                label="Email Address"
                name="email"
                value={loginState.email}
                onChange={handleChange}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                required
                fullWidth
                type="password"
                label="Password"
                name="password"
                value={loginState.password}
                onChange={handleChange}
              />
            </Grid>
            <Grid item xs={12}>
              <Button
                type="submit"
                fullWidth
                variant="contained"
                color="primary"
              >
                Sign In
              </Button>
            </Grid>
          </Grid>
        </Box>
      </Box>
    </Container>
  );
};

export default App;
