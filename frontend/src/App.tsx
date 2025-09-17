import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { Box } from '@mui/material';
import { motion, AnimatePresence } from 'framer-motion';

// Components
import Navbar from './components/Layout/Navbar';
import Sidebar from './components/Layout/Sidebar';
import LoadingScreen from './components/Common/LoadingScreen';

// Pages
import Dashboard from './pages/Dashboard';
import Login from './pages/Auth/Login';
import Register from './pages/Auth/Register';
import YouTubeDownloader from './pages/YouTube/YouTubeDownloader';
import YouTubeSearch from './pages/YouTube/YouTubeSearch';
import TorrentSearch from './pages/Torrent/TorrentSearch';
import MediaStreaming from './pages/Media/MediaStreaming';
import Downloads from './pages/Downloads/Downloads';
import Profile from './pages/Profile/Profile';
import Settings from './pages/Settings/Settings';

// Hooks
import { useAuth } from './hooks/useAuth';


const App: React.FC = () => {
  const { isAuthenticated, loading } = useAuth();

  // Add a timeout to prevent infinite loading
  const [showFallback, setShowFallback] = React.useState(false);
  
  React.useEffect(() => {
    const timer = setTimeout(() => {
      if (loading) {
        setShowFallback(true);
      }
    }, 3000);
    
    return () => clearTimeout(timer);
  }, [loading]);

  if (loading && !showFallback) {
    return <LoadingScreen />;
  }
  
  // If still loading after timeout, show login page as fallback
  if (showFallback) {
    return (
      <Box sx={{ width: '100%' }}>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
      </Box>
    );
  }

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh' }}>
      <AnimatePresence mode="wait">
        {isAuthenticated ? (
          <motion.div
            key="authenticated"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.3 }}
            style={{ display: 'flex', width: '100%' }}
          >
            <Sidebar />
            <Box sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
              <Navbar />
              <Box
                component="main"
                sx={{
                  flexGrow: 1,
                  p: 3,
                  backgroundColor: 'background.default',
                  minHeight: 'calc(100vh - 64px)',
                }}
              >
                <Routes>
                  <Route path="/dashboard" element={<Dashboard />} />
                  <Route path="/youtube/download" element={<YouTubeDownloader />} />
                  <Route path="/youtube/search" element={<YouTubeSearch />} />
                  <Route path="/torrent/search" element={<TorrentSearch />} />
                  <Route path="/media/streaming" element={<MediaStreaming />} />
                  <Route path="/downloads" element={<Downloads />} />
                  <Route path="/profile" element={<Profile />} />
                  <Route path="/settings" element={<Settings />} />
                  <Route path="/" element={<Navigate to="/dashboard" replace />} />
                  <Route path="*" element={<Navigate to="/dashboard" replace />} />
                </Routes>
              </Box>
            </Box>
          </motion.div>
        ) : (
          <motion.div
            key="unauthenticated"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.3 }}
            style={{ width: '100%' }}
          >
            <Routes>
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/" element={<Navigate to="/login" replace />} />
              <Route path="*" element={<Navigate to="/login" replace />} />
            </Routes>
          </motion.div>
        )}
      </AnimatePresence>
    </Box>
  );
};

export default App;
