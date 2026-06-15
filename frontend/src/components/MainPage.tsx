import { useState, useCallback, useMemo, memo, useEffect, useRef } from "react";
import { PlaceholdersAndVanishInput } from "@/components/ui/placeholders-and-vanish-input";
import { Sidebar, SidebarBody } from "@/components/ui/sidebar";
import { BackgroundBeams } from "@/components/ui/background-beams";
import { CodeBlock } from "@/components/ui/code-block";
import { ConfirmationModal } from "@/components/ui/confirmation-modal";
import { useAuth } from "@/contexts/AuthContext";
import { useNavigate } from "react-router-dom";
import { IconPlus, IconUser, IconLogout, IconMenu2, IconDownload, IconCode, IconX, IconHistory, IconCheck } from "@tabler/icons-react";
import type { ManimGenerationRequest, UserHistoryItem } from '@/types/api';
import { ManimApiService } from '@/services/manimApi';
import { Box, useTheme, useMediaQuery } from '@mui/material';
import HistorySidebar from '@/components/HistorySidebar';
import '@/styles/scrollbar.css';
import { motion, AnimatePresence } from "motion/react";

interface MessageType {
  type: 'user' | 'assistant';
  content: string;
  taskId?: string;
  videoUrl?: string;
  progress?: number;
  stage?: string;
  code?: string;
  filename?: string;
  success?: boolean;
  id: string; 
}

const SUGGESTION_PROMPTS = [
  "Create a 3D surface plot of the function z = sin(x) * cos(y) using a grid",
  "Animate how the normal distribution curve changes with different standard deviations.",
  "Plot y = e^(-x²) as a smooth bell-shaped curve",
  "Draw a projectile motion trajectory in, marking max height and range."

];

const PLACEHOLDERS = [
  "Create an animation showing the derivation of quadratic formula",
  "Generate a video explaining Newton's laws of motion with examples",
  "Make an animation about the water cycle and climate change",
];

const SuggestionButton = memo(({ suggestion, onClick }: { suggestion: string, onClick: (suggestion: string, options?: { format: string; quality: string; resolution?: string }) => void }) => (
  <motion.button
    whileHover={{ scale: 1.02 }}
    whileTap={{ scale: 0.98 }}
    onClick={() => onClick(suggestion, { format: "mp4", quality: "ql", resolution: "1920x1080" })}
    className="flex flex-col items-start p-4 md:p-5 rounded-2xl border border-neutral-800 bg-neutral-900/50 backdrop-blur-sm transition-all duration-300 hover:border-neutral-700 text-left group cursor-pointer w-full"
  >
    <p className="text-sm text-neutral-400 group-hover:text-neutral-200 transition-colors">{suggestion}</p>
  </motion.button>
));

const ProgressStepper = memo(({ progress }: { progress?: number }) => {
  const fullSteps = [
    'Setting up description generation state',
    'Analyzing if user query is possible',
    'Detailed description in progress',
    'Creating animation code and rendering video',
    'Video generation completed successfully'
  ];

  const getActiveStep = () => {
    const currentProgress = progress || 0;
    if (currentProgress <= 10) return 0; 
    if (currentProgress <= 20) return 1;
    if (currentProgress <= 30) return 2;
    if (currentProgress <= 50) return 3;
    return 4;
  };

  const activeStep = getActiveStep();

  return (
    <div className="w-full py-4 md:py-8 px-2 md:px-4 font-sans">
      <div className="relative flex flex-col md:flex-row justify-between w-full">
        {fullSteps.map((label, idx) => {
          const isCompleted = idx < activeStep;
          const isActive = idx === activeStep;
          const isLast = idx === fullSteps.length - 1;

          return (
            <div 
              key={label} 
              className={`relative flex flex-row md:flex-col items-start md:items-center ${isLast ? '' : 'md:flex-1'} mb-8 md:mb-0`}
            >
              {/* Connecting Lines */}
              {!isLast && (
                <>
                  {/* Desktop horizontal line */}
                  <div className="hidden md:block absolute top-[14px] left-[50%] w-full h-[2px] bg-neutral-800">
                    <motion.div 
                      className="h-full bg-blue-500 origin-left"
                      initial={false}
                      animate={{ scaleX: isCompleted ? 1 : 0 }}
                      transition={{ duration: 0.6, ease: "easeInOut" }}
                    />
                  </div>
                  {/* Mobile vertical line */}
                  <div className="md:hidden absolute top-[28px] left-[13px] w-[2px] h-[calc(100%+20px)] bg-neutral-800">
                    <motion.div 
                      className="w-full bg-blue-500 origin-top"
                      initial={false}
                      animate={{ scaleY: isCompleted ? 1 : 0 }}
                      transition={{ duration: 0.6, ease: "easeInOut" }}
                    />
                  </div>
                </>
              )}

              {/* Step Circle Container */}
              <div className="relative z-10 flex flex-col items-center shrink-0">
                <motion.div 
                  className={`flex items-center justify-center w-7 h-7 rounded-full border-[2px] text-xs font-semibold transition-colors duration-500 ${
                    isCompleted 
                      ? 'bg-emerald-500/20 border-emerald-500 text-emerald-400 shadow-[0_0_15px_rgba(16,185,129,0.3)]' 
                      : isActive 
                        ? 'bg-blue-600 border-blue-500 text-white shadow-[0_0_20px_rgba(59,130,246,0.6)]' 
                        : 'bg-neutral-900 border-neutral-700 text-neutral-500'
                  }`}
                  animate={isActive ? { scale: [1, 1.15, 1], borderColor: ['#3b82f6', '#60a5fa', '#3b82f6'] } : { scale: 1 }}
                  transition={isActive ? { repeat: Infinity, duration: 2 } : { duration: 0.3 }}
                >
                  {isCompleted ? (
                    <motion.div
                      initial={{ scale: 0 }}
                      animate={{ scale: 1 }}
                      transition={{ type: "spring", stiffness: 300, damping: 20 }}
                    >
                      <IconCheck size={16} stroke={3} />
                    </motion.div>
                  ) : (
                    <span>{idx + 1}</span>
                  )}
                </motion.div>
              </div>

              {/* Label */}
              <div className={`mt-0 ml-4 md:mt-4 md:ml-0 text-left md:text-center w-full md:w-36 transition-colors duration-500 ${
                isCompleted 
                  ? 'text-emerald-400/90' 
                  : isActive 
                    ? 'text-blue-300 font-medium' 
                    : 'text-neutral-500'
              }`}>
                <span className="text-[0.85rem] md:text-[0.75rem] leading-snug md:leading-tight block">
                  {label}
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
});

const Message = memo(({ message, onCodeModalToggle, onDownload }: { 
  message: MessageType,
  onCodeModalToggle: (isOpen: boolean, message?: MessageType | null) => void,
  onDownload: (url: string, filename?: string | undefined) => Promise<void>
}) => {


  const handleShowCode = useCallback(() => {
    onCodeModalToggle(true, message);
  }, [onCodeModalToggle, message]);

  const videoSection = useMemo(() => {
    if (message.type !== 'assistant' || !message.videoUrl || message.success === false) {
      return null;
    }

    const isGif = message.videoUrl.toLowerCase().includes('.gif');

    return (
      <div className="mt-3 flex flex-col items-center">
        {isGif ? (
          <img 
            src={message.videoUrl}
            alt="Generated animation"
            className="w-full max-w-md rounded-lg"
            style={{ maxHeight: '400px', objectFit: 'contain' }}
          />
        ) : (
          <video 
            controls 
            className="w-full max-w-md rounded-lg"
            poster=""
            preload="metadata" 
          >
            <source src={message.videoUrl} type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        )}
        <div className="mt-2 flex gap-2 flex-wrap">
          {isGif ? (
            <button
              onClick={() => { if (message.videoUrl) void onDownload(message.videoUrl, message.filename); }}
              className="inline-flex items-center gap-1 px-3 py-1 bg-blue-600 hover:bg-blue-700 rounded text-xs transition-colors flex-shrink-0"
            >
              <IconDownload className="h-3 w-3 flex-shrink-0" />
              <span className="whitespace-nowrap">Download GIF</span>
            </button>
          ) : (
            <a 
              href={message.videoUrl} 
              download
              className="inline-flex items-center gap-1 px-3 py-1 bg-blue-600 hover:bg-blue-700 rounded text-xs transition-colors flex-shrink-0"
            >
              <IconDownload className="h-3 w-3 flex-shrink-0" />
              <span className="whitespace-nowrap">Download Video</span>
            </a>
          )}
          {message.code && (
            <button
              onClick={handleShowCode}
              className="inline-flex items-center gap-1 px-3 py-1 bg-green-600 hover:bg-green-700 rounded text-xs transition-colors flex-shrink-0"
            >
              <IconCode className="h-3 w-3 flex-shrink-0" />
              <span className="whitespace-nowrap">Code</span>
            </button>
          )}
        </div>
      </div>
    );
  }, [message.videoUrl, message.code, message.success, handleShowCode]);

  const stepperSection = useMemo(() => {
    if (message.type !== 'assistant' || !message.taskId || message.videoUrl || message.success === false) {
      return null;
    }
    return <ProgressStepper progress={message.progress} />;
  }, [message.type, message.taskId, message.videoUrl, message.success, message.progress]);

  return (
    <>
      <motion.div
        initial={{ opacity: 0, y: message.type === 'user' ? 0 : 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.2, ease: "easeOut" }}
        className={`group flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
      >
        <div className={`flex flex-col gap-2 ${message.type === 'user' ? 'max-w-[80%] items-end' : 'w-full'}`}>
          <div
            className={
              message.type === 'user'
                ? 'user-message-bubble rounded-2xl rounded-tr-sm bg-neutral-800 px-4 py-2.5 text-sm md:text-base text-neutral-100 shadow-sm'
                : 'flex-1 text-sm md:text-base text-neutral-100'
            }
          >
            <p className="whitespace-pre-wrap break-words leading-relaxed text-neutral-200">{message.content}</p>
            
            {stepperSection}

            {videoSection}
          </div>
        </div>
      </motion.div>

      {/* Code Modal is rendered at top-level in MainPage to avoid sidebar overlap */}
    </>
  );
}, (prevProps, nextProps) => {

  const prevMsg = prevProps.message;
  const nextMsg = nextProps.message;
  
  return (
    prevMsg.content === nextMsg.content &&
    prevMsg.progress === nextMsg.progress &&
    prevMsg.videoUrl === nextMsg.videoUrl &&
    prevMsg.success === nextMsg.success &&
    prevMsg.stage === nextMsg.stage &&
    prevMsg.code === nextMsg.code
  );
});

export default function MainPage() {
  const [messages, setMessages] = useState<MessageType[]>([]);
  const [isGenerating, setIsGenerating] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [currentHistoryId, setCurrentHistoryId] = useState<string>("");
  const [historyRefreshKey, setHistoryRefreshKey] = useState<number>(0);
  const [currentTaskId, setCurrentTaskId] = useState<string>("");
  const [inputValue, setInputValue] = useState<string>(""); 
  const [pollingInterval, setPollingInterval] = useState<NodeJS.Timeout | null>(null);
  const [isCodeModalOpen, setIsCodeModalOpen] = useState(false); 
  const [codeModalMessage, setCodeModalMessage] = useState<MessageType | null>(null);
  const [cancelledTasks, setCancelledTasks] = useState<Set<string>>(new Set());
  const [activePollingTimeouts, setActivePollingTimeouts] = useState<Set<NodeJS.Timeout>>(new Set()); 
  const [isLogoutModalOpen, setIsLogoutModalOpen] = useState(false);
  const { user, logout, tokens } = useAuth();
  const navigate = useNavigate();
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const userMenuRef = useRef<HTMLDivElement>(null);
  const mobileUserMenuRef = useRef<HTMLDivElement>(null);

  const generateMessageId = useCallback(() => `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`, []);

  const startTaskPolling = useCallback(async (taskId: string) => {
    if (!tokens?.accessToken) return;

    let pollCount = 0;
    let consecutiveErrors = 0;
    const maxRetries = 3;
    const baseInterval = 2000;
    const maxInterval = 10000; 
    const maxPollCount = 300;
    let isCancelled = false;
    const timeouts: NodeJS.Timeout[] = [];
    
    const calculateInterval = () => {
      if (consecutiveErrors === 0) return 2000;
      const backoff = Math.min(baseInterval * Math.pow(1.5, consecutiveErrors), maxInterval);
      const jitter = Math.random() * 500;
      return backoff + jitter;
    };

    const pollTask = async () => {
      try {
        pollCount++;
        
        if (cancelledTasks.has(taskId) || isCancelled) {
          console.log('Task was cancelled locally, stopping polling');
          return true;
        }
        
        if (pollCount > maxPollCount) {
          console.warn('Polling timeout reached, stopping polling');
          setMessages(prev => prev.map(msg => 
            msg.taskId === taskId 
              ? { 
                  ...msg, 
                  content: 'Polling timeout. The task may still be processing on the server.'
                }
              : msg
          ));
          setIsGenerating(false);
          return true;
        }

        const result = await ManimApiService.pollTaskStatus(taskId, tokens.accessToken);
        

        consecutiveErrors = 0;

        setMessages(prev => prev.map(msg => 
          msg.taskId === taskId 
            ? { 
                ...msg, 
                progress: result.progress,
                stage: result.current_stage,
                content: result.status === 'completed'
                  ? result.data?.success
                    ? `Animation completed successfully! Your "${result.data.chat_name}" is ready.`
                    : `Animation generation failed: ${result.data?.reason || result.data?.message || 'Unknown error'}`
                  : result.status === 'failed'
                  ? `Animation generation failed. Please try again.`
                  : result.status === 'cancelled'
                  ? `Animation generation was cancelled by user.`
                  : result.status === 'pending'
                    ? (() => {
                        const queuePos = typeof result.queue_left === 'number' ? result.queue_left : null;
                        return queuePos !== null ? `Your Place in Queue: ${queuePos}` : 'In Queue';
                      })()
                  : result.status === 'in_progress'
                    ? 'Generating animation...'
                  : `${result.current_stage || 'In Queue'}`
              }
            : msg
        ));

        if (result.status === 'completed' || result.status === 'failed' || result.status === 'cancelled') {
          
          setIsGenerating(false);
          
          if (result.status === 'completed') {
            if (result.data?.success) {
              if (result.data.historyId) {
                setCurrentHistoryId(result.data.historyId);
              }
              setMessages(prev => prev.map(msg => 
                msg.taskId === taskId 
                  ? { 
                      ...msg, 
                      videoUrl: result.data?.link,
                      code: result.data?.data?.code || result.data?.code,
                      filename: result.data?.data?.filename || result.data?.filename,
                      content: `✅ Animation completed successfully! Your "${result.data?.chat_name}" is ready.`,
                      success: true
                    }
                  : msg
              ));

              setHistoryRefreshKey(prev => prev + 1);
            } else {
              const failureReason = result.data?.reason || result.data?.message || 'Animation generation failed for unknown reasons.';
              setMessages(prev => prev.map(msg => 
                msg.taskId === taskId 
                  ? { 
                      ...msg, 
                      content: `❌ Animation generation failed: ${failureReason}`,
                      success: false
                    }
                  : msg
              ));
            }
          } else if (result.status === 'failed') {
            setMessages(prev => prev.map(msg => 
              msg.taskId === taskId 
                ? { 
                    ...msg, 
                    content: `❌ Animation generation failed. Please try again.`,
                    success: false
                  }
                : msg
            ));
          } else if (result.status === 'cancelled') {
            setMessages(prev => prev.map(msg => 
              msg.taskId === taskId 
                ? { 
                    ...msg, 
                    content: `🚫 Animation generation was cancelled.`,
                    success: false,
                    progress: undefined,
                    stage: undefined
                  }
                : msg
            ));
          }
          
          return true;
        }
        
        return false;
      } catch (error) {
        consecutiveErrors++;
        console.error(`Polling error #${consecutiveErrors}:`, error);
        
        if (consecutiveErrors >= maxRetries) {
          console.error('Max polling errors reached, stopping polling');
          setMessages(prev => prev.map(msg => 
            msg.taskId === taskId 
              ? { 
                  ...msg, 
                  content: `Connection failed after ${maxRetries} retries. Task ID: ${taskId}`
                }
              : msg
          ));
          setIsGenerating(false);
          return true;
        }

        setMessages(prev => prev.map(msg => 
          msg.taskId === taskId 
            ? { 
                ...msg, 
                content: `Connection issue (${consecutiveErrors}/${maxRetries}). Retrying...`
              }
            : msg
        ));
        
        return false;
      }
    };

    const shouldStop = await pollTask();
    if (shouldStop) {
      return;
    }
    
    const scheduleNextPoll = () => {
      if (isCancelled || cancelledTasks.has(taskId)) {
        return;
      }
      
      const interval = calculateInterval();
      
      const timeoutId = setTimeout(async () => {
        setActivePollingTimeouts(prev => {
          const newSet = new Set(prev);
          newSet.delete(timeoutId);
          return newSet;
        });
        
        const shouldStop = await pollTask();
        if (!shouldStop) {
          scheduleNextPoll();
        } else {
          setPollingInterval(null);
        }
      }, interval);
      
      timeouts.push(timeoutId);
      setActivePollingTimeouts(prev => new Set([...prev, timeoutId]));
    };

    scheduleNextPoll();
    
    // Return cleanup function
    return () => {
      isCancelled = true;
      timeouts.forEach(timeout => clearTimeout(timeout));
    };
  }, [tokens?.accessToken, cancelledTasks]);

  useEffect(() => {
    return () => {
      if (pollingInterval) {
        clearInterval(pollingInterval);
      }
    };
  }, [pollingInterval]);

  useEffect(() => {
    const scrollToBottom = () => {
      messagesEndRef.current?.scrollIntoView({ 
        behavior: 'smooth',
        block: 'nearest'
      });
    };
    
    if (messages.length < 50) {
      const timeoutId = setTimeout(scrollToBottom, 150);
      return () => clearTimeout(timeoutId);
    }
  }, [messages.length]);

  useEffect(() => {
    if (isGenerating) {
      const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ 
          behavior: 'smooth',
          block: 'nearest'
        });
      };
      
      const timeoutId = setTimeout(scrollToBottom, 100);
      return () => clearTimeout(timeoutId);
    }
  }, [isGenerating]);

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      const target = event.target as Element;
      
      if (target.closest('button')?.textContent?.includes('Logout')) {
        return;
      }
      
      const clickedInsideDesktop = userMenuRef.current?.contains(target) ?? false;
      const clickedInsideMobile = mobileUserMenuRef.current?.contains(target) ?? false;

      if (showUserMenu && !clickedInsideDesktop && !clickedInsideMobile) {
        setShowUserMenu(false);
      }
    }

    if (showUserMenu) {
      setTimeout(() => {
        document.addEventListener('mousedown', handleClickOutside);
      }, 0);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [showUserMenu]);

  const toggleSidebar = useCallback(() => setSidebarOpen(prev => !prev), []);

  const handleHistoryItemClick = useCallback((historyItem: UserHistoryItem) => {
    const newMessages: MessageType[] = [];
    
    historyItem.messages.forEach((histMsg, index) => {
      newMessages.push({
        type: 'user',
        content: histMsg.userQuery,
        id: `history_user_${historyItem._id}_${index}`
      });

      newMessages.push({
        type: 'assistant',
        content: `✅ Animation completed successfully! Your "${historyItem.chatName}" is ready.`,
        videoUrl: histMsg.link,
        code: histMsg.code,
        filename: histMsg.filename,
        success: true,
        id: `history_assistant_${historyItem._id}_${index}`
      });
    });

    setMessages(newMessages);
    setCurrentHistoryId(historyItem._id);

    if (window.innerWidth < 768) {
      setSidebarOpen(false);
    }
  }, []);

  const stopPollingAndReset = useCallback(() => {
    // Clear all active polling timeouts
    activePollingTimeouts.forEach(timeout => clearTimeout(timeout));
    setActivePollingTimeouts(new Set());
    
    if (pollingInterval) {
      clearInterval(pollingInterval);
      setPollingInterval(null);
    }
    setIsGenerating(false);
    setCurrentTaskId("");
  }, [pollingInterval, activePollingTimeouts]);

  const handleCancelTask = useCallback(async () => {
    if (!currentTaskId || !tokens?.accessToken) return;

    try {
      setCancelledTasks(prev => new Set([...prev, currentTaskId]));
      
      stopPollingAndReset();

      setMessages(prev => prev.map(msg => 
        msg.taskId === currentTaskId 
          ? { 
              ...msg, 
              content: 'Cancelling animation generation...',
              progress: undefined,
              stage: undefined
            }
          : msg
      ));

      await ManimApiService.cancelTask(currentTaskId, tokens.accessToken);

      setMessages(prev => prev.map(msg => 
        msg.taskId === currentTaskId 
          ? { 
              ...msg, 
              content: '🚫 Animation generation was cancelled.',
              success: false
            }
          : msg
      ));

    } catch (error: any) {
      console.error('Error cancelling task:', error);
      
      setMessages(prev => prev.map(msg => 
        msg.taskId === currentTaskId 
          ? { 
              ...msg, 
              content: '🚫 Animation generation was cancelled (local cancellation).',
              success: false
            }
          : msg
      ));
    }
  }, [currentTaskId, tokens?.accessToken, stopPollingAndReset]);

  const handleNewChat = useCallback(() => {
    setMessages([]);
    setCurrentHistoryId(""); 
    setCurrentTaskId(""); 
    setIsGenerating(false);
    setCancelledTasks(new Set());
    
    // Clear all active polling timeouts
    activePollingTimeouts.forEach(timeout => clearTimeout(timeout));
    setActivePollingTimeouts(new Set());
    
    if (pollingInterval) {
      clearInterval(pollingInterval);
      setPollingInterval(null);
    }
    
    setShowUserMenu(false);

    if (window.innerWidth < 768) {
      setSidebarOpen(false);
    }
  }, [pollingInterval, activePollingTimeouts]);

  const confirmLogout = useCallback(() => {
    try {
      logout();
      setShowUserMenu(false);
      setIsLogoutModalOpen(false);
      navigate('/login', { replace: true });
    } catch (error) {
      console.error('Logout error:', error);
      setShowUserMenu(false);
      setIsLogoutModalOpen(false);
      navigate('/login', { replace: true });
    }
  }, [logout, navigate]);

  const handleLogoutClick = useCallback((e?: React.MouseEvent) => {
    e?.preventDefault();
    e?.stopPropagation();
    setIsLogoutModalOpen(true);
  }, []);

  const toggleUserMenu = useCallback(() => setShowUserMenu(prev => !prev), []);

  const processSubmission = useCallback(async (text: string, options: { format: string; quality: string; resolution?: string } = { format: "mp4", quality: "ql", resolution: "1920x1080" }) => {
    if (!text || !text.trim()) return;

    const userMessage: MessageType = { 
      type: 'user', 
      content: text.trim(),
      id: generateMessageId()
    };
    setMessages(prev => [...prev, userMessage]);
    setIsGenerating(true);

    const assistantMessage: MessageType = {
      type: 'assistant',
      content: 'Generating animation...',
      taskId: 'temp-id',
      progress: 0,
      stage: "Setting up description generation state",
      id: generateMessageId()
    };
    setMessages(prev => [...prev, assistantMessage]);

    try {
      if (!tokens?.accessToken) {
        throw new Error('Authentication required. Please log in again.');
      }
      const requestPayload: ManimGenerationRequest = {
        userQuery: text.trim(),
        format: options.format,
        quality: options.quality, 
        historyId: currentHistoryId,
        resolution: options.resolution
      };

      const response = await ManimApiService.generateAnimation(requestPayload, tokens.accessToken);

      setCurrentTaskId(response.task_id);

      if (response.historyId) {
        setCurrentHistoryId(response.historyId);
      }

      setMessages(prev => prev.map(msg => 
        msg.taskId === 'temp-id' 
          ? { ...msg, taskId: response.task_id }
          : msg
      ));

      startTaskPolling(response.task_id);


    } catch (error: any) {
      console.error('Error generating manim animation:', error);
      let errorMessage = 'Sorry, there was an error generating your animation. Please try again.';
      
      if (error.message.includes('Authentication')) {
        errorMessage = 'Authentication failed. Please log in again.';
      } else if (error.message.includes('403')) {
        errorMessage = 'You do not have permission to generate animations.';
      } else if (error.message.includes('Network error')) {
        errorMessage = 'Network error. Please check your connection and try again.';
      } else if (error.message.includes('timeout')) {
        errorMessage = 'Request timed out. The animation generation is taking longer than expected.';
      } else if (error.message) {
        errorMessage = error.message;
      }

      const errorResponseMessage: MessageType = {
        type: 'assistant',
        content: errorMessage,
        id: generateMessageId()
      };
      setMessages(prev => [...prev, errorResponseMessage]);
      setIsGenerating(false);
    }
  }, [currentHistoryId, tokens?.accessToken, startTaskPolling, generateMessageId]);

  const handleDownload = useCallback(async (url: string, filename?: string) => {
    try {
      const headers: Record<string, string> = {};
      if (tokens?.accessToken) {
        headers['Authorization'] = `Bearer ${tokens.accessToken}`;
      }

      const response = await fetch(url, { headers });

      if (!response.ok) {
        window.open(url, '_blank');
        return;
      }

      const blob = await response.blob();
      const objectUrl = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = objectUrl;

      const parsedUrl = new URL(url);
      const isGif = parsedUrl.pathname.toLowerCase().endsWith('.gif');
      let downloadName = filename || parsedUrl.pathname.split('/').pop() || 'download';
      if (isGif) {
        downloadName = downloadName.replace(/\.[^/.]+$/, "") + ".gif";
      }
      a.download = downloadName;

      document.body.appendChild(a);
      a.click();
      a.remove();
      setTimeout(() => URL.revokeObjectURL(objectUrl), 1000 * 10);
    } catch (err) {
      console.error('Download failed, opening in new tab as fallback:', err);
      window.open(url, '_blank');
    }
  }, [tokens?.accessToken]);

  const onInputSubmit = (e: React.FormEvent<HTMLFormElement>, options: { format: string; quality: string; resolution?: string }) => {
      e.preventDefault();
      
      if (inputValue && inputValue.trim()) {
        processSubmission(inputValue.trim(), options);
        setInputValue("");
      }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(e.target.value);
  };

  const suggestionButtons = useMemo(() => 
    SUGGESTION_PROMPTS.map((prompt, i) => (
      <SuggestionButton key={i} suggestion={prompt} onClick={processSubmission} />
    )), [processSubmission]
  );

  return (
    <div className="h-[100dvh] w-full flex flex-col md:flex-row bg-black overflow-hidden">
      <Sidebar open={sidebarOpen} setOpen={setSidebarOpen} autoOpen={false}>
        <SidebarBody 
          className="justify-between gap-2 h-full bg-black z-[100]"
          centerContent={<span className="font-semibold text-neutral-200 text-lg truncate">Manim Generator</span>}
          rightContent={
            <button
              onClick={handleNewChat}
              className="text-neutral-400 hover:text-white transition-colors p-1"
              aria-label="New chat"
            >
              <IconPlus className="h-6 w-6" />
            </button>
          }
        >
          <div className="flex flex-col h-full min-h-0">
            <div className="flex-shrink-0 space-y-2 px-2 py-2">
              <div className={`flex items-center flex-shrink-0 ${sidebarOpen ? 'justify-between px-2' : 'justify-center'}`}>
                  <span className={`font-semibold text-neutral-200 text-lg truncate transition-opacity duration-200 ${sidebarOpen ? 'opacity-100' : 'opacity-0 hidden'}`}>
                    Manim Generator
                  </span>
                  <button
                      onClick={toggleSidebar}
                      className="p-2 hover:bg-neutral-900 rounded-lg cursor-pointer transition-colors flex-shrink-0"
                      aria-label="Toggle Menu"
                  >
                      <IconX className="text-neutral-300 hover:text-white h-5 w-5 md:hidden" />
                      <IconMenu2 className="text-neutral-300 hover:text-white h-5 w-5 hidden md:block" />
                  </button>
              </div>
              <button
                onClick={handleNewChat}
                className={`flex items-center gap-2 p-2 hover:bg-neutral-900 rounded-lg cursor-pointer transition-colors w-full ${sidebarOpen ? 'text-left' : 'justify-center'}`}
              >
                <IconPlus className="text-neutral-200 h-5 w-5 shrink-0" />
                <span className={`text-neutral-200 text-sm transition-opacity duration-200 ${sidebarOpen ? 'opacity-100' : 'opacity-0 hidden'}`}>New chat</span>
              </button>
            </div>
            
            {/* History Section */}
            <div className={`flex-1 flex flex-col min-h-0 mt-4 transition-opacity duration-200 ${sidebarOpen ? 'opacity-100 block' : 'opacity-0 hidden'}`}>
              {/* Header (fixed) */}
              <div className="mb-2 px-2 flex-shrink-0">
                <p className="px-1 text-xs font-medium uppercase tracking-wide text-neutral-500">
                  Recent
                </p>
              </div>

              {/* Scrollable history list (grows to fill space) */}
              <div className="flex-1 overflow-y-auto px-2 pr-1 sidebar-scrollbar pb-8">
                <HistorySidebar 
                    isOpen={true}
                    onToggle={() => {}}
                    onHistoryItemClick={handleHistoryItemClick}
                    inMainSidebar={true}
                    currentHistoryId={currentHistoryId}
                    refreshKey={historyRefreshKey}
                />
              </div>
            </div>
          </div>
          <div className="relative flex-shrink-0 px-2 py-1 mt-auto" ref={userMenuRef}>
            <button
              onClick={toggleUserMenu}
              className={`flex items-center gap-2 py-1 px-2 hover:bg-neutral-900 rounded-lg cursor-pointer transition-colors w-full ${sidebarOpen ? 'text-left' : 'justify-center'}`}
            >
              <div className="flex w-8 h-8 bg-neutral-800 rounded-full items-center justify-center shrink-0 border border-neutral-700">
                <IconUser className="text-neutral-200 h-4 w-4" />
              </div>
              <span className={`text-neutral-200 text-sm truncate transition-opacity duration-200 ${sidebarOpen ? 'opacity-100' : 'opacity-0 hidden'}`}>{user?.firstName || 'User'}</span>
            </button>
            {showUserMenu && sidebarOpen && (
              <div className="absolute bottom-full left-0 right-0 mb-2 bg-neutral-900 border border-neutral-800 rounded-xl shadow-2xl z-50 p-2">
                <div className="mb-2 truncate px-2 py-1.5 text-sm font-medium text-neutral-300">
                  {user?.email || `${user?.firstName || 'User'}@example.com`}
                </div>
                <div className="h-px bg-neutral-800 mb-2"></div>
                <button
                  onClick={handleLogoutClick}
                  onMouseDown={(e) => e.stopPropagation()}
                  className="w-full flex items-center justify-start gap-2 rounded-lg px-2 py-2 text-sm text-red-400 transition hover:bg-neutral-800 hover:text-red-300 cursor-pointer"
                  type="button"
                >
                  <IconLogout className="h-4 w-4 shrink-0" />
                  Logout
                </button>
              </div>
            )}
            {showUserMenu && !sidebarOpen && (
              <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 bg-neutral-900 border border-neutral-800 rounded-xl shadow-2xl z-50 p-2 whitespace-nowrap min-w-[200px]">
                <div className="mb-2 truncate px-2 py-1.5 text-sm font-medium text-neutral-300">
                  {user?.email || `${user?.firstName || 'User'}@example.com`}
                </div>
                <div className="h-px bg-neutral-800 mb-2"></div>
                <button
                  onClick={handleLogoutClick}
                  onMouseDown={(e) => e.stopPropagation()}
                  className="flex w-full items-center justify-start gap-2 rounded-lg px-2 py-2 text-sm text-red-400 transition hover:bg-neutral-800 hover:text-red-300 cursor-pointer"
                  type="button"
                >
                  <IconLogout className="h-4 w-4 shrink-0" />
                  Logout
                </button>
              </div>
            )}
          </div>
        </SidebarBody>
      </Sidebar>

      <main className="flex-1 flex flex-col min-w-0 transition-all duration-300 bg-neutral-950 relative">
        {/* Top fade mask to prevent scrolling messages from clashing with top-right global icons */}
        <div className="hidden md:block absolute top-0 left-0 right-0 h-24 bg-gradient-to-b from-neutral-950 via-neutral-950/80 to-transparent z-40 pointer-events-none" />
        
        <div className="relative flex-1 min-h-0">
          <div className="absolute inset-0 overflow-y-auto overflow-x-hidden custom-scrollbar p-4 md:p-6 md:pt-20 [overflow-anchor:auto]">
          {messages.length === 0 ? (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, ease: "easeOut" }}
              className="flex flex-col items-center justify-center min-h-[60vh] py-4 md:py-8 text-center px-4"
            >
              <h2 className="bg-gradient-to-br from-white to-neutral-500 bg-clip-text text-2xl md:text-5xl font-bold tracking-tight text-transparent mb-2 md:mb-4">
                What animation can I create for you?
              </h2>
              <p className="max-w-md text-sm md:text-base text-neutral-400 mb-6 md:mb-12">
                Describe a mathematical concept or an idea, and I'll generate a high-quality video animation using Manim.
              </p>

              <div className="w-full max-w-4xl px-2">
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 md:gap-4">
                  {suggestionButtons}
                </div>
              </div>
            </motion.div>
          ) : (
            <div className="space-y-6 md:space-y-8 max-w-4xl mx-auto pb-8 md:pb-12">
              <AnimatePresence initial={false}>
                {messages.map((msg) => (
                  <Message 
                    key={msg.id} 
                    message={msg} 
                    onCodeModalToggle={(isOpen: boolean, message?: MessageType | null) => {
                      setIsCodeModalOpen(isOpen);
                      setCodeModalMessage(message ?? null);
                    }}
                    onDownload={handleDownload}
                  />
                ))}
              </AnimatePresence>
              <div ref={messagesEndRef} id="chat-bottom" />
            </div>
          )}
          </div>
        </div>
        {!isCodeModalOpen && (
          <div className="shrink-0 bg-neutral-950 p-4 pb-6 md:pb-4">
            <div className="max-w-4xl mx-auto">
              {/* Warning message for animation code creation and video rendering */}
              {isGenerating && messages.some(msg => 
                msg.type === 'assistant' && 
                msg.taskId && 
                !msg.videoUrl && 
                msg.progress && 
                msg.progress > 30 && 
                msg.progress <= 50
              ) && (
                <div className="mb-4 p-3 bg-yellow-900/50 border border-yellow-600/50 rounded-lg">
                  <div className="flex items-center gap-2">
                    <div className="w-2 h-2 bg-yellow-500 rounded-full animate-pulse"></div>
                    <p className="text-yellow-200 text-sm">
                      The rendering process may take some time based on the complexity of your query. Please be patient while we create your animation.
                    </p>
                  </div>
                </div>
              )}
              <PlaceholdersAndVanishInput
                placeholders={PLACEHOLDERS}
                onChange={handleInputChange}
                onSubmit={onInputSubmit}
                onCancel={handleCancelTask}
                isGenerating={isGenerating}
              />
            </div>
          </div>
        )}
      </main>
      {/* Top-level Code Modal to ensure it's above sidebar */}
      {isCodeModalOpen && codeModalMessage && codeModalMessage.code && (
        <div 
          className="fixed inset-0 flex items-center justify-center p-4 z-[99999]"
          onClick={() => { setIsCodeModalOpen(false); setCodeModalMessage(null); }}
        >
          <div className="absolute inset-0 bg-black/70 backdrop-blur-md" />

          <div 
            className="relative bg-gray-900 rounded-lg max-w-6xl w-full max-h-[85vh] overflow-hidden shadow-[0_25px_50px_-12px_rgba(0,0,0,0.75)] transform transition-transform duration-200 z-[100000]"
            style={{ margin: '0 1rem' }}
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center justify-between p-4 border-b border-gray-700">
              <h3 className="text-white text-lg font-semibold">Generated Animation Code</h3>
              <button
                onClick={() => { setIsCodeModalOpen(false); setCodeModalMessage(null); }}
                className="text-gray-400 hover:text-white transition-colors"
              >
                <IconX className="h-5 w-5" />
              </button>
            </div>
            <div className="p-4 overflow-auto max-h-[calc(85vh-80px)]">
              <CodeBlock
                language="python"
                filename={codeModalMessage.filename || "animation.py"}
                code={codeModalMessage.code}
              />
            </div>
          </div>
        </div>
      )}

      {/* Logout Confirmation Modal */}
      <ConfirmationModal
        isOpen={isLogoutModalOpen}
        onClose={() => setIsLogoutModalOpen(false)}
        onConfirm={confirmLogout}
        title="Logout"
        message="Are you sure you want to log out? You will need to sign in again to access your projects."
        confirmText="Logout"
        isDanger={true}
      />
    </div>
  );
}