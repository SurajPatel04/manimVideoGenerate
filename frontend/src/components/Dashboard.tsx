import { useAuth } from '@/contexts/AuthContext';
import { Link } from 'react-router-dom';

export default function Dashboard() {
  const { user, logout } = useAuth();

  return (
    <div className="relative z-10 flex min-h-screen flex-col items-center justify-center p-4">
      <div className="shadow-input mx-auto w-full max-w-2xl rounded-2xl bg-white p-8 dark:bg-black">
        <div className="mb-8 text-center">
          <h1 className="text-3xl font-bold text-neutral-800 dark:text-neutral-200">
            Dashboard - Welcome, {user?.firstName}!
          </h1>
          <p className="mt-2 text-neutral-600 dark:text-neutral-300">
            Manage your account and view your activity.
          </p>
        </div>

        <div className="mb-8 rounded-lg bg-gradient-to-r from-blue-50 to-indigo-50 p-6 dark:from-blue-900/20 dark:to-indigo-900/20">
          <h2 className="mb-4 text-xl font-semibold text-neutral-800 dark:text-neutral-200">
            Your Profile
          </h2>
          <div className="space-y-2">
            <p className="text-neutral-600 dark:text-neutral-300">
              <span className="font-medium">Name:</span> {user?.firstName} {user?.lastName}
            </p>
            <p className="text-neutral-600 dark:text-neutral-300">
              <span className="font-medium">Email:</span> {user?.email}
            </p>
            <p className="text-neutral-600 dark:text-neutral-300">
              <span className="font-medium">User ID:</span> {user?.id}
            </p>
          </div>
        </div>

        <div className="grid gap-4 md:grid-cols-2">
          <div className="rounded-lg border border-neutral-200 p-4 dark:border-neutral-700">
            <h3 className="mb-2 font-medium text-neutral-800 dark:text-neutral-200">
              Quick Actions
            </h3>
            <div className="space-y-2">
              <Link 
                to="/main"
                className="block w-full rounded-md bg-blue-100 px-3 py-2 text-left text-sm text-blue-800 hover:bg-blue-200 dark:bg-blue-900/30 dark:text-blue-300 dark:hover:bg-blue-900/50"
              >
                Go to Manim Generator
              </Link>
              <button className="w-full rounded-md bg-green-100 px-3 py-2 text-left text-sm text-green-800 hover:bg-green-200 dark:bg-green-900/30 dark:text-green-300 dark:hover:bg-green-900/50">
                Edit Profile
              </button>
              <button className="w-full rounded-md bg-purple-100 px-3 py-2 text-left text-sm text-purple-800 hover:bg-purple-200 dark:bg-purple-900/30 dark:text-purple-300 dark:hover:bg-purple-900/50">
                View Activity
              </button>
            </div>
          </div>

          <div className="rounded-lg border border-neutral-200 p-4 dark:border-neutral-700">
            <h3 className="mb-2 font-medium text-neutral-800 dark:text-neutral-200">
              Recent Activity
            </h3>
            <div className="space-y-2 text-sm text-neutral-600 dark:text-neutral-300">
              <p>• Logged in successfully</p>
              <p>• Account created</p>
              <p>• Welcome email sent</p>
            </div>
          </div>
        </div>

        <div className="mt-8 flex justify-center space-x-4">
          <Link
            to="/main"
            className="rounded-md bg-blue-600 px-6 py-2 font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:focus:ring-offset-black"
          >
            Create Animation
          </Link>
          <button
            onClick={logout}
            className="rounded-md bg-red-600 px-6 py-2 font-medium text-white hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 dark:focus:ring-offset-black"
          >
            Sign Out
          </button>
        </div>
      </div>
    </div>
  );
}
