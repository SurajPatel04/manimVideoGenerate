import { Link } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import { LayoutTextFlip } from '@/components/ui/layout-text-flip';
import { IconBrandGithub, IconBrandLinkedin } from '@tabler/icons-react';

export default function Homepage() {
  const { isAuthenticated } = useAuth();

  const showcaseItems = [
    {
      prompt: "Create a 3D surface plot of the function z = sin(x) * cos(y) using a grid",
      gif: "/generatedManim.gif",
      description: "3D mathematical visualizations"
    },
    {
      prompt: "Show a 3D surface plot for sin(x) + cos(y)",
      gif: "/generatedManimVideo.gif",
      description: "Complex mathematical functions made simple"
    }
  ];

  return (
    <div className="relative z-10 min-h-screen">
      {/* Top-corner social icons: LinkedIn left-top, GitHub right-top */}
  <div className="absolute left-4 top-4 z-50">
        <a
          href="https://www.linkedin.com/"
          target="_blank"
          rel="noreferrer"
          className="text-neutral-300 hover:text-blue-500 transition-colors bg-transparent p-0 m-0 shadow-none focus:outline-none focus:ring-0"
          aria-label="LinkedIn"
          style={{ background: 'transparent' }}
        >
          <IconBrandLinkedin className="w-6 h-6" />
        </a>
      </div>

  <div className="absolute right-4 top-4 z-50">
        <a
          href="https://github.com/"
          target="_blank"
          rel="noreferrer"
          className="text-neutral-300 hover:text-white transition-colors bg-transparent p-0 m-0 shadow-none focus:outline-none focus:ring-0"
          aria-label="GitHub"
          style={{ background: 'transparent' }}
        >
          <IconBrandGithub className="w-6 h-6" />
        </a>
      </div>
      <div className="flex flex-col items-center pt-16 md:pt-24 pb-12 p-4">
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-6xl font-bold text-white mb-6">
            <div className="flex flex-col items-center gap-4">
              <LayoutTextFlip
                text="Manim Video Generator"
                words={["Mathematical Animations", "3D Visualizations", "Interactive Demos"]}
                duration={3000}
              />
            </div>
          </h1>
          <p className="text-xl text-gray-300 mb-8 max-w-2xl">
            Transform your mathematical concepts into beautiful animations using the power of AI and Manim.
          </p>
          <div className="space-x-4 mb-12">
            <Link
              to="/auth"
              className="inline-block bg-blue-600 text-white px-8 py-3 rounded-lg font-medium hover:bg-blue-700 transition-colors"
            >
              Get Started
            </Link>
            {!isAuthenticated && (
              <Link
                to="/auth"
                className="inline-block border border-white text-white px-8 py-3 rounded-lg font-medium hover:bg-white hover:text-black transition-colors"
              >
                Sign In
              </Link>
            )}
          </div>
        </div>

        {/* Showcase Section */}
        <div className="w-full max-w-6xl mx-auto">
          <div className="text-center mb-8">
            <h2 className="text-2xl md:text-3xl font-bold text-white mb-4">
              See What You Can Create
            </h2>
            <p className="text-lg text-gray-300">
              Just describe your mathematical concept and watch it come to life
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 md:gap-12">
            {showcaseItems.map((item, index) => (
              <div key={index} className="bg-gray-900/50 backdrop-blur-sm rounded-2xl p-6 border border-gray-700/50 hover:border-gray-600/50 transition-all duration-300">
                <div className="aspect-video bg-gray-800 rounded-xl mb-4 overflow-hidden">
                  <img 
                    src={item.gif}
                    alt={`Animation for: ${item.prompt}`}
                    className="w-full h-full object-contain"
                    loading="lazy"
                  />
                </div>
                <div className="space-y-3">
                  <div className="bg-gray-800/80 rounded-lg p-3 border-l-4 border-blue-500">
                    <p className="text-gray-300 text-sm italic">
                      "{item.prompt}"
                    </p>
                  </div>
                  <p className="text-blue-400 font-medium text-sm">
                    {item.description}
                  </p>
                </div>
              </div>
            ))}
          </div>

          {/* Features Section */}
          <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center p-6 bg-gray-900/30 rounded-xl border border-gray-700/30">
              <div className="w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold text-white mb-2">AI-Powered</h3>
              <p className="text-gray-400 text-sm">
                Simply describe your mathematical concept in natural language
              </p>
            </div>

            <div className="text-center p-6 bg-gray-900/30 rounded-xl border border-gray-700/30">
              <div className="w-12 h-12 bg-green-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 4V2a1 1 0 011-1h8a1 1 0 011 1v2M7 4h10M7 4l-2 16h14L17 4M9 9v6m6-6v6" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold text-white mb-2">High Quality</h3>
              <p className="text-gray-400 text-sm">
                Professional-grade animations powered by Manim
              </p>
            </div>

            <div className="text-center p-6 bg-gray-900/30 rounded-xl border border-gray-700/30">
              <div className="w-12 h-12 bg-purple-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold text-white mb-2">Easy to Use</h3>
              <p className="text-gray-400 text-sm">
                No coding required - just type and create
              </p>
            </div>
          </div>


        </div>
      </div>
    </div>
  );
}