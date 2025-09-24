import './App.css'
import 'react-toastify/dist/ReactToastify.css';
import { ToastContainer } from 'react-toastify';
import { createBrowserRouter, createRoutesFromElements, Route, Navigate, Outlet, RouterProvider } from 'react-router-dom';

import { BackgroundBeams } from "@/components/ui/background-beams";
import AuthForm from "@/components/AuthForm";
import VerifiedPage from "@/components/VerifiedPage";
import MainPage from "@/components/MainPage";
import Homepage from "@/components/Homepage";
import { AuthProvider, useAuth } from "@/contexts/AuthContext";
import ResetPassword from "@/components/ResetPassword"
import ForgotPassword from "@/components/ForgotPassword"

import { useLocation, Link } from 'react-router-dom';
import { IconBrandGithub, IconBrandLinkedin } from '@tabler/icons-react';

function Layout() {
  const location = useLocation();
  const { isAuthenticated } = useAuth();
  const hideOn = ['/', '/home'];
  const onMain = location.pathname.startsWith('/main');
  const showLeft = !onMain && !hideOn.includes(location.pathname); // Manim text on left
  const showRight = !hideOn.includes(location.pathname) || onMain; // icons on right; always show on main

  return (
    <div style={{ position: "relative", minHeight: "100vh", overflow: "hidden", backgroundColor: "black" }}>
      <BackgroundBeams className="z-0" />

      {/* Page-level corner: Manim link on left (hidden on /main), social icons on right (visible on /main and other allowed pages) */}
      {showLeft && (
        <div className="absolute top-4 left-4 z-20">
          <Link to={isAuthenticated ? "/main" : "/"} className="text-white font-semibold hover:text-gray-300">
            Manim
          </Link>
        </div>
      )}

      {showRight && (
        <div className="absolute right-0 md:right-4 top-0 md:top-4 z-20 flex items-center gap-4 text-neutral-200 h-16 md:h-auto pr-4 md:pr-0">
          <a
            href="https://www.linkedin.com/in/suraj-patel-9201b2381/"
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-blue-500 transition-colors"
            aria-label="LinkedIn"
          >
            <IconBrandLinkedin className="h-6 w-6" />
          </a>

          <a
            href="https://github.com/SurajPatel04"
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-white transition-colors"
            aria-label="GitHub"
          >
            <IconBrandGithub className="h-6 w-6" />
          </a>
        </div>
      )}

      <div className="relative z-10">
        <Outlet />
      </div>
    </div>
  );
}

function ProtectedRoute() {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? <Outlet /> : <Navigate to="/login" replace />;
}

function PublicRoute() {
  const { isAuthenticated } = useAuth();
  return !isAuthenticated ? <Outlet /> : <Navigate to="/main" replace />;
}

const router = createBrowserRouter(
  createRoutesFromElements(
    <Route path="/" element={<Layout />}>
      {/* Public Routes */}
      <Route path="" element={<Homepage />} />
      <Route path="forgetPassword" element={<ForgotPassword />} />
      <Route path='resetPassword/*' element={
        <div className="flex min-h-screen box-border items-center justify-center p-4">
          <ResetPassword />
        </div>
      }/>
      
      <Route element={<PublicRoute />}>
        <Route 
          path="login" 
          element={
            <div className="flex min-h-screen box-border items-center justify-center p-4">
              <AuthForm />
            </div>
          } 
        />
        <Route 
          path="signup" 
          element={
            <div className="flex min-h-screen box-border items-center justify-center p-4">
              <AuthForm />
            </div>
          } 
        />
        <Route path="home" element={<Homepage />} />
        <Route 
          path="verified"
          element={
            <div className="flex min-h-screen box-border items-center justify-center p-4">
              <VerifiedPage />
            </div>
          }
        />
      </Route>
      
      <Route element={<ProtectedRoute />}>
        <Route path="main" element={<MainPage />} />
      </Route>
      
      <Route path="auth" element={<Navigate to="/login" replace />} />
      <Route path="*" element={<Navigate to="/home" replace />} />
    </Route>
  )
);

function App() {
  return (
    <AuthProvider>
      <RouterProvider router={router} />
      <ToastContainer />
    </AuthProvider>
  );
}

export default App
