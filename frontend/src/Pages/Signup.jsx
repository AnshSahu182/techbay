import React, { useState } from "react";
import {
  Box,
  Paper,
  Typography,
  TextField,
  Button,
  IconButton,
  InputAdornment,
  Link,
} from "@mui/material";
import { Visibility, VisibilityOff } from "@mui/icons-material";
import { useNavigate } from "react-router-dom";

export default function Signup() {
  const navigate = useNavigate();
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const handleTogglePassword = () => setShowPassword(!showPassword);
  const handleToggleConfirmPassword = () =>
    setShowConfirmPassword(!showConfirmPassword);

  return (
    <Box
      sx={{
        minHeight: "100vh",
        display: "flex",
        flexDirection: "column",
        backgroundColor: "#f9fafb",
        fontFamily: "Inter, sans-serif",
      }}
    >
      
      <Box
        sx={{
          display: "flex",
          alignItems: "center",
          gap: 1,
          p: 1,
          pl: 2,
        }}
      >
        <Box
          component="svg"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 48 48"
          fill="none"
          sx={{ width: 30, height: 30, color: "#2563eb" }}
        >
          <path
            d="M24 45.8096C19.6865 45.8096 15.4698 44.5305 11.8832 42.134C8.29667 39.7376 5.50128 36.3314 3.85056 32.3462C2.19985 28.361 1.76794 23.9758 2.60947 19.7452C3.451 15.5145 5.52816 11.6284 8.57829 8.5783C11.6284 5.52817 15.5145 3.45101 19.7452 2.60948C23.9758 1.76795 28.361 2.19986 32.3462 3.85057C36.3314 5.50129 39.7376 8.29668 42.134 11.8833C44.5305 15.4698 45.8096 19.6865 45.8096 24L24 24L24 45.8096Z"
            fill="currentColor"
          ></path>
        </Box>
        <Typography
          sx={{
            fontSize: "1.2rem",
            fontWeight: 1000,
            color: "#111",
            fontFamily: "Inter, sans-serif",
          }}
        >
          Techbay
        </Typography>
      </Box>

      
      <Box
        sx={{
          flexGrow: 1,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          pb: 8,
        }}
      >
        <Paper
          elevation={3}
          sx={{
            width: 380,
            padding: 5,
            borderRadius: 4,
            textAlign: "center",
          }}
        >
          <Typography
            variant="h5"
            sx={{ mb: 2, fontWeight: 1000, fontFamily: "Inter, sans-serif" }}
          >
            Create an Account
          </Typography>

          <TextField
            label="Full Name"
            fullWidth
            variant="outlined"
            margin="normal"
            placeholder="Enter your full name"
          />

          <TextField
            label="Email Address"
            fullWidth
            variant="outlined"
            margin="normal"
            placeholder="Enter your email address"
          />

          <TextField
            label="Password"
            type={showPassword ? "text" : "password"}
            fullWidth
            variant="outlined"
            margin="normal"
            placeholder="Enter your password"
            InputProps={{
              endAdornment: (
                <InputAdornment position="end">
                  <IconButton onClick={handleTogglePassword} edge="end">
                    {showPassword ? <VisibilityOff /> : <Visibility />}
                  </IconButton>
                </InputAdornment>
              ),
            }}
          />

          <TextField
            label="Confirm Password"
            type={showConfirmPassword ? "text" : "password"}
            fullWidth
            variant="outlined"
            margin="normal"
            placeholder="Confirm your password"
            InputProps={{
              endAdornment: (
                <InputAdornment position="end">
                  <IconButton onClick={handleToggleConfirmPassword} edge="end">
                    {showConfirmPassword ? <VisibilityOff /> : <Visibility />}
                  </IconButton>
                </InputAdornment>
              ),
            }}
          />

          <Button
            variant="contained"
            fullWidth
            sx={{
              mt: 3,
              py: 1.2,
              backgroundColor: "#007bff",
              textTransform: "none",
              fontWeight: 600,
              borderRadius: 2,
              fontFamily: "Inter, sans-serif",
              "&:hover": {
                backgroundColor: "#0069e0",
              },
            }}
          >
            Sign Up
          </Button>

          <Typography
            sx={{
              mt: 3,
              fontSize: 14,
              fontFamily: "Inter, sans-serif",
            }}
          >
            Already have an account?{" "}
            <Link
              underline="hover"
              sx={{ cursor: "pointer" }}
              onClick={() => navigate("/login")}
            >
              Sign In
            </Link>
          </Typography>
        </Paper>
      </Box>
    </Box>
  );
}
