import { useState, useCallback, useMemo, memo } from "react";
import { PlaceholdersAndVanishInput } from "@/components/ui/placeholders-and-vanish-input";
import { Sidebar, SidebarBody } from "@/components/ui/sidebar";
import { BackgroundBeams } from "@/components/ui/background-beams";
import { useAuth } from "@/contexts/AuthContext";
import { IconPlus, IconUser, IconLogout, IconMenu2 } from "@tabler/icons-react";

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

const Message = memo(({ message }: { message: { type: 'user' | 'assistant', content: string } }) => (
  <div className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
    <div
      className={`max-w-[85%] md:max-w-3xl p-3 md:p-4 rounded-lg ${
        message.type === 'user'
          ? 'bg-blue-600 text-white'
          : 'bg-gray-800 text-white shadow-lg border border-gray-700'
      }`}
    >
      <p className="whitespace-pre-wrap text-sm md:text-base">{message.content}</p>
    </div>
  </div>
));

export default function MainPage() {
  const [messages, setMessages] = useState<Array<{ type: 'user' | 'assistant', content: string }>>([]);
  const [isGenerating, setIsGenerating] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [showUserMenu, setShowUserMenu] = useState(false);
  const { user, logout } = useAuth();

  const toggleSidebar = useCallback(() => setSidebarOpen(prev => !prev), []);

  const handleNewChat = useCallback(() => {
    setMessages([]);
    setShowUserMenu(false);
  }, []);

  const handleLogout = useCallback(() => {
    logout();
    setShowUserMenu(false);
  }, [logout]);

  const toggleUserMenu = useCallback(() => setShowUserMenu(prev => !prev), []);

  const processSubmission = useCallback(async (text: string) => {
    if (!text.trim()) return;

    const userMessage = { type: 'user' as const, content: text };
    setMessages(prev => [...prev, userMessage]);
    setIsGenerating(true);

    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 2000));
      const assistantMessage = {
        type: 'assistant' as const,
        content: `I'll help you create an animation about "${text}". Let me generate the Manim code and video for you.`
      };
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setIsGenerating(false);
    }
  }, []);

  const onInputSubmit = (e: React.FormEvent<HTMLFormElement>) => {
      e.preventDefault();
      const formData = new FormData(e.target as HTMLFormElement);
      const value = formData.get('input') as string;
      processSubmission(value);
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
                      <span className="text-sm md:text-base">Generating your animation...</span>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
        <div className="p-4 md:p-6 bg-gradient-to-t from-black to-transparent relative z-10">
          <div className="max-w-4xl mx-auto">
            <PlaceholdersAndVanishInput
              placeholders={PLACEHOLDERS}
              onChange={() => {}}
              onSubmit={onInputSubmit}
            />
          </div>
        </div>
      </main>
    </div>
  );
}