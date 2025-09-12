import { Link } from 'react-router-dom';

export default function Homepage() {
  return (
    <div className="relative z-10 flex min-h-screen flex-col items-center justify-center p-4">
      <div className="text-center">
        <h1 className="text-4xl md:text-6xl font-bold text-white mb-6">
          Manim Video Generator
        </h1>
        <p className="text-xl text-gray-300 mb-8 max-w-2xl">
          Transform your mathematical concepts into beautiful animations using the power of AI and Manim.
        </p>
        <div className="space-x-4">
          <Link
            to="/auth"
            className="inline-block bg-blue-600 text-white px-8 py-3 rounded-lg font-medium hover:bg-blue-700 transition-colors"
          >
            Get Started
          </Link>
          <Link
            to="/auth"
            className="inline-block border border-white text-white px-8 py-3 rounded-lg font-medium hover:bg-white hover:text-black transition-colors"
          >
            Sign In
          </Link>
        </div>
      </div>
    </div>
  );
}