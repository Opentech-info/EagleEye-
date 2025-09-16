import React from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  LinearProgress,
  Chip,
  Avatar,
  IconButton,
} from '@mui/material';
import {
  CloudDownload,
  PlayCircle,
  Search,
  Download,
  TrendingUp,
  Speed,
  Storage,
  Refresh,
} from '@mui/icons-material';
import { motion } from 'framer-motion';
import { useAuth } from '../hooks/useAuth';
import { useDownloads } from '../hooks/useDownloads';
import { useNavigate } from 'react-router-dom';

const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const { downloads, isLoading, refetch } = useDownloads();
  const navigate = useNavigate();

  const recentDownloads = downloads.slice(0, 5);
  const completedDownloads = downloads.filter(d => d.status === 'completed').length;
  const activeDownloads = downloads.filter(d => d.status === 'downloading' || d.status === 'pending').length;

  const quickActions = [
    {
      title: 'YouTube Download',
      description: 'Download videos from YouTube',
      icon: <CloudDownload />,
      color: '#f44336',
      path: '/youtube/download',
    },
    {
      title: 'Search YouTube',
      description: 'Search and preview videos',
      icon: <Search />,
      color: '#2196f3',
      path: '/youtube/search',
    },
    {
      title: 'Media Streaming',
      description: 'Stream videos and audio',
      icon: <PlayCircle />,
      color: '#4caf50',
      path: '/media/streaming',
    },
    {
      title: 'View Downloads',
      description: 'Manage your downloads',
      icon: <Download />,
      color: '#ff9800',
      path: '/downloads',
    },
  ];

  const stats = [
    {
      title: 'Total Downloads',
      value: downloads.length,
      icon: <Download />,
      color: '#667eea',
    },
    {
      title: 'Completed',
      value: completedDownloads,
      icon: <TrendingUp />,
      color: '#4caf50',
    },
    {
      title: 'Active',
      value: activeDownloads,
      icon: <Speed />,
      color: '#ff9800',
    },
    {
      title: 'Storage Used',
      value: '2.4 GB',
      icon: <Storage />,
      color: '#9c27b0',
    },
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'success';
      case 'downloading':
        return 'primary';
      case 'pending':
        return 'warning';
      case 'failed':
        return 'error';
      default:
        return 'default';
    }
  };

  return (
    <Box sx={{ p: 3 }}>
      {/* Welcome Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <Box sx={{ mb: 4 }}>
          <Typography variant="h4" sx={{ fontWeight: 'bold', mb: 1 }}>
            Welcome back, {user?.username}! 👋
          </Typography>
          <Typography variant="body1" sx={{ opacity: 0.7 }}>
            Manage your media downloads and streaming from your dashboard
          </Typography>
        </Box>
      </motion.div>

      {/* Stats Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {stats.map((stat, index) => (
          <Grid item xs={12} sm={6} md={3} key={stat.title}>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
            >
              <Card
                sx={{
                  background: 'linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%)',
                  backdropFilter: 'blur(10px)',
                  border: '1px solid rgba(255,255,255,0.1)',
                }}
              >
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                    <Box>
                      <Typography variant="h4" sx={{ fontWeight: 'bold', mb: 1 }}>
                        {stat.value}
                      </Typography>
                      <Typography variant="body2" sx={{ opacity: 0.7 }}>
                        {stat.title}
                      </Typography>
                    </Box>
                    <Avatar
                      sx={{
                        backgroundColor: stat.color,
                        width: 56,
                        height: 56,
                      }}
                    >
                      {stat.icon}
                    </Avatar>
                  </Box>
                </CardContent>
              </Card>
            </motion.div>
          </Grid>
        ))}
      </Grid>

      <Grid container spacing={3}>
        {/* Quick Actions */}
        <Grid item xs={12} md={8}>
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
          >
            <Card
              sx={{
                background: 'linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%)',
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(255,255,255,0.1)',
                mb: 3,
              }}
            >
              <CardContent>
                <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 3 }}>
                  Quick Actions
                </Typography>
                <Grid container spacing={2}>
                  {quickActions.map((action, index) => (
                    <Grid item xs={12} sm={6} key={action.title}>
                      <motion.div
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                      >
                        <Card
                          sx={{
                            cursor: 'pointer',
                            background: 'rgba(255,255,255,0.05)',
                            border: '1px solid rgba(255,255,255,0.1)',
                            '&:hover': {
                              background: 'rgba(255,255,255,0.1)',
                            },
                          }}
                          onClick={() => navigate(action.path)}
                        >
                          <CardContent sx={{ p: 2 }}>
                            <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                              <Avatar
                                sx={{
                                  backgroundColor: action.color,
                                  width: 32,
                                  height: 32,
                                  mr: 2,
                                }}
                              >
                                {action.icon}
                              </Avatar>
                              <Typography variant="subtitle1" sx={{ fontWeight: 'bold' }}>
                                {action.title}
                              </Typography>
                            </Box>
                            <Typography variant="body2" sx={{ opacity: 0.7 }}>
                              {action.description}
                            </Typography>
                          </CardContent>
                        </Card>
                      </motion.div>
                    </Grid>
                  ))}
                </Grid>
              </CardContent>
            </Card>
          </motion.div>

          {/* Recent Downloads */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
          >
            <Card
              sx={{
                background: 'linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%)',
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(255,255,255,0.1)',
              }}
            >
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 3 }}>
                  <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
                    Recent Downloads
                  </Typography>
                  <IconButton onClick={() => refetch()} disabled={isLoading}>
                    <Refresh />
                  </IconButton>
                </Box>
                {recentDownloads.length > 0 ? (
                  <Box>
                    {recentDownloads.map((download) => (
                      <Box
                        key={download.id}
                        sx={{
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'space-between',
                          p: 2,
                          mb: 1,
                          borderRadius: 1,
                          background: 'rgba(255,255,255,0.05)',
                          border: '1px solid rgba(255,255,255,0.1)',
                        }}
                      >
                        <Box sx={{ flex: 1 }}>
                          <Typography variant="subtitle2" sx={{ fontWeight: 'bold' }}>
                            {download.title || 'Unknown Title'}
                          </Typography>
                          <Typography variant="caption" sx={{ opacity: 0.7 }}>
                            {new Date(download.created_at).toLocaleDateString()}
                          </Typography>
                          {download.status === 'downloading' && (
                            <LinearProgress
                              variant="determinate"
                              value={download.progress * 100}
                              sx={{ mt: 1 }}
                            />
                          )}
                        </Box>
                        <Chip
                          label={download.status}
                          color={getStatusColor(download.status) as any}
                          size="small"
                          sx={{ ml: 2 }}
                        />
                      </Box>
                    ))}
                    <Button
                      fullWidth
                      variant="outlined"
                      onClick={() => navigate('/downloads')}
                      sx={{ mt: 2 }}
                    >
                      View All Downloads
                    </Button>
                  </Box>
                ) : (
                  <Box sx={{ textAlign: 'center', py: 4 }}>
                    <Typography variant="body2" sx={{ opacity: 0.7 }}>
                      No downloads yet. Start by downloading some videos!
                    </Typography>
                    <Button
                      variant="contained"
                      onClick={() => navigate('/youtube/download')}
                      sx={{ mt: 2 }}
                    >
                      Start Downloading
                    </Button>
                  </Box>
                )}
              </CardContent>
            </Card>
          </motion.div>
        </Grid>

        {/* System Info */}
        <Grid item xs={12} md={4}>
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.5 }}
          >
            <Card
              sx={{
                background: 'linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%)',
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(255,255,255,0.1)',
              }}
            >
              <CardContent>
                <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 3 }}>
                  System Status
                </Typography>
                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2" sx={{ opacity: 0.7, mb: 1 }}>
                    Server Status
                  </Typography>
                  <Chip label="Online" color="success" size="small" />
                </Box>
                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2" sx={{ opacity: 0.7, mb: 1 }}>
                    Version
                  </Typography>
                  <Typography variant="body2">EagleEye v2.0.0</Typography>
                </Box>
                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2" sx={{ opacity: 0.7, mb: 1 }}>
                    Last Updated
                  </Typography>
                  <Typography variant="body2">
                    {new Date().toLocaleDateString()}
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          </motion.div>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;
