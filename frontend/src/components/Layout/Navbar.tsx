import React from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  IconButton,
  Avatar,
  Menu,
  MenuItem,
  Box,
  Badge,
  Tooltip,
} from '@mui/material';
import {
  Notifications,
  AccountCircle,
  Settings,
  Logout,
  Download,
} from '@mui/icons-material';
import { motion } from 'framer-motion';
import { useAuth } from '../../hooks/useAuth';
import { useSocket } from '../../contexts/SocketContext';
import { useDownloads } from '../../hooks/useDownloads';

const Navbar: React.FC = () => {
  const { user, logout } = useAuth();
  const { isConnected } = useSocket();
  const { downloads } = useDownloads();
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);

  const activeDownloads = downloads.filter(
    (download) => download.status === 'downloading' || download.status === 'pending'
  ).length;

  const handleMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    logout();
    handleClose();
  };

  return (
    <AppBar
      position="static"
      sx={{
        backgroundColor: 'rgba(26, 29, 58, 0.95)',
        backdropFilter: 'blur(10px)',
        borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
        boxShadow: 'none',
      }}
    >
      <Toolbar>
        {/* App Title */}
        <Typography
          variant="h6"
          component="div"
          sx={{
            flexGrow: 1,
            fontWeight: 'bold',
            background: 'linear-gradient(45deg, #667eea, #764ba2)',
            backgroundClip: 'text',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
          }}
        >
          EagleEye
        </Typography>

        {/* Connection Status */}
        <Box sx={{ display: 'flex', alignItems: 'center', mr: 2 }}>
          <motion.div
            animate={{ scale: isConnected ? 1 : 0.8 }}
            transition={{ duration: 0.3 }}
          >
            <Box
              sx={{
                width: 8,
                height: 8,
                borderRadius: '50%',
                backgroundColor: isConnected ? '#4caf50' : '#f44336',
                mr: 1,
              }}
            />
          </motion.div>
          <Typography variant="caption" sx={{ opacity: 0.7 }}>
            {isConnected ? 'Connected' : 'Disconnected'}
          </Typography>
        </Box>

        {/* Downloads Badge */}
        <Tooltip title={`${activeDownloads} active downloads`}>
          <IconButton color="inherit" sx={{ mr: 1 }}>
            <Badge badgeContent={activeDownloads} color="secondary">
              <Download />
            </Badge>
          </IconButton>
        </Tooltip>

        {/* Notifications */}
        <Tooltip title="Notifications">
          <IconButton color="inherit" sx={{ mr: 1 }}>
            <Badge badgeContent={0} color="secondary">
              <Notifications />
            </Badge>
          </IconButton>
        </Tooltip>

        {/* User Menu */}
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <Typography variant="body2" sx={{ mr: 2, opacity: 0.8 }}>
            {user?.username}
          </Typography>
          <IconButton
            size="large"
            aria-label="account of current user"
            aria-controls="menu-appbar"
            aria-haspopup="true"
            onClick={handleMenu}
            color="inherit"
          >
            <Avatar
              sx={{
                width: 32,
                height: 32,
                background: 'linear-gradient(45deg, #667eea, #764ba2)',
              }}
            >
              {user?.username?.charAt(0).toUpperCase()}
            </Avatar>
          </IconButton>
          <Menu
            id="menu-appbar"
            anchorEl={anchorEl}
            anchorOrigin={{
              vertical: 'bottom',
              horizontal: 'right',
            }}
            keepMounted
            transformOrigin={{
              vertical: 'top',
              horizontal: 'right',
            }}
            open={Boolean(anchorEl)}
            onClose={handleClose}
            PaperProps={{
              sx: {
                backgroundColor: 'rgba(26, 29, 58, 0.95)',
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                mt: 1,
              },
            }}
          >
            <MenuItem onClick={handleClose}>
              <AccountCircle sx={{ mr: 2 }} />
              Profile
            </MenuItem>
            <MenuItem onClick={handleClose}>
              <Settings sx={{ mr: 2 }} />
              Settings
            </MenuItem>
            <MenuItem onClick={handleLogout}>
              <Logout sx={{ mr: 2 }} />
              Logout
            </MenuItem>
          </Menu>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
