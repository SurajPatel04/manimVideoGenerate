import { Link } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import { LayoutTextFlip } from '@/components/ui/layout-text-flip';
import { 
  IconBrandGithub, 
  IconBrandLinkedin, 
  IconWand, 
  IconVideo, 
  IconCode, 
  IconSparkles,
  IconMessage2,
  IconBrain,
  IconPlayerPlay
} from '@tabler/icons-react';

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

  const workflowSteps = [
    {
      icon: <IconMessage2 className="w-5 h-5 text-white" />,
      title: "1. Describe Your Idea",
      description: "Type out your mathematical concept, graph, or animation idea in plain English using our chat interface."
    },
    {
      icon: <IconBrain className="w-5 h-5 text-white" />,
      title: "2. AI Code Generation",
      description: "Our fine-tuned LLM instantly analyzes your request and writes precise, industry-standard Manim Python code."
    },
    {
      icon: <IconPlayerPlay className="w-5 h-5 text-white" />,
      title: "3. Cloud Rendering",
      description: "The backend server securely compiles the code into a smooth, high-quality MP4 or GIF in seconds."
    }
  ];

  return (
    <div className="relative z-10 min-h-screen bg-[#000000] font-sans text-neutral-200 selection:bg-neutral-800 selection:text-white pb-24">
      
      {/* Top Navigation / Icons */}
      <div className="absolute right-4 top-4 z-50 flex gap-4 md:right-8 md:top-8">
        <a
          href="https://www.linkedin.com/in/suraj-patel-9201b2381/"
          target="_blank"
          rel="noreferrer"
          className="text-neutral-500 hover:text-white transition-colors"
          aria-label="LinkedIn"
        >
          <IconBrandLinkedin className="w-6 h-6 md:w-5 md:h-5" />
        </a>
        <a
          href="https://github.com/SurajPatel04"
          target="_blank"
          rel="noreferrer"
          className="text-neutral-500 hover:text-white transition-colors"
          aria-label="GitHub"
        >
          <IconBrandGithub className="w-6 h-6 md:w-5 md:h-5" />
        </a>
      </div>

      <div className="relative flex flex-col items-center pt-24 md:pt-32 pb-20 px-4 max-w-7xl mx-auto">
        
        {/* 1. Hero Section */}
        <div className="text-center max-w-4xl mx-auto mb-32 flex flex-col items-center">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full border border-neutral-800 text-xs font-medium text-neutral-400 mb-8 tracking-wide uppercase">
            <IconSparkles className="w-3.5 h-3.5 text-neutral-400" />
            <span>Powered by AI & Manim</span>
          </div>
          
          <h1 className="text-4xl md:text-7xl font-semibold tracking-tight text-white mb-8 leading-tight">
            <div className="flex flex-col items-center gap-1 md:gap-2">
              <span className="px-2 text-center leading-tight">Manim Video Generator</span>
              <div className="flex flex-col md:flex-row items-center justify-center min-h-[100px] mt-2 md:mt-4 text-neutral-400 font-normal w-full">
                <LayoutTextFlip
                  text="Create"
                  words={["Mathematical Animations", "3D Visualizations", "Interactive Demos"]}
                  duration={3000}
                />
              </div>
            </div>
          </h1>
          
          <p className="text-lg md:text-xl text-neutral-500 mb-10 max-w-2xl leading-relaxed">
            Transform your mathematical concepts into beautiful, production-ready animations using natural language. No complex Python coding required.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 items-center justify-center w-full sm:w-auto">
            <Link
              to={isAuthenticated ? "/main" : "/auth"}
              className="w-full sm:w-auto group inline-flex items-center justify-center gap-2 bg-white text-black px-8 py-3.5 rounded-md font-medium transition-colors hover:bg-neutral-200"
            >
              {isAuthenticated ? "Go to Dashboard" : "Start Creating Free"}
              <svg className="w-4 h-4 transition-transform group-hover:translate-x-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 12h14M12 5l7 7-7 7" />
              </svg>
            </Link>
            
            {!isAuthenticated && (
              <Link
                to="/auth"
                className="w-full sm:w-auto inline-flex items-center justify-center px-8 py-3.5 rounded-md font-medium text-white border border-neutral-800 hover:bg-neutral-900 transition-colors"
              >
                Sign In
              </Link>
            )}
          </div>
        </div>

        {/* 2. Showcase Section */}
        <div className="w-full mb-32">
          <div className="text-center mb-12">
            <h2 className="text-2xl font-semibold tracking-tight text-white mb-3">
              See What You Can Create
            </h2>
            <p className="text-neutral-500">
              Just describe your concept and watch it come to life.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {showcaseItems.map((item, index) => (
              <div key={index} className="bg-neutral-950 rounded-xl p-2 border border-neutral-800/80">
                <div className="aspect-video bg-[#0a0a0a] rounded-lg mb-4 overflow-hidden border border-neutral-800/50">
                  <img 
                    src={item.gif}
                    alt={`Animation for: ${item.prompt}`}
                    className="w-full h-full object-cover"
                    loading="lazy"
                  />
                </div>
                <div className="px-3 pb-3 pt-1">
                  <p className="text-sm font-medium text-white mb-3">{item.description}</p>
                  <div className="bg-[#0a0a0a] rounded-md p-3 border border-neutral-800/50 flex flex-col justify-center min-h-[4rem]">
                    <p className="text-neutral-400 text-sm font-mono leading-relaxed">
                      <span className="text-neutral-600 mr-2">{">"}</span>
                      {item.prompt}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* 3. How It Works Section */}
        <div className="w-full mb-32 border-t border-neutral-800/80 pt-24">
          <div className="text-center mb-16">
            <h2 className="text-2xl font-semibold tracking-tight text-white mb-3">
              How It Works
            </h2>
            <p className="text-neutral-500 max-w-2xl mx-auto">
              From natural language to production-ready video in three simple steps. Our pipeline handles the heavy lifting so you can focus on teaching.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 relative">
            {/* Connecting line for desktop */}
            <div className="hidden md:block absolute top-[52px] left-[16.66%] right-[16.66%] h-[1px] bg-neutral-800 z-0" />

            {workflowSteps.map((step, idx) => (
              <div key={idx} className="relative z-10 flex flex-col items-center text-center p-6 bg-transparent">
                <div className="w-14 h-14 rounded-full flex items-center justify-center mb-6 border border-neutral-700 bg-neutral-900 text-white shadow-sm ring-8 ring-[#000000]">
                  {step.icon}
                </div>
                <h3 className="text-lg font-medium text-white mb-3 tracking-tight">{step.title}</h3>
                <p className="text-neutral-500 leading-relaxed text-sm">
                  {step.description}
                </p>
              </div>
            ))}
          </div>
        </div>

        {/* 4. Features Section */}
        <div className="w-full mb-24 border-t border-neutral-800/80 pt-24">
          <div className="text-center mb-12">
            <h2 className="text-2xl font-semibold tracking-tight text-white mb-3">
              Built for Creators & Educators
            </h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="p-8 bg-neutral-950 rounded-xl border border-neutral-800/80 hover:bg-neutral-900 transition-colors">
              <div className="w-10 h-10 rounded-lg flex items-center justify-center mb-5 border border-neutral-700 bg-neutral-800 text-white">
                <IconWand className="w-5 h-5" />
              </div>
              <h3 className="text-lg font-medium text-white mb-2">Automated Geometry</h3>
              <p className="text-neutral-500 leading-relaxed text-sm">
                Easily generate perfect axes, 3D grids, mathematical equations, and geometric transforms without debugging coordinates.
              </p>
            </div>

            <div className="p-8 bg-neutral-950 rounded-xl border border-neutral-800/80 hover:bg-neutral-900 transition-colors">
              <div className="w-10 h-10 rounded-lg flex items-center justify-center mb-5 border border-neutral-700 bg-neutral-800 text-white">
                <IconVideo className="w-5 h-5" />
              </div>
              <h3 className="text-lg font-medium text-white mb-2">Multi-Format Output</h3>
              <p className="text-neutral-500 leading-relaxed text-sm">
                Request high-res MP4s for YouTube content, or lightweight optimized GIFs perfect for Twitter, Notion, and blogs.
              </p>
            </div>

            <div className="p-8 bg-neutral-950 rounded-xl border border-neutral-800/80 hover:bg-neutral-900 transition-colors">
              <div className="w-10 h-10 rounded-lg flex items-center justify-center mb-5 border border-neutral-700 bg-neutral-800 text-white">
                <IconCode className="w-5 h-5" />
              </div>
              <h3 className="text-lg font-medium text-white mb-2">Export Code</h3>
              <p className="text-neutral-500 leading-relaxed text-sm">
                We don't lock you in. You can copy the generated raw Manim Python code to tweak the timing and vectors locally.
              </p>
            </div>
          </div>
        </div>

        {/* 5. Bottom CTA */}
        <div className="w-full py-16 bg-neutral-950 rounded-2xl border border-neutral-800/80 text-center px-4">
          <h2 className="text-3xl font-semibold text-white mb-4 tracking-tight">Ready to visualize math?</h2>
          <p className="text-neutral-500 mb-8">Join and start generating high-quality Manim videos instantly.</p>
          <Link
            to={isAuthenticated ? "/main" : "/auth"}
            className="inline-flex items-center justify-center bg-white text-black px-8 py-3 rounded-md font-medium transition-colors hover:bg-neutral-200"
          >
            {isAuthenticated ? "Open Dashboard" : "Start Creating Free"}
          </Link>
        </div>

      </div>
    </div>
  );
}