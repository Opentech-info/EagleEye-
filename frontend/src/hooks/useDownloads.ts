import { useQuery, useMutation, useQueryClient } from 'react-query';
import { downloadsAPI } from '../services/api';
import toast from 'react-hot-toast';

export interface Download {
  id: number;
  url: string;
  title: string;
  status: 'pending' | 'downloading' | 'completed' | 'failed';
  progress: number;
  created_at: string;
  completed_at?: string;
}

export const useDownloads = () => {
  const queryClient = useQueryClient();

  // Get all downloads
  const {
    data: downloads,
    isLoading,
    error,
    refetch,
  } = useQuery<Download[]>('downloads', async () => {
    const response = await downloadsAPI.getAll();
    return response.data;
  });

  // Delete download mutation
  const deleteDownloadMutation = useMutation(
    (downloadId: number) => downloadsAPI.delete(downloadId),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('downloads');
        toast.success('Download deleted successfully');
      },
      onError: (error: any) => {
        toast.error(error.response?.data?.error || 'Failed to delete download');
      },
    }
  );

  // Download file mutation
  const downloadFileMutation = useMutation(
    async (downloadId: number) => {
      const response = await downloadsAPI.downloadFile(downloadId);
      
      // Create blob URL and trigger download
      const blob = new Blob([response.data]);
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      
      // Try to get filename from response headers
      const contentDisposition = response.headers['content-disposition'];
      let filename = 'download';
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="(.+)"/);
        if (filenameMatch) {
          filename = filenameMatch[1];
        }
      }
      
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      
      return response;
    },
    {
      onSuccess: () => {
        toast.success('File download started');
      },
      onError: (error: any) => {
        toast.error(error.response?.data?.error || 'Failed to download file');
      },
    }
  );

  return {
    downloads: downloads || [],
    isLoading,
    error,
    refetch,
    deleteDownload: deleteDownloadMutation.mutate,
    downloadFile: downloadFileMutation.mutate,
    isDeleting: deleteDownloadMutation.isLoading,
    isDownloading: downloadFileMutation.isLoading,
  };
};
