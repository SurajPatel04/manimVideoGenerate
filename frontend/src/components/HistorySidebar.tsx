import { useState, useEffect, useCallback, useRef } from 'react';
import { IconHistory, IconChevronRight, IconVideo, IconFileCode } from '@tabler/icons-react';
import { UserApiService } from '@/services/userApi';
import { useAuth } from '@/contexts/AuthContext';
import type { UserHistoryItem, UserHistoryMessage } from '@/types/api';

interface HistorySidebarProps {
  isOpen: boolean;
  onToggle: () => void;
  onHistoryItemClick?: (historyItem: UserHistoryItem) => void;
  inMainSidebar?: boolean;
  currentHistoryId?: string | null;
  refreshKey?: number;
}

export default function HistorySidebar({ isOpen, onToggle, onHistoryItemClick, inMainSidebar = false, currentHistoryId = null, refreshKey }: HistorySidebarProps) {
  const [historyData, setHistoryData] = useState<UserHistoryItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [hasMore, setHasMore] = useState(false);
  const [noHistoryFound, setNoHistoryFound] = useState(false);
  const { tokens } = useAuth();
  const isFetchingRef = useRef(false);
  const fetchedOnceRef = useRef(false);

  const fetchHistory = useCallback(async (page: number = 1, reset: boolean = false) => {
    if (!tokens?.accessToken) return;
    if (isFetchingRef.current) return;
    isFetchingRef.current = true;

    setLoading(true);
    setError(null);
    setNoHistoryFound(false);

    try {
      const response = await UserApiService.getUserHistory(tokens.accessToken, page, 15);
      
      if (reset) {
        setHistoryData(response.data || []);
      } else {
        setHistoryData(prev => [...(prev || []), ...(response.data || [])]);
      }
      
      setCurrentPage(response.page);
      setHasMore(response.page < response.pages);
      

      if (response.total === 0) {
        setNoHistoryFound(true);
      }
    } catch (err: any) {
      console.error('Failed to fetch user history:', err);
      setError(err.message || 'Failed to load history');
      if (reset) {
        setHistoryData([]);
      }
    } finally {
      setLoading(false);
      isFetchingRef.current = false;
      if (page === 1 && !reset) {

      }
    }
  }, [tokens?.accessToken]);

  useEffect(() => {
    if (!isOpen || !tokens?.accessToken) return;
    if (fetchedOnceRef.current) return;
    fetchHistory(1, true).catch(() => {});
    fetchedOnceRef.current = true;
  }, [isOpen, tokens?.accessToken, fetchHistory]);

  useEffect(() => {
    fetchedOnceRef.current = false;
  }, [tokens?.accessToken]);

  useEffect(() => {
    if (refreshKey === undefined || refreshKey === null) return;
    if (!tokens?.accessToken) return;
    fetchedOnceRef.current = false;
    fetchHistory(1, true).catch(err => {
      console.warn('HistorySidebar: refresh fetch failed', err);
    });
  }, [refreshKey, tokens?.accessToken, fetchHistory]);

  const handleLoadMore = useCallback(() => {
    if (!loading && hasMore) {
      fetchHistory(currentPage + 1, false);
    }
  }, [loading, hasMore, currentPage, fetchHistory]);

  const formatDate = (timestamp: string) => {
    try {
      const date = new Date(timestamp);
      return date.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    } catch {
      return 'Unknown date';
    }
  };

  const getLatestMessage = (messages: UserHistoryMessage[]) => {
    if (!messages || messages.length === 0) return null;
    return messages[messages.length - 1] || messages[0];
  };

  if (!isOpen) return null;
  const safeHistoryData = Array.isArray(historyData) ? historyData : [];

  if (inMainSidebar) {
    return (
      <div className="space-y-2">
        {loading && (safeHistoryData?.length || 0) === 0 && (
          <div className="text-center py-4">
            <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-400 mx-auto"></div>
            <p className="text-gray-400 text-xs mt-1">Loading...</p>
          </div>
        )}

        {error && !noHistoryFound && (
          <div className="text-center py-4">
            <p className="text-red-400 text-xs">{error}</p>
            <button
              onClick={() => fetchHistory(1, true)}
              className="mt-1 px-2 py-1 bg-blue-600 hover:bg-blue-700 rounded text-xs text-white transition-colors"
            >
              Retry
            </button>
          </div>
        )}

        {(((safeHistoryData?.length || 0) === 0 && !loading && !error) || noHistoryFound) && (
          <div className="text-center py-4">
            <IconHistory className="h-8 w-8 text-gray-600 mx-auto mb-1" />
            <p className="text-gray-400 text-xs">No history found</p>
          </div>
        )}

        {safeHistoryData?.map((item) => {
          const latestMessage = getLatestMessage(item.messages || []);
          const isVideo = latestMessage?.link?.includes('.mp4');
          const isGif = latestMessage?.link?.includes('.gif');
          
          const isActive = currentHistoryId && currentHistoryId === item._id;

          return (
            <div
              key={item._id}
              className={`rounded-lg p-3 border transition-all duration-200 cursor-pointer ${isActive ? 'bg-gradient-to-r from-blue-700/40 to-transparent border-blue-500' : 'bg-gray-800/50 border border-gray-700/50 hover:border-gray-600 hover:bg-gray-700/50'}`}
              onClick={() => onHistoryItemClick?.(item)}
            >
              <div className="flex items-start justify-between gap-2 mb-2">
                <h3 className="text-white text-sm font-medium line-clamp-2 flex-1 group-hover:text-blue-300 transition-colors">
                  {item.chatName}
                </h3>
                <div className="flex-shrink-0 mt-0.5">
                  {isVideo && <IconVideo className="h-3.5 w-3.5 text-blue-400" />}
                  {isGif && <IconFileCode className="h-3.5 w-3.5 text-green-400" />}
                </div>
              </div>

              <div className="flex items-center justify-between text-xs">
                <span className="text-gray-400">
                  {item.messages?.length || 0} msg{(item.messages?.length || 0) !== 1 ? 's' : ''}
                </span>
                {latestMessage && (
                  <span className="text-gray-500 text-xs">
                    {formatDate(latestMessage.timestamp).split(',')[0]}
                  </span>
                )}
              </div>
            </div>
          );
        })}

        {hasMore && (
          <div className="text-center py-3">
            <button
              onClick={handleLoadMore}
              disabled={loading}
              className="px-3 py-1.5 bg-gray-700 hover:bg-gray-600 rounded-md text-white text-xs transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Loading...' : 'Load More'}
            </button>
          </div>
        )}
      </div>
    );
  }

  return (
    <div className={`fixed right-0 top-0 h-full w-80 bg-gray-900 border-l border-gray-700 z-50 transform transition-transform duration-300 shadow-2xl ${
      isOpen ? 'translate-x-0' : 'translate-x-full'
    }`}>

      <div className="flex items-center justify-between p-4 border-b border-gray-700">
        <div className="flex items-center gap-2">
          <IconHistory className="h-5 w-5 text-blue-400" />
          <h2 className="text-white font-semibold">History</h2>
        </div>
        <button
          onClick={onToggle}
          className="p-2 hover:bg-gray-700 rounded-lg transition-colors"
        >
          <IconChevronRight className="h-4 w-4 text-gray-400" />
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {loading && (safeHistoryData?.length || 0) === 0 && (
          <div className="text-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-400 mx-auto"></div>
            <p className="text-gray-400 text-sm mt-2">Loading history...</p>
          </div>
        )}

        {error && !noHistoryFound && (
          <div className="text-center py-8">
            <p className="text-red-400 text-sm">{error}</p>
            <button
              onClick={() => fetchHistory(1, true)}
              className="mt-2 px-3 py-1 bg-blue-600 hover:bg-blue-700 rounded text-xs text-white transition-colors"
            >
              Retry
            </button>
          </div>
        )}

        {(((safeHistoryData?.length || 0) === 0 && !loading && !error) || noHistoryFound) && (
          <div className="text-center py-8">
            <IconHistory className="h-12 w-12 text-gray-600 mx-auto mb-2" />
            <p className="text-gray-400 text-sm">No history found</p>
          </div>
        )}

        {safeHistoryData?.map((item) => {
          const latestMessage = getLatestMessage(item.messages || []);
          const isVideo = latestMessage?.link?.includes('.mp4');
          const isGif = latestMessage?.link?.includes('.gif');
          
          return (
            <div
              key={item._id}
              className="bg-gray-800 rounded-lg p-3 border border-gray-700 hover:border-gray-600 cursor-pointer transition-all duration-200 hover:bg-gray-750"
              onClick={() => onHistoryItemClick?.(item)}
            >

              <div className="flex items-start justify-between gap-2 mb-2">
                <h3 className="text-white text-sm font-medium line-clamp-2 flex-1">
                  {item.chatName}
                </h3>
                <div className="flex-shrink-0">
                  {isVideo && <IconVideo className="h-4 w-4 text-blue-400" />}
                  {isGif && <IconFileCode className="h-4 w-4 text-green-400" />}
                </div>
              </div>

              {latestMessage && (
                <p className="text-gray-400 text-xs line-clamp-2 mb-2">
                  {latestMessage.userQuery}
                </p>
              )}

              <div className="flex items-center justify-between text-xs">
                <span className="text-gray-500">
                  {item.messages?.length || 0} message{(item.messages?.length || 0) !== 1 ? 's' : ''}
                </span>
                {latestMessage && (
                  <span className="text-gray-500">
                    {formatDate(latestMessage.timestamp)}
                  </span>
                )}
              </div>
              {latestMessage?.quality && (
                <div className="mt-2">
                  <span className="inline-block px-2 py-1 bg-blue-600/20 text-blue-400 text-xs rounded">
                    {latestMessage.quality.toUpperCase()}
                  </span>
                </div>
              )}
            </div>
          );
        })}

        {hasMore && (
          <div className="text-center py-4">
            <button
              onClick={handleLoadMore}
              disabled={loading}
              className="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg text-white text-sm transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Loading...' : 'Load More'}
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export function HistoryToggleButton({ onClick, isOpen }: { onClick: () => void; isOpen: boolean }) {
  return (
    <button
      onClick={onClick}
      className="fixed right-4 top-4 z-30 p-3 bg-gray-800 hover:bg-gray-700 rounded-lg border border-gray-700 transition-all duration-200 shadow-lg"
      title="Toggle History"
    >
      {isOpen ? (
        <IconChevronRight className="h-5 w-5 text-white" />
      ) : (
        <IconHistory className="h-5 w-5 text-white" />
      )}
    </button>
  );
}
