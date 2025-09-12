import { useState, useCallback, useMemo, memo, useEffect } from "react";
import { PlaceholdersAndVanishInput } from "@/components/ui/placeholders-and-vanish-input";
import { Sidebar, SidebarBody } from "@/components/ui/sidebar";
import { BackgroundBeams } from "@/components/ui/background-beams";
import { useAuth } from "@/contexts/AuthContext";
import { IconPlus, IconUser, IconLogout, IconMenu2, IconDownload } from "@tabler/icons-react";
import type { ManimGenerationRequest, TaskResultResponse } from '@/types/api';
import { ManimApiService } from '@/services/manimApi';

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
const SuggestionButton = memo(({ suggestion, onClick }: { suggestion: string, onClick: (suggestion: string) => void }) => (
  <button
    onClick={() => onClick(suggestion)}
    className="p-3 md:p-4 bg-gray-800 hover:bg-gray-700 rounded-xl border border-gray-700 text-white text-left transition-all duration-200 hover:border-gray-600 w-full"
  >
    <p className="text-xs md:text-sm">{suggestion}</p>
  </button>
));

const Message = memo(({ message }: { message: { type: 'user' | 'assistant', content: string, taskId?: string, videoUrl?: string, progress?: number, stage?: string } }) => (
  <div className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
    <div
      className={`max-w-[85%] md:max-w-3xl p-3 md:p-4 rounded-lg ${
        message.type === 'user'
          ? 'bg-blue-600 text-white'
          : 'bg-gray-800 text-white shadow-lg border border-gray-700'
      }`}
    >
      <p className="whitespace-pre-wrap break-words text-sm md:text-base mb-2 leading-relaxed">{message.content}</p>
      
      {/* Progress bar for assistant messages with tasks */}
      {message.type === 'assistant' && message.taskId && typeof message.progress === 'number' && message.progress < 100 && (
        <div className="mt-3">
          <div className="flex justify-between text-xs text-gray-300 mb-1">
            <span>{message.stage || 'Processing'}</span>
            <span>{message.progress}%</span>
          </div>
          <div className="w-full bg-gray-700 rounded-full h-2">
            <div 
              className="bg-blue-600 h-2 rounded-full transition-all duration-500" 
              style={{ width: `${message.progress}%` }}
            ></div>
          </div>
        </div>
      )}

      {/* Video player for completed animations */}
      {message.type === 'assistant' && message.videoUrl && (
        <div className="mt-3 flex flex-col items-center">
          <video 
            controls 
            className="w-full max-w-md rounded-lg"
            poster=""
          >
            <source src={message.videoUrl} type="video/mp4" />
            Your browser does not support the video tag.
          </video>
          <div className="mt-2 flex gap-2">
            <a 
              href={message.videoUrl} 
              download
              className="inline-flex items-center gap-1 px-3 py-1 bg-blue-600 hover:bg-blue-700 rounded text-xs transition-colors"
            >
              <IconDownload className="h-3 w-3" />
              Download
            </a>
          </div>
        </div>
      )}
    </div>
  </div>
));

export default function MainPage() {
  const [messages, setMessages] = useState<Array<{ type: 'user' | 'assistant', content: string, taskId?: string, videoUrl?: string, progress?: number, stage?: string }>>([]);
  const [isGenerating, setIsGenerating] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [currentHistoryId, setCurrentHistoryId] = useState<string>("");
  const [currentTaskId, setCurrentTaskId] = useState<string>("");
  const [inputValue, setInputValue] = useState<string>(""); // Add state for input value
  const [pollingInterval, setPollingInterval] = useState<NodeJS.Timeout | null>(null);
  const { user, logout, tokens } = useAuth();

  const startTaskPolling = useCallback(async (taskId: string) => {
    if (!tokens?.accessToken) return;

    const pollTask = async () => {
      try {
        const result = await ManimApiService.pollTaskStatus(taskId, tokens.accessToken);
        
        // Update the message with progress
        setMessages(prev => prev.map(msg => 
          msg.taskId === taskId 
            ? { 
                ...msg, 
                progress: result.progress,
                stage: result.current_stage,
                content: result.status === 'completed' && result.data?.success
                  ? `✅ Animation completed successfully! Your "${result.data.chat_name}" is ready.`
                  : result.status === 'failed'
                  ? `❌ Animation generation failed. Please try again.`
                  : `🔄 ${result.current_stage || 'Processing'} (${result.progress || 0}%)`
              }
            : msg
        ));

        if (result.status === 'completed') {
          if (result.data?.success) {
            // Update history ID from the result
            if (result.data.historyId) {
              setCurrentHistoryId(result.data.historyId);
              console.log('History ID updated from result:', result.data.historyId);
            }

            // Add the video to the message
            setMessages(prev => prev.map(msg => 
              msg.taskId === taskId 
                ? { 
                    ...msg, 
                    videoUrl: result.data?.link,
                    content: `✅ Animation completed successfully! Your "${result.data?.chat_name}" is ready.`
                  }
                : msg
            ));
          }
          
          setIsGenerating(false);
          if (pollingInterval) {
            clearInterval(pollingInterval);
            setPollingInterval(null);
          }
        } else if (result.status === 'failed') {
          setIsGenerating(false);
          if (pollingInterval) {
            clearInterval(pollingInterval);
            setPollingInterval(null);
          }
        }
      } catch (error) {
        console.error('Polling error:', error);
        
        // Update message to show polling failed
        setMessages(prev => prev.map(msg => 
          msg.taskId === taskId 
            ? { 
                ...msg, 
                content: `⚠️ Unable to track progress. Task ID: ${taskId}. Please check back later.`
              }
            : msg
        ));
        
        setIsGenerating(false);
        if (pollingInterval) {
          clearInterval(pollingInterval);
          setPollingInterval(null);
        }
      }
    };

    // Start polling immediately
    await pollTask();
    
    // Set up interval for continued polling
    const interval = setInterval(pollTask, 3000); // Poll every 3 seconds
    setPollingInterval(interval);
  }, [tokens?.accessToken, pollingInterval]);

  // Cleanup polling on unmount
  useEffect(() => {
    return () => {
      if (pollingInterval) {
        clearInterval(pollingInterval);
      }
    };
  }, [pollingInterval]);

  const toggleSidebar = useCallback(() => setSidebarOpen(prev => !prev), []);

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

  const processSubmission = useCallback(async (text: string) => {
    // Add null check and trim validation
    if (!text || !text.trim()) return;

    const userMessage = { type: 'user' as const, content: text.trim() };
    setMessages(prev => [...prev, userMessage]);
    setIsGenerating(true);

    try {
      // Check if user has access token
      if (!tokens?.accessToken) {
        throw new Error('Authentication required. Please log in again.');
      }

      // Prepare the API request payload
      const requestPayload: ManimGenerationRequest = {
        userQuery: text.trim(),
        format: "mp4",
        quality: "ql", 
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

      // Add assistant response with task ID for tracking
      const isNewChat = !currentHistoryId;
      const assistantMessage = {
        type: 'assistant' as const,
        content: `🔄 Starting animation generation for "${text.trim()}"...`,
        taskId: response.task_id,
        progress: 0,
        stage: "Initializing"
      };
      setMessages(prev => [...prev, assistantMessage]);

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

      const errorResponseMessage = {
        type: 'assistant' as const,
        content: errorMessage
      };
      setMessages(prev => [...prev, errorResponseMessage]);
      setIsGenerating(false); // Only set to false on API call failure
    }
    // Note: Don't set setIsGenerating(false) in finally - let polling handle it for successful submissions
  }, [currentHistoryId, tokens?.accessToken, startTaskPolling]);

  const onInputSubmit = (e: React.FormEvent<HTMLFormElement>) => {
      e.preventDefault();
      
      if (inputValue && inputValue.trim()) {
        processSubmission(inputValue.trim());
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
              {messages.map((msg, i) => <Message key={i} message={msg} />)}
              {isGenerating && (
                <div className="flex justify-start">
                  <div className="bg-gray-800 text-white p-3 md:p-4 rounded-lg shadow-lg max-w-3xl border border-gray-700">
                    <div className="flex items-center space-x-2">
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
                      <span className="text-sm md:text-base">Processing your animation request...</span>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
        <div className="p-4 md:p-6 bg-gradient-to-t from-black to-transparent relative z-10">
          <div className="max-w-4xl mx-auto">
            {/* Debug indicator - remove in production */}
            {messages.length > 0 && (
              <div className="mb-2 text-xs text-gray-500 text-center">
                Chat Session: {currentHistoryId ? `ID: ${currentHistoryId.slice(0, 8)}...` : 'New Session'}
              </div>
            )}
            <PlaceholdersAndVanishInput
              placeholders={PLACEHOLDERS}
              onChange={handleInputChange}
              onSubmit={onInputSubmit}
            />
          </div>
        </div>
      </main>
    </div>
  );
}