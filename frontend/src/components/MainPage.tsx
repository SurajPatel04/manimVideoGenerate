import { useState, useCallback, useMemo, memo, useEffect, useRef } from "react";
import { PlaceholdersAndVanishInput } from "@/components/ui/placeholders-and-vanish-input";
import { Sidebar, SidebarBody } from "@/components/ui/sidebar";
import { BackgroundBeams } from "@/components/ui/background-beams";
import { CodeBlock } from "@/components/ui/code-block";
import { useAuth } from "@/contexts/AuthContext";
import { IconPlus, IconUser, IconLogout, IconMenu2, IconDownload, IconCode, IconX } from "@tabler/icons-react";
import type { ManimGenerationRequest } from '@/types/api';
import { ManimApiService } from '@/services/manimApi';
import { Stepper, Step, StepLabel, Box } from '@mui/material';

// Types for better performance
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
  id: string; // Add unique ID for better list rendering
}

// Constants
const SUGGESTION_PROMPTS = [
  "Create an animation showing the derivation of quadratic formula",
  "Generate a video explaining Newton's laws of motion with examples",
  "Make an animation about the water cycle and climate change",

];

const PLACEHOLDERS = [
  "Create an animation showing the derivation of quadratic formula",
  "Generate a video explaining Newton's laws of motion with examples",
  "Make an animation about the water cycle and climate change",
];

// Memoized Components for performance
const SuggestionButton = memo(({ suggestion, onClick }: { suggestion: string, onClick: (suggestion: string, options?: { format: string; quality: string }) => void }) => (
  <button
    onClick={() => onClick(suggestion, { format: "mp4", quality: "ql" })}
    className="p-3 md:p-4 bg-gray-800 hover:bg-gray-700 rounded-xl border border-gray-700 text-white text-left transition-all duration-200 hover:border-gray-600 w-full"
  >
    <p className="text-xs md:text-sm">{suggestion}</p>
  </button>
));

// Progress Stepper Component
const ProgressStepper = memo(({ progress }: { progress?: number }) => {
  const steps = [
    'Setting up description generation state',
    'Analyzing if user query is possible',
    'Detailed description in progress',
    'Creating animation code',
    'Video generation completed successfully'
  ];

  // Determine active step based on progress from backend
  const getActiveStep = () => {
    const currentProgress = progress || 0;
    if (currentProgress <= 10) return 0;      // Step 1: 0-10%
    if (currentProgress <= 20) return 1;      // Step 2: 10-20%
    if (currentProgress <= 30) return 2;      // Step 3: 20-30%
    if (currentProgress <= 50) return 3;      // Step 4: 30-50%
    return 4; // Step 5: 50-100%
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
              borderColor: '#4B5563', // gray-600
              borderTopWidth: 2,
            }
          },
          '& .MuiStepConnector-active .MuiStepConnector-line': {
            borderColor: '#3B82F6', // blue-500
          },
          '& .MuiStepConnector-completed .MuiStepConnector-line': {
            borderColor: '#10B981', // green-500
          }
        }}
      >
        {steps.map((label) => (
          <Step key={label} sx={{ padding: 0 }}>
            <StepLabel 
              sx={{
                '& .MuiStepLabel-label': {
                  color: '#9CA3AF', // gray-400
                  fontSize: '0.75rem', // text-xs
                  marginTop: '8px',
                },
                '& .MuiStepLabel-label.Mui-active': {
                  color: '#3B82F6', // blue-500
                  fontWeight: 600,
                },
                '& .MuiStepLabel-label.Mui-completed': {
                  color: '#10B981', // green-500
                },
                '& .MuiStepIcon-root': {
                  color: '#4B5563', // gray-600
                  fontSize: '1.5rem',
                },
                '& .MuiStepIcon-root.Mui-active': {
                  color: '#3B82F6', // blue-500
                },
                '& .MuiStepIcon-root.Mui-completed': {
                  color: '#10B981', // green-500
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
  onCodeModalToggle: (isOpen: boolean) => void 
}) => {
  const [showCode, setShowCode] = useState(false);

  const handleShowCode = useCallback(() => {
    setShowCode(true);
    onCodeModalToggle(true);
  }, [onCodeModalToggle]);

  const handleHideCode = useCallback(() => {
    setShowCode(false);
    onCodeModalToggle(false);
  }, [onCodeModalToggle]);

  // Memoize video/gif section to prevent unnecessary re-renders
  const videoSection = useMemo(() => {
    if (message.type !== 'assistant' || !message.videoUrl || message.success === false) {
      return null;
    }

    // Check if the URL is a GIF file
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
            preload="metadata" // Optimize video loading
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

  // Memoize stepper section
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
          
          {/* Material UI Stepper for assistant messages with tasks */}
          {stepperSection}

          {/* Video player for completed animations */}
          {videoSection}
        </div>
      </div>

      {/* Code Modal */}
      {showCode && message.code && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
          onClick={handleHideCode}
        >
          <div 
            className="bg-gray-900 rounded-lg max-w-4xl w-full max-h-[80vh] overflow-hidden"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center justify-between p-4 border-b border-gray-700">
              <h3 className="text-white text-lg font-semibold">Generated Animation Code</h3>
              <button
                onClick={handleHideCode}
                className="text-gray-400 hover:text-white transition-colors"
              >
                <IconX className="h-5 w-5" />
              </button>
            </div>
            <div className="p-4 overflow-auto max-h-[calc(80vh-80px)]">
              <CodeBlock
                language="python"
                filename={message.filename || "animation.py"}
                code={message.code}
              />
            </div>
          </div>
        </div>
      )}
    </>
  );
}, (prevProps, nextProps) => {
  // Custom comparison function for better memoization
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
  const [inputValue, setInputValue] = useState<string>(""); // Add state for input value
  const [pollingInterval, setPollingInterval] = useState<NodeJS.Timeout | null>(null);
  const [isCodeModalOpen, setIsCodeModalOpen] = useState(false); // Track if any code modal is open
  const { user, logout, tokens } = useAuth();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Utility function to generate unique IDs
  const generateMessageId = useCallback(() => `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`, []);

  const startTaskPolling = useCallback(async (taskId: string) => {
    if (!tokens?.accessToken) return;

    let pollCount = 0;
    let consecutiveErrors = 0;
    const maxRetries = 3;
    const baseInterval = 2000; // Start with 2 seconds
    const maxInterval = 30000; // Max 30 seconds
    const maxPollCount = 300; // Stop after 10 minutes (300 * 2s average)

    const calculateInterval = () => {
      // Exponential backoff with jitter
      const backoff = Math.min(baseInterval * Math.pow(1.5, consecutiveErrors), maxInterval);
      const jitter = Math.random() * 1000; // Add up to 1 second jitter
      return backoff + jitter;
    };

    const pollTask = async () => {
      try {
        pollCount++;
        
        // Safety check to prevent infinite polling
        if (pollCount > maxPollCount) {
          console.warn('Polling timeout reached, stopping polling');
          setMessages(prev => prev.map(msg => 
            msg.taskId === taskId 
              ? { 
                  ...msg, 
                  content: '⏰ Polling timeout. The task may still be processing on the server.'
                }
              : msg
          ));
          setIsGenerating(false);
          return true;
        }

        const result = await ManimApiService.pollTaskStatus(taskId, tokens.accessToken);
        console.log(`Polling #${pollCount} - Status: ${result.status}, Progress: ${result.progress}%`);
        
        // Reset error count on successful response
        consecutiveErrors = 0;
        
        // Update the message with progress
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
                  : `${result.current_stage || 'Processing'} (${result.progress || 0}%)`
              }
            : msg
        ));

        // Check if task is completed or failed and stop polling
        if (result.status === 'completed' || result.status === 'failed') {
          console.log(`Polling completed after ${pollCount} attempts - Status: ${result.status}`);
          
          // Set generating to false
          setIsGenerating(false);
          
          if (result.status === 'completed') {
            // Check if the task was successful or failed based on data.success
            if (result.data?.success) {
              // Update history ID from the result
              if (result.data.historyId) {
                setCurrentHistoryId(result.data.historyId);
                console.log('History ID updated from result:', result.data.historyId);
              }

              // Add the video to the message for successful completion
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
              // Handle failure case where data.success is false
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
            // Handle system-level failure
            setMessages(prev => prev.map(msg => 
              msg.taskId === taskId 
                ? { 
                    ...msg, 
                    content: `❌ Animation generation failed. Please try again.`,
                    success: false
                  }
                : msg
            ));
          }
          
          // Return true to indicate polling should stop
          return true;
        }
        
        // Return false to continue polling
        return false;
      } catch (error) {
        consecutiveErrors++;
        console.error(`Polling error #${consecutiveErrors}:`, error);
        
        // Stop polling after max consecutive errors
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
        
        // Update message to show retry attempt
        setMessages(prev => prev.map(msg => 
          msg.taskId === taskId 
            ? { 
                ...msg, 
                content: `Connection issue (${consecutiveErrors}/${maxRetries}). Retrying...`
              }
            : msg
        ));
        
        // Continue polling with backoff
        return false;
      }
    };

    // Start polling immediately
    const shouldStop = await pollTask();
    if (shouldStop) {
      console.log('Task already completed, not setting up interval');
      return; // Don't set up interval if already completed
    }
    
    // Set up dynamic interval polling with exponential backoff
    const scheduleNextPoll = () => {
      const interval = calculateInterval();
      console.log(`Scheduling next poll in ${Math.round(interval)}ms`);
      
      setTimeout(async () => {
        const shouldStop = await pollTask();
        if (!shouldStop) {
          scheduleNextPoll(); // Schedule the next poll
        } else {
          console.log('Polling sequence completed');
          setPollingInterval(null);
        }
      }, interval);
    };

    scheduleNextPoll();
  }, [tokens?.accessToken]);

  // Cleanup polling on unmount
  useEffect(() => {
    return () => {
      if (pollingInterval) {
        clearInterval(pollingInterval);
      }
    };
  }, [pollingInterval]);

  // Auto-scroll to bottom when messages change (optimized)
  useEffect(() => {
    const scrollToBottom = () => {
      messagesEndRef.current?.scrollIntoView({ 
        behavior: 'smooth',
        block: 'nearest'
      });
    };
    
    // Only scroll if not too many messages to avoid performance issues
    if (messages.length < 50) {
      const timeoutId = setTimeout(scrollToBottom, 150);
      return () => clearTimeout(timeoutId);
    }
  }, [messages.length]); // Only depend on length, not entire messages array

  // Also scroll when generating state changes (for progress updates)
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

  const toggleSidebar = useCallback(() => setSidebarOpen(prev => !prev), []);

  // Cleanup function to stop polling and reset states
  const stopPollingAndReset = useCallback(() => {
    if (pollingInterval) {
      clearInterval(pollingInterval);
      setPollingInterval(null);
    }
    setIsGenerating(false);
    setCurrentTaskId("");
  }, [pollingInterval]);

  // Cancel task function
  const handleCancelTask = useCallback(async () => {
    if (!currentTaskId || !tokens?.accessToken) return;

    try {
      const response = await ManimApiService.cancelTask(currentTaskId, tokens.accessToken);
      console.log('Task cancelled:', response);

      // Stop polling and reset states
      stopPollingAndReset();

      // Update the message that was showing progress to show cancelled status
      setMessages(prev => prev.map(msg => 
        msg.taskId === currentTaskId 
          ? { 
              ...msg, 
              content: 'Animation generation has been cancelled.',
              progress: undefined,
              stage: undefined
            }
          : msg
      ));

    } catch (error: any) {
      console.error('Error cancelling task:', error);
      
      // Still stop the polling even if cancel API fails
      stopPollingAndReset();

      // Update the message that was showing progress to show local cancellation
      setMessages(prev => prev.map(msg => 
        msg.taskId === currentTaskId 
          ? { 
              ...msg, 
              content: 'Process stopped locally (may continue on server).',
              progress: undefined,
              stage: undefined
            }
          : msg
      ));
    }
  }, [currentTaskId, tokens?.accessToken, stopPollingAndReset]);

  const handleNewChat = useCallback(() => {
    console.log('Starting new chat - resetting history');
    setMessages([]);
    setCurrentHistoryId(""); // Reset history for new chat
    setCurrentTaskId(""); // Reset task ID for new chat
    setIsGenerating(false); // Reset generating state
    
    // Clear any active polling
    if (pollingInterval) {
      clearInterval(pollingInterval);
      setPollingInterval(null);
    }
    
    setShowUserMenu(false);
  }, [pollingInterval]);

  const handleLogout = useCallback(() => {
    logout();
    setShowUserMenu(false);
  }, [logout]);

  const toggleUserMenu = useCallback(() => setShowUserMenu(prev => !prev), []);

  const processSubmission = useCallback(async (text: string, options: { format: string; quality: string } = { format: "mp4", quality: "ql" }) => {
    // Add null check and trim validation
    if (!text || !text.trim()) return;

    const userMessage: MessageType = { 
      type: 'user', 
      content: text.trim(),
      id: generateMessageId()
    };
    setMessages(prev => [...prev, userMessage]);
    setIsGenerating(true);

    // Add assistant response with stepper immediately showing 0% progress
    const assistantMessage: MessageType = {
      type: 'assistant',
      content: `🔄 Starting animation generation for "${text.trim()}"...`,
      taskId: 'temp-id', // Temporary ID until we get real one
      progress: 0,
      stage: "Setting up description generation state",
      id: generateMessageId()
    };
    setMessages(prev => [...prev, assistantMessage]);

    try {
      // Check if user has access token
      if (!tokens?.accessToken) {
        throw new Error('Authentication required. Please log in again.');
      }

      // Prepare the API request payload
      const requestPayload: ManimGenerationRequest = {
        userQuery: text.trim(),
        format: options.format,
        quality: options.quality, 
        historyId: currentHistoryId // Empty string for new chat, otherwise existing historyId
      };

      // Log the request payload for debugging
      console.log('API Request:', {
        userQuery: text.trim(),
        historyId: currentHistoryId,
        isNewChat: currentHistoryId === ""
      });

      // Make API call to manim generation endpoint using the service
      const response = await ManimApiService.generateAnimation(requestPayload, tokens.accessToken);

      // Log the task ID as requested
      console.log('Task ID:', response.task_id);

      // Store the task ID for potential future use (status polling, etc.)
      setCurrentTaskId(response.task_id);

      // Update history ID if returned from API for subsequent requests in this chat
      if (response.historyId) {
        setCurrentHistoryId(response.historyId);
        console.log('History ID updated:', response.historyId);
      }

      // Update the message with the real task ID
      setMessages(prev => prev.map(msg => 
        msg.taskId === 'temp-id' 
          ? { ...msg, taskId: response.task_id }
          : msg
      ));

      // Start polling for task status
      startTaskPolling(response.task_id);

      // TODO: You might want to store the task_id for polling status later

    } catch (error: any) {
      console.error('Error generating manim animation:', error);
      
      // Handle specific error cases
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
      setIsGenerating(false); // Only set to false on API call failure
    }
    // Note: Don't set setIsGenerating(false) in finally - let polling handle it for successful submissions
  }, [currentHistoryId, tokens?.accessToken, startTaskPolling, generateMessageId]);

  const onInputSubmit = (e: React.FormEvent<HTMLFormElement>, options: { format: string; quality: string }) => {
      e.preventDefault();
      
      if (inputValue && inputValue.trim()) {
        processSubmission(inputValue.trim(), options);
        setInputValue(""); // Clear the input after submission
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
    <div className="h-screen w-screen flex bg-black overflow-hidden">
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
      <div className="hidden md:block">
        <Sidebar open={sidebarOpen} setOpen={setSidebarOpen}>
          <SidebarBody className="justify-between gap-10">
            <div className="flex flex-col gap-2">
              <div className={`flex-shrink-0 ${sidebarOpen ? 'p-2' : 'px-2 py-2 flex justify-center'}`}>
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
            <div className="relative">
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
                    className="w-full flex items-center gap-2 p-3 hover:bg-gray-700 rounded-lg transition-colors text-white text-sm"
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
                    className="flex items-center gap-2 p-3 hover:bg-gray-700 rounded-lg transition-colors text-white text-sm"
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
      <div className={`md:hidden fixed top-0 left-0 h-full bg-[#171717] border-r border-gray-700 z-50 transform transition-transform duration-300 ${
        sidebarOpen ? 'translate-x-0' : '-translate-x-full'
      } w-64`}>
        <div className="flex flex-col h-full justify-between p-4">
          <div className="flex flex-col gap-4">
            <div className="flex items-center justify-between">
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
              className="flex items-center gap-3 p-3 hover:bg-gray-700 rounded-lg transition-colors w-full text-left"
            >
              <IconPlus className="text-white h-5 w-5" />
              <span className="text-white text-sm">New chat</span>
            </button>
          </div>
          <div className="relative">
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
                  className="w-full flex items-center gap-3 p-3 hover:bg-gray-700 rounded-lg transition-colors text-white text-sm"
                >
                  <IconLogout className="h-4 w-4" />
                  Logout
                </button>
              </div>
            )}
          </div>
        </div>
      </div>

      <main className="flex-1 flex flex-col min-w-0 md:ml-0 pt-16 md:pt-0 relative">
        <BackgroundBeams />
        <div className="flex-1 overflow-y-auto p-4 md:p-6 relative z-10">
          {messages.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full">
              <div className="w-full max-w-3xl px-2">
                <div className="grid grid-cols-1 gap-3 md:gap-4">
                  {suggestionButtons}
                </div>
              </div>
            </div>
          ) : (
            <div className="space-y-4 md:space-y-6 max-w-4xl mx-auto">
              {messages.map((msg) => (
                <Message 
                  key={msg.id} 
                  message={msg} 
                  onCodeModalToggle={setIsCodeModalOpen}
                />
              ))}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>
        {!isCodeModalOpen && (
          <div className="p-4 md:p-6 bg-gradient-to-t from-black to-transparent relative z-10">
            <div className="max-w-4xl mx-auto">
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
    </div>
  );
}