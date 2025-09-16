import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  TextField,
  Button,
  Typography,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
  LinearProgress,
} from '@mui/material';
import { CloudDownload, Info } from '@mui/icons-material';
import { motion } from 'framer-motion';
import { useForm } from 'react-hook-form';
import { youtubeAPI } from '../../services/api';
import toast from 'react-hot-toast';

interface DownloadFormData {
  url: string;
  quality: string;
  type: 'video' | 'audio' | 'video+audio';
}

const YouTubeDownloader: React.FC = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [videoInfo, setVideoInfo] = useState<any>(null);
  const [downloadProgress, setDownloadProgress] = useState(0);

  const {
    register,
    handleSubmit,
    formState: { errors },
    watch,
  } = useForm<DownloadFormData>({
    defaultValues: {
      quality: '1080p',
      type: 'video+audio',
    },
  });

  const url = watch('url');

  const getVideoInfo = async () => {
    if (!url) return;

    setIsLoading(true);
    try {
      const response = await youtubeAPI.getVideoInfo(url);
      if (response.data.success) {
        setVideoInfo(response.data.info);
      } else {
        toast.error(response.data.error);
      }
    } catch (error: any) {
      toast.error(error.response?.data?.error || 'Failed to get video info');
    } finally {
      setIsLoading(false);
    }
  };

  const onSubmit = async (data: DownloadFormData) => {
    setIsLoading(true);
    setDownloadProgress(0);

    try {
      const response = await youtubeAPI.download(data);
      if (response.data.success) {
        // Create a direct download link
        const downloadUrl = response.data.download_url;
        const fileName = response.data.file_name;
        
        // Create a temporary anchor element to trigger browser download
        const link = document.createElement('a');
        link.href = downloadUrl;
        link.download = fileName;
        link.target = '_blank';
        
        // Trigger the download
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        toast.success('Download started successfully! Check your browser downloads.');
        
        // Reset progress after a delay
        setTimeout(() => {
          setDownloadProgress(0);
        }, 3000);
      } else {
        toast.error(response.data.error);
      }
    } catch (error: any) {
      toast.error(error.response?.data?.error || 'Download failed');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Box sx={{ maxWidth: 800, mx: 'auto' }}>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <Typography variant="h4" sx={{ fontWeight: 'bold', mb: 1 }}>
          YouTube Downloader
        </Typography>
        <Typography variant="body1" sx={{ opacity: 0.7, mb: 4 }}>
          Download videos and audio from YouTube with high quality
        </Typography>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
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
            <Box component="form" onSubmit={handleSubmit(onSubmit)}>
              <TextField
                fullWidth
                label="YouTube URL"
                placeholder="https://www.youtube.com/watch?v=..."
                {...register('url', {
                  required: 'URL is required',
                  pattern: {
                    value: /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/.+/,
                    message: 'Please enter a valid YouTube URL',
                  },
                })}
                error={!!errors.url}
                helperText={errors.url?.message}
                sx={{ mb: 3 }}
                InputProps={{
                  endAdornment: (
                    <Button
                      onClick={getVideoInfo}
                      disabled={!url || isLoading}
                      startIcon={<Info />}
                      sx={{ ml: 1 }}
                    >
                      Get Info
                    </Button>
                  ),
                }}
              />

              {videoInfo && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  transition={{ duration: 0.3 }}
                >
                  <Alert severity="info" sx={{ mb: 3 }}>
                    <Typography variant="subtitle2" sx={{ fontWeight: 'bold' }}>
                      {videoInfo.title}
                    </Typography>
                    <Typography variant="body2">
                      Duration: {Math.floor(videoInfo.duration / 60)}:{(videoInfo.duration % 60).toString().padStart(2, '0')} | 
                      Views: {videoInfo.view_count?.toLocaleString()} | 
                      Uploader: {videoInfo.uploader}
                    </Typography>
                  </Alert>
                </motion.div>
              )}

              <Box sx={{ display: 'flex', gap: 2, mb: 3 }}>
                <FormControl fullWidth>
                  <InputLabel>Download Type</InputLabel>
                  <Select
                    {...register('type')}
                    label="Download Type"
                    defaultValue="video+audio"
                  >
                    <MenuItem value="video+audio">Video + Audio</MenuItem>
                    <MenuItem value="video">Video Only</MenuItem>
                    <MenuItem value="audio">Audio Only</MenuItem>
                  </Select>
                </FormControl>

                <FormControl fullWidth>
                  <InputLabel>Quality</InputLabel>
                  <Select
                    {...register('quality')}
                    label="Quality"
                    defaultValue="1080p"
                  >
                    <MenuItem value="best">Best Available</MenuItem>
                    <MenuItem value="4320p">4320p (8K)</MenuItem>
                    <MenuItem value="2160p">2160p (4K)</MenuItem>
                    <MenuItem value="1440p">1440p (2K)</MenuItem>
                    <MenuItem value="1080p">1080p (Full HD)</MenuItem>
                    <MenuItem value="720p">720p (HD)</MenuItem>
                    <MenuItem value="480p">480p (SD)</MenuItem>
                    <MenuItem value="360p">360p</MenuItem>
                  </Select>
                </FormControl>
              </Box>

              {downloadProgress > 0 && (
                <Box sx={{ mb: 3 }}>
                  <Typography variant="body2" sx={{ mb: 1 }}>
                    Download Progress: {Math.round(downloadProgress)}%
                  </Typography>
                  <LinearProgress variant="determinate" value={downloadProgress} />
                </Box>
              )}

              <Button
                type="submit"
                fullWidth
                variant="contained"
                size="large"
                disabled={isLoading}
                startIcon={<CloudDownload />}
                sx={{
                  py: 1.5,
                  background: 'linear-gradient(45deg, #667eea, #764ba2)',
                  '&:hover': {
                    background: 'linear-gradient(45deg, #5a6fd8, #6a4190)',
                  },
                }}
              >
                {isLoading ? 'Processing...' : 'Download'}
              </Button>
            </Box>
          </CardContent>
        </Card>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
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
            <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 2 }}>
              How to Use
            </Typography>
            <Typography variant="body2" sx={{ opacity: 0.7, mb: 2 }}>
              1. Paste a YouTube video URL in the field above
            </Typography>
            <Typography variant="body2" sx={{ opacity: 0.7, mb: 2 }}>
              2. Click "Get Info" to preview the video details
            </Typography>
            <Typography variant="body2" sx={{ opacity: 0.7, mb: 2 }}>
              3. Select your preferred download type and quality
            </Typography>
            <Typography variant="body2" sx={{ opacity: 0.7 }}>
              4. Click "Download" to start the download process
            </Typography>
          </CardContent>
        </Card>
      </motion.div>
    </Box>
  );
};

export default YouTubeDownloader;
