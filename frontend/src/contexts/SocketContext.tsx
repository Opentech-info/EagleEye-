import React, { createContext, useContext, useEffect, useState, useRef } from 'react';
import { io, Socket } from 'socket.io-client';
import { useAuth } from '../hooks/useAuth';
import toast from 'react-hot-toast';

interface SocketContextType {
  socket: Socket | null;
  isConnected: boolean;
}

const SocketContext = createContext<SocketContextType | undefined>(undefined);

export const SocketProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [socket, setSocket] = useState<Socket | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const { isAuthenticated, token } = useAuth();
  const socketRef = useRef<Socket | null>(null);

  useEffect(() => {
    if (isAuthenticated && token) {
      // Create socket connection with error handling
      try {
        const newSocket = io('http://localhost:5000', {
          auth: {
            token,
          },
          transports: ['websocket'],
          timeout: 5000, // Add timeout
          reconnection: true,
          reconnectionAttempts: 3,
          reconnectionDelay: 1000,
        });

        // Connection event handlers
        newSocket.on('connect', () => {
          setIsConnected(true);
          console.log('Connected to server');
        });

        newSocket.on('disconnect', () => {
          setIsConnected(false);
          console.log('Disconnected from server');
        });

        newSocket.on('connect_error', (error) => {
          console.error('Connection error:', error);
          setIsConnected(false);
        });

        // Download progress events
        newSocket.on('download_progress', (data) => {
          // Handle download progress updates
          console.log('Download progress:', data);
          // You can dispatch this to a downloads context or state management
        });

        newSocket.on('download_complete', (data) => {
          toast.success(`Download completed: ${data.file_path}`);
          console.log('Download completed:', data);
        });

        newSocket.on('download_error', (data) => {
          toast.error(`Download failed: ${data.error}`);
          console.error('Download error:', data);
        });

        // Server status updates
        newSocket.on('status', (data) => {
          console.log('Server status:', data);
        });

        socketRef.current = newSocket;
        setSocket(newSocket);

        // Cleanup on unmount or auth change
        return () => {
          newSocket.close();
          socketRef.current = null;
          setSocket(null);
          setIsConnected(false);
        };
      } catch (error) {
        console.error('Failed to create socket connection:', error);
        // Don't block the app if socket fails
      }
    } else {
      // Disconnect if not authenticated
      if (socketRef.current) {
        socketRef.current.close();
        socketRef.current = null;
        setSocket(null);
        setIsConnected(false);
      }
    }
  }, [isAuthenticated, token]);

  const value: SocketContextType = {
    socket,
    isConnected,
  };

  return <SocketContext.Provider value={value}>{children}</SocketContext.Provider>;
};

export const useSocket = (): SocketContextType => {
  const context = useContext(SocketContext);
  if (context === undefined) {
    throw new Error('useSocket must be used within a SocketProvider');
  }
  return context;
};
