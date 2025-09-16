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

// Types
interface ProtectedRouteProps {
  children: React.ReactNode;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return <LoadingScreen />;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
};

const PublicRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return <LoadingScreen />;
  }

  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }

  return <>{children}</>;
};

const App: React.FC = () => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return <LoadingScreen />;
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
                  <Route
                    path="/dashboard"
                    element={
                      <ProtectedRoute>
                        <Dashboard />
                      </ProtectedRoute>
                    }
                  />
                  <Route
                    path="/youtube/download"
                    element={
                      <ProtectedRoute>
                        <YouTubeDownloader />
                      </ProtectedRoute>
                    }
                  />
                  <Route
                    path="/youtube/search"
                    element={
                      <ProtectedRoute>
                        <YouTubeSearch />
                      </ProtectedRoute>
                    }
                  />
                  <Route
                    path="/torrent/search"
                    element={
                      <ProtectedRoute>
                        <TorrentSearch />
                      </ProtectedRoute>
                    }
                  />
                  <Route
                    path="/media/streaming"
                    element={
                      <ProtectedRoute>
                        <MediaStreaming />
                      </ProtectedRoute>
                    }
                  />
                  <Route
                    path="/downloads"
                    element={
                      <ProtectedRoute>
                        <Downloads />
                      </ProtectedRoute>
                    }
                  />
                  <Route
                    path="/profile"
                    element={
                      <ProtectedRoute>
                        <Profile />
                      </ProtectedRoute>
                    }
                  />
                  <Route
                    path="/settings"
                    element={
                      <ProtectedRoute>
                        <Settings />
                      </ProtectedRoute>
                    }
                  />
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
              <Route
                path="/login"
                element={
                  <PublicRoute>
                    <Login />
                  </PublicRoute>
                }
              />
              <Route
                path="/register"
                element={
                  <PublicRoute>
                    <Register />
                  </PublicRoute>
                }
              />
              <Route path="*" element={<Navigate to="/login" replace />} />
            </Routes>
          </motion.div>
        )}
      </AnimatePresence>
    </Box>
  );
};

export default App;
