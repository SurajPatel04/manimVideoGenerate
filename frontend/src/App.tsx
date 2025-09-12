import './App.css'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

import { BackgroundBeams } from "@/components/ui/background-beams";
import AuthForm from "@/components/AuthForm";
import Dashboard from "@/components/Dashboard";
import MainPage from "@/components/MainPage";
import Homepage from "@/components/Homepage";
import { AuthProvider, useAuth } from "@/contexts/AuthContext";

// Protected Route Component
function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? <>{children}</> : <Navigate to="/auth" replace />;
}

// Public Route Component (redirect to main if authenticated)
function PublicRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated } = useAuth();
  return !isAuthenticated ? <>{children}</> : <Navigate to="/main" replace />;
}

function AppContent() {
  return (
    <div style={{ position: "relative", minHeight: "100vh", overflow: "hidden", backgroundColor: "black" }}>
      {/* Background Beams */}
      <BackgroundBeams className="z-0" />
      {/* Main Content */}
      <div className="relative z-10">
        <Routes>
          {/* Public Routes */}
          <Route 
            path="/auth" 
            element={
              <PublicRoute>
                <div className="flex min-h-screen items-center justify-center p-4">
                  <AuthForm />
                </div>
              </PublicRoute>
            } 
          />
          <Route 
            path="/home" 
            element={
              <PublicRoute>
                <Homepage />
              </PublicRoute>
            } 
          />
          
          {/* Protected Routes */}
          <Route 
            path="/main" 
            element={
              <ProtectedRoute>
                <MainPage />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/dashboard" 
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            } 
          />
          
          {/* Default Routes */}
          <Route path="/" element={<Navigate to="/home" replace />} />
          <Route path="*" element={<Navigate to="/home" replace />} />
        </Routes>
      </div>
    </div>
  );
}

function App() {
  return (
    <AuthProvider>
      <Router>
        <AppContent />
      </Router>
    </AuthProvider>
  );
}

export default App
