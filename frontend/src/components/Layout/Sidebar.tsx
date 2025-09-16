import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import {
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Box,
  Typography,
  Divider,
} from '@mui/material';
import {
  Dashboard,
  Search,
  CloudDownload,
  PlayCircle,
  Download,
  Person,
  Settings,
  FileDownload,
} from '@mui/icons-material';
import { motion } from 'framer-motion';

const drawerWidth = 280;

interface MenuItem {
  text: string;
  icon: React.ReactElement;
  path: string;
  category?: string;
}

const menuItems: MenuItem[] = [
  { text: 'Dashboard', icon: <Dashboard />, path: '/dashboard' },
  { text: 'YouTube Download', icon: <CloudDownload />, path: '/youtube/download', category: 'YouTube' },
  { text: 'YouTube Search', icon: <Search />, path: '/youtube/search', category: 'YouTube' },
  { text: 'Torrent Search', icon: <FileDownload />, path: '/torrent/search', category: 'Torrent' },
  { text: 'Media Streaming', icon: <PlayCircle />, path: '/media/streaming', category: 'Media' },
  { text: 'Downloads', icon: <Download />, path: '/downloads' },
  { text: 'Profile', icon: <Person />, path: '/profile', category: 'Account' },
  { text: 'Settings', icon: <Settings />, path: '/settings', category: 'Account' },
];

const Sidebar: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();

  const handleNavigation = (path: string) => {
    navigate(path);
  };

  const renderMenuItems = () => {
    const groupedItems: { [key: string]: MenuItem[] } = {};
    const ungroupedItems: MenuItem[] = [];

    menuItems.forEach((item) => {
      if (item.category) {
        if (!groupedItems[item.category]) {
          groupedItems[item.category] = [];
        }
        groupedItems[item.category].push(item);
      } else {
        ungroupedItems.push(item);
      }
    });

    const renderItems = (items: MenuItem[], startIndex: number = 0) =>
      items.map((item, index) => {
        const isActive = location.pathname === item.path;
        const itemIndex = startIndex + index;

        return (
          <motion.div
            key={item.path}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: itemIndex * 0.1 }}
          >
            <ListItem disablePadding>
              <ListItemButton
                onClick={() => handleNavigation(item.path)}
                sx={{
                  mx: 1,
                  mb: 0.5,
                  borderRadius: 2,
                  backgroundColor: isActive
                    ? 'rgba(102, 126, 234, 0.2)'
                    : 'transparent',
                  border: isActive
                    ? '1px solid rgba(102, 126, 234, 0.3)'
                    : '1px solid transparent',
                  '&:hover': {
                    backgroundColor: isActive
                      ? 'rgba(102, 126, 234, 0.3)'
                      : 'rgba(255, 255, 255, 0.05)',
                  },
                  transition: 'all 0.2s ease-in-out',
                }}
              >
                <ListItemIcon
                  sx={{
                    color: isActive ? '#667eea' : 'rgba(255, 255, 255, 0.7)',
                    minWidth: 40,
                  }}
                >
                  {item.icon}
                </ListItemIcon>
                <ListItemText
                  primary={item.text}
                  sx={{
                    '& .MuiListItemText-primary': {
                      fontSize: '0.9rem',
                      fontWeight: isActive ? 600 : 400,
                      color: isActive ? '#667eea' : 'rgba(255, 255, 255, 0.9)',
                    },
                  }}
                />
              </ListItemButton>
            </ListItem>
          </motion.div>
        );
      });

    let currentIndex = 0;
    const result = [];

    // Render ungrouped items first
    result.push(...renderItems(ungroupedItems, currentIndex));
    currentIndex += ungroupedItems.length;

    // Render grouped items
    Object.entries(groupedItems).forEach(([category, items]) => {
      result.push(
        <motion.div
          key={category}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: currentIndex * 0.1 }}
        >
          <Divider sx={{ my: 2, mx: 2, borderColor: 'rgba(255, 255, 255, 0.1)' }} />
          <Typography
            variant="caption"
            sx={{
              px: 3,
              py: 1,
              display: 'block',
              color: 'rgba(255, 255, 255, 0.5)',
              fontWeight: 600,
              textTransform: 'uppercase',
              letterSpacing: 1,
            }}
          >
            {category}
          </Typography>
        </motion.div>
      );
      currentIndex++;

      result.push(...renderItems(items, currentIndex));
      currentIndex += items.length;
    });

    return result;
  };

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: drawerWidth,
          boxSizing: 'border-box',
          backgroundColor: 'rgba(26, 29, 58, 0.95)',
          backdropFilter: 'blur(10px)',
          border: 'none',
          borderRight: '1px solid rgba(255, 255, 255, 0.1)',
        },
      }}
    >
      {/* Logo Section */}
      <Box
        sx={{
          p: 3,
          display: 'flex',
          alignItems: 'center',
          borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
        }}
      >
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ type: 'spring', delay: 0.2 }}
        >
          <Box
            sx={{
              width: 40,
              height: 40,
              borderRadius: '50%',
              background: 'linear-gradient(45deg, #667eea, #764ba2)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              mr: 2,
            }}
          >
            <Typography variant="h6" sx={{ color: 'white', fontWeight: 'bold' }}>
              E
            </Typography>
          </Box>
        </motion.div>
        <Box>
          <Typography
            variant="h6"
            sx={{
              fontWeight: 'bold',
              background: 'linear-gradient(45deg, #667eea, #764ba2)',
              backgroundClip: 'text',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
            }}
          >
            EagleEye
          </Typography>
          <Typography variant="caption" sx={{ opacity: 0.7 }}>
            Media Management
          </Typography>
        </Box>
      </Box>

      {/* Navigation Menu */}
      <Box sx={{ overflow: 'auto', flex: 1, py: 2 }}>
        <List>{renderMenuItems()}</List>
      </Box>

      {/* Footer */}
      <Box
        sx={{
          p: 2,
          borderTop: '1px solid rgba(255, 255, 255, 0.1)',
          textAlign: 'center',
        }}
      >
        <Typography variant="caption" sx={{ opacity: 0.5 }}>
          EagleEye v2.0.0
        </Typography>
      </Box>
    </Drawer>
  );
};

export default Sidebar;
