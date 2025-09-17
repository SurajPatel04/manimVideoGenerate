import { useState, useCallback, useMemo, memo, useEffect, useRef } from "react";
import { PlaceholdersAndVanishInput } from "@/components/ui/placeholders-and-vanish-input";
import { Sidebar, SidebarBody } from "@/components/ui/sidebar";
import { BackgroundBeams } from "@/components/ui/background-beams";
import { CodeBlock } from "@/components/ui/code-block";
import { useAuth } from "@/contexts/AuthContext";
import { useNavigate } from "react-router-dom";
import { IconPlus, IconUser, IconLogout, IconMenu2, IconDownload, IconCode, IconX, IconHistory } from "@tabler/icons-react";
import type { ManimGenerationRequest, UserHistoryItem } from '@/types/api';
import { ManimApiService } from '@/services/manimApi';
import { Stepper, Step, StepLabel, Box } from '@mui/material';
import HistorySidebar from '@/components/HistorySidebar';
import '@/styles/scrollbar.css';

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
  "Show a 3D surface plot for sin(x) + cos(y)",
  "Visualize a 3D surface plot of z = x^2 + y^2 (a paraboloid)",

];

const PLACEHOLDERS = [
  "Create an animation showing the derivation of quadratic formula",
  "Generate a video explaining Newton's laws of motion with examples",
  "Make an animation about the water cycle and climate change",
];

const SuggestionButton = memo(({ suggestion, onClick }: { suggestion: string, onClick: (suggestion: string, options?: { format: string; quality: string }) => void }) => (
  <button
    onClick={() => onClick(suggestion, { format: "mp4", quality: "ql" })}
    className="p-3 md:p-4 bg-gray-800 hover:bg-gray-700 rounded-xl border border-gray-700 text-white text-left transition-all duration-200 hover:border-gray-600 w-full"
  >
    <p className="text-xs md:text-sm">{suggestion}</p>
  </button>
));

const ProgressStepper = memo(({ progress }: { progress?: number }) => {
  const steps = [
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
    <Box sx={{ 
      width: '100%', 
      mt: 2, 
      mb: 2,
      backgroundColor: 'transparent',
      '& .MuiStepper-root': {
        backgroundColor: 'transparent',
        padding: 0,
      }
    }}>
      <Stepper 
        activeStep={activeStep} 
        alternativeLabel
        sx={{
          backgroundColor: 'transparent',
          width: '100%',
          '& .MuiStepConnector-root': {
            top: 22,
            left: 'calc(-50% + 16px)',
            right: 'calc(50% + 16px)',
            '& .MuiStepConnector-line': {
              borderColor: '#4B5563', 
              borderTopWidth: 2,
            }
          },
          '& .MuiStepConnector-active .MuiStepConnector-line': {
            borderColor: '#3B82F6',
          },
          '& .MuiStepConnector-completed .MuiStepConnector-line': {
            borderColor: '#10B981',
          }
        }}
      >
        {steps.map((label) => (
          <Step key={label} sx={{ padding: 0 }}>
            <StepLabel 
              sx={{
                '& .MuiStepLabel-label': {
                  color: '#9CA3AF',
                  fontSize: '0.75rem',
                  marginTop: '8px',
                },
                '& .MuiStepLabel-label.Mui-active': {
                  color: '#3B82F6',
                  fontWeight: 600,
                },
                '& .MuiStepLabel-label.Mui-completed': {
                  color: '#10B981',
                },
                '& .MuiStepIcon-root': {
                  color: '#4B5563', 
                  fontSize: '1.5rem',
                },
                '& .MuiStepIcon-root.Mui-active': {
                  color: '#3B82F6',
                },
                '& .MuiStepIcon-root.Mui-completed': {
                  color: '#10B981',
                },
              }}
            >
              {label}
            </StepLabel>
          </Step>
        ))}
      </Stepper>
    </Box>
  );
});

const Message = memo(({ message, onCodeModalToggle }: { 
  message: MessageType,
  onCodeModalToggle: (isOpen: boolean, message?: MessageType | null) => void 
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
          <a 
            href={message.videoUrl} 
            download
            className="inline-flex items-center gap-1 px-3 py-1 bg-blue-600 hover:bg-blue-700 rounded text-xs transition-colors flex-shrink-0"
          >
            <IconDownload className="h-3 w-3 flex-shrink-0" />
            <span className="whitespace-nowrap">Download {isGif ? 'GIF' : 'Video'}</span>
          </a>
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
      <div className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
        <div
          className={`max-w-[85%] md:max-w-3xl p-3 md:p-4 rounded-lg ${
            message.type === 'user'
              ? 'bg-blue-600 text-white'
              : 'bg-gray-800 text-white shadow-lg border border-gray-700'
          }`}
        >
          <p className="whitespace-pre-wrap break-words text-sm md:text-base mb-2 leading-relaxed">{message.content}</p>
          
          {stepperSection}

          {videoSection}
        </div>
      </div>

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
  const [currentTaskId, setCurrentTaskId] = useState<string>("");
  const [inputValue, setInputValue] = useState<string>(""); 
  const [pollingInterval, setPollingInterval] = useState<NodeJS.Timeout | null>(null);
  const [isCodeModalOpen, setIsCodeModalOpen] = useState(false); 
  const [codeModalMessage, setCodeModalMessage] = useState<MessageType | null>(null);
  const [cancelledTasks, setCancelledTasks] = useState<Set<string>>(new Set()); 
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
    const maxInterval = 30000; 
    const maxPollCount = 300; 
    const calculateInterval = () => {

      const backoff = Math.min(baseInterval * Math.pow(1.5, consecutiveErrors), maxInterval);
      const jitter = Math.random() * 1000;
      return backoff + jitter;
    };

    const pollTask = async () => {
      try {
        pollCount++;
        
        if (cancelledTasks.has(taskId)) {
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
      const interval = calculateInterval();
      
      setTimeout(async () => {
        const shouldStop = await pollTask();
        if (!shouldStop) {
          scheduleNextPoll();
        } else {
          setPollingInterval(null);
        }
      }, interval);
    };

    scheduleNextPoll();
  }, [tokens?.accessToken]);

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
  }, []);

  const stopPollingAndReset = useCallback(() => {
    if (pollingInterval) {
      clearInterval(pollingInterval);
      setPollingInterval(null);
    }
    setIsGenerating(false);
    setCurrentTaskId("");
  }, [pollingInterval]);

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
    
    if (pollingInterval) {
      clearInterval(pollingInterval);
      setPollingInterval(null);
    }
    
    setShowUserMenu(false);
  }, [pollingInterval]);

  const handleLogout = useCallback((e?: React.MouseEvent) => {
    e?.preventDefault();
    e?.stopPropagation();
    try {
      logout();
      setShowUserMenu(false);
      navigate('/login', { replace: true });
    } catch (error) {
      console.error('Logout error:', error);
      setShowUserMenu(false);
      navigate('/login', { replace: true });
    }
  }, [logout, navigate]);

  const toggleUserMenu = useCallback(() => setShowUserMenu(prev => !prev), []);

  const processSubmission = useCallback(async (text: string, options: { format: string; quality: string } = { format: "mp4", quality: "ql" }) => {
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
      content: `Starting animation generation for "${text.trim()}"...`,
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
        historyId: currentHistoryId
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

  const onInputSubmit = (e: React.FormEvent<HTMLFormElement>, options: { format: string; quality: string }) => {
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
    <div className="min-h-screen w-screen flex bg-black">
      {/* Mobile Header */}
      <div className="md:hidden fixed top-0 left-0 right-0 z-50 bg-[#171717] border-b border-gray-700 p-4 flex items-center justify-between">
        <button
          onClick={toggleSidebar}
          className="p-2 hover:bg-gray-700 rounded-lg transition-colors"
        >
          <IconMenu2 className="text-white h-5 w-5" />
        </button>
        <h1 className="text-white text-lg font-semibold">Manim Generator</h1>
        <button
          onClick={handleNewChat}
          className="p-2 hover:bg-gray-700 rounded-lg transition-colors"
        >
          <IconPlus className="text-white h-5 w-5" />
        </button>
      </div>

      {/* Mobile Sidebar Overlay */}
      {sidebarOpen && (
        <div 
          className="md:hidden fixed inset-0 bg-black bg-opacity-50 z-40"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Desktop Sidebar */}
      <div className="hidden md:block fixed top-0 left-0 h-screen z-30">
        <Sidebar open={sidebarOpen} setOpen={setSidebarOpen}>
          <SidebarBody className="justify-between gap-10 h-full">
            <div className="flex flex-col h-full min-h-0">
              <div className="flex-shrink-0 space-y-2 px-2 py-2">
                <div className={`flex-shrink-0 ${sidebarOpen ? '' : 'flex justify-center'}`}>
                    <button
                        onClick={toggleSidebar}
                        className="p-2 hover:bg-gray-700 rounded-lg cursor-pointer transition-colors"
                    >
                        <IconMenu2 className="text-white h-5 w-5" />
                    </button>
                </div>
                <button
                  onClick={handleNewChat}
                  className={`flex items-center gap-2 p-2 hover:bg-gray-700 rounded-lg cursor-pointer transition-colors w-full ${sidebarOpen ? 'text-left' : 'justify-center'}`}
                >
                  <IconPlus className="text-white h-5 w-5 shrink-0" />
                  <span className={`text-white text-sm transition-opacity duration-200 ${sidebarOpen ? 'opacity-100' : 'opacity-0 hidden'}`}>New chat</span>
                </button>
              </div>
              
              {/* History Section */}
              {sidebarOpen && (
                <div className="flex-1 min-h-0 mt-4">
                  <div className="mb-3 px-2">
                    <div className="flex items-center gap-2 px-2 py-1">
                      <IconHistory className="h-4 w-4 text-gray-400" />
                      <span className="text-xs text-gray-400 font-medium">Recent</span>
                    </div>
                  </div>
                  <div className="overflow-y-auto px-2 max-h-[calc(100vh-220px)] pr-1 sidebar-scrollbar">
                    <HistorySidebar 
                        isOpen={true}
                        onToggle={() => {}}
                        onHistoryItemClick={handleHistoryItemClick}
                        inMainSidebar={true}
                        currentHistoryId={currentHistoryId}
                    />
                  </div>
                </div>
              )}
            </div>
            <div className="relative flex-shrink-0 px-2 pb-2" ref={userMenuRef}>
              <button
                onClick={toggleUserMenu}
                className={`flex items-center gap-2 p-2 hover:bg-gray-700 rounded-lg cursor-pointer transition-colors w-full ${sidebarOpen ? 'text-left' : 'justify-center'}`}
              >
                <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center shrink-0">
                  <IconUser className="text-white h-4 w-4" />
                </div>
                <span className={`text-white text-sm truncate transition-opacity duration-200 ${sidebarOpen ? 'opacity-100' : 'opacity-0 hidden'}`}>{user?.firstName || 'User'}</span>
              </button>
              {showUserMenu && sidebarOpen && (
                <div className="absolute bottom-full left-0 right-0 mb-2 bg-gray-800 border border-gray-600 rounded-lg shadow-lg z-50">
                  <button
                    onClick={handleLogout}
                    onMouseDown={(e) => e.stopPropagation()}
                    className="w-full flex items-center gap-2 p-3 hover:bg-gray-700 rounded-lg transition-colors text-white text-sm cursor-pointer"
                    type="button"
                  >
                    <IconLogout className="h-4 w-4 shrink-0" />
                    Logout
                  </button>
                </div>
              )}
              {showUserMenu && !sidebarOpen && (
                <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 bg-gray-800 border border-gray-600 rounded-lg shadow-lg z-50 whitespace-nowrap">
                  <button
                    onClick={handleLogout}
                    onMouseDown={(e) => e.stopPropagation()}
                    className="flex items-center gap-2 p-3 hover:bg-gray-700 rounded-lg transition-colors text-white text-sm cursor-pointer"
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
      </div>

      {/* Mobile Sidebar */}
      <div className={`md:hidden fixed top-0 left-0 h-screen bg-[#171717] border-r border-gray-700 z-50 transform transition-transform duration-300 ${
        sidebarOpen ? 'translate-x-0' : '-translate-x-full'
      } w-64`}>
        <div className="flex flex-col h-full justify-between p-4">
          <div className="flex flex-col gap-4 min-h-0">
            <div className="flex items-center justify-between flex-shrink-0">
              <h2 className="text-white text-lg font-semibold">Menu</h2>
              <button
                onClick={() => setSidebarOpen(false)}
                className="p-2 hover:bg-gray-700 rounded-lg transition-colors"
              >
                <IconMenu2 className="text-white h-5 w-5" />
              </button>
            </div>
            <button
              onClick={handleNewChat}
              className="flex items-center gap-3 p-3 hover:bg-gray-700 rounded-lg transition-colors w-full text-left flex-shrink-0"
            >
              <IconPlus className="text-white h-5 w-5" />
              <span className="text-white text-sm">New chat</span>
            </button>
            {/* History Section for Mobile */}
            <div className="flex-1 min-h-0">
              <div className="mb-3 px-2">
                <div className="flex items-center gap-2 px-2 py-1">
                  <IconHistory className="h-4 w-4 text-gray-400" />
                  <span className="text-xs text-gray-400 font-medium">Recent</span>
                </div>
              </div>
              <div className="overflow-y-auto px-2 max-h-[calc(100vh-220px)] pr-1 sidebar-scrollbar">
                <HistorySidebar 
                  isOpen={true}
                  onToggle={() => {}}
                  onHistoryItemClick={handleHistoryItemClick}
                  inMainSidebar={true}
                  currentHistoryId={currentHistoryId}
                />
              </div>
            </div>
          </div>
          <div className="relative flex-shrink-0" ref={mobileUserMenuRef}>
            <button
              onClick={toggleUserMenu}
              className="flex items-center gap-3 p-3 hover:bg-gray-700 rounded-lg transition-colors w-full text-left"
            >
              <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
                <IconUser className="text-white h-4 w-4" />
              </div>
              <span className="text-white text-sm">{user?.firstName || 'User'}</span>
            </button>
            {showUserMenu && (
              <div className="absolute bottom-full left-0 right-0 mb-2 bg-gray-800 border border-gray-600 rounded-lg shadow-lg">
                <button
                  onClick={handleLogout}
                  onMouseDown={(e) => e.stopPropagation()}
                  className="w-full flex items-center gap-3 p-3 hover:bg-gray-700 rounded-lg transition-colors text-white text-sm cursor-pointer"
                  type="button"
                >
                  <IconLogout className="h-4 w-4" />
                  Logout
                </button>
              </div>
            )}
          </div>
        </div>
      </div>

      <main className={`flex-1 flex flex-col min-w-0 pt-16 md:pt-0 relative min-h-screen transition-all duration-300 ${
        sidebarOpen ? 'md:ml-[300px]' : 'md:ml-[60px]'
      }`}>
        <BackgroundBeams />
  <div className="flex-1 p-4 md:p-6 relative z-10 pb-20 md:pb-24 overflow-y-auto">
          {messages.length === 0 ? (
            <div className="flex flex-col items-center justify-center min-h-[60vh]">
              <div className="w-full max-w-3xl px-2">
                <div className="grid grid-cols-1 gap-3 md:gap-4">
                  {suggestionButtons}
                </div>
              </div>
            </div>
          ) : (
            <div className="space-y-4 md:space-y-6 max-w-4xl mx-auto pb-8 md:pb-12">
              {messages.map((msg) => (
                <Message 
                  key={msg.id} 
                  message={msg} 
                  onCodeModalToggle={(isOpen: boolean, message?: MessageType | null) => {
                    setIsCodeModalOpen(isOpen);
                    setCodeModalMessage(message ?? null);
                  }}
                />
              ))}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>
        {!isCodeModalOpen && (
          <div className={`fixed bottom-0 right-0 p-4 md:p-6 bg-gradient-to-t from-black via-black/95 to-transparent z-20 transition-all duration-300 ${
            sidebarOpen ? 'left-0 md:left-[300px]' : 'left-0 md:left-[60px]'
          }`}>
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
    </div>
  );
}