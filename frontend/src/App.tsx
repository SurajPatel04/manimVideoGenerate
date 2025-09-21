import './App.css'
import { createBrowserRouter, createRoutesFromElements, Route, Navigate, Outlet, RouterProvider } from 'react-router-dom';

import { BackgroundBeams } from "@/components/ui/background-beams";
import AuthForm from "@/components/AuthForm";
import MainPage from "@/components/MainPage";
import Homepage from "@/components/Homepage";
import { AuthProvider, useAuth } from "@/contexts/AuthContext";
import VerifiedPage from "@/components/VerifiedPage"

function Layout() {
  return (
    <div style={{ position: "relative", minHeight: "100vh", overflow: "hidden", backgroundColor: "black" }}>
      <BackgroundBeams className="z-0" />
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
      <Route path='verify' element={<VerifiedPage/>}/>
      
      <Route element={<PublicRoute />}>
        <Route 
          path="login" 
          element={
            <div className="flex min-h-screen items-center justify-center p-4">
              <AuthForm />
            </div>
          } 
        />
        <Route 
          path="signup" 
          element={
            <div className="flex min-h-screen items-center justify-center p-4">
              <AuthForm />
            </div>
          } 
        />
        <Route path="home" element={<Homepage />} />
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
    </AuthProvider>
  );
}

export default App
