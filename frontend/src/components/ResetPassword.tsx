"use client";
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";
import { IconEye, IconEyeOff, IconBrandGithub, IconBrandLinkedin } from "@tabler/icons-react";
import axios from 'axios';
import { useAuth } from '@/contexts/AuthContext';

export default function ResetPassword() {
  // use loading from auth context; don't rely on resetPassword method existing
  const { loading } = useAuth();
  const navigate = useNavigate();

  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [error, setError] = useState("");
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    confirmPassword: "",
  });

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.id]: e.target.value,
    });
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError("");

    if (formData.password.length < 6) {
      setError("Password must be at least 6 characters");
      return;
    }

    if (formData.password !== formData.confirmPassword) {
      setError("Passwords don't match!");
      return;
    }

    try {
      // Call backend reset endpoint. Adjust payload to whatever your API expects.
      await axios.post(
        '/api/user/reset-password',
        {
          email: formData.email,
          newPassword: formData.password,
        },
        {
          withCredentials: true,
          headers: { 'Content-Type': 'application/json' },
          timeout: 10000,
        }
      );

      navigate('/login');
    } catch (err: unknown) {
      console.error('Reset failed:', err);
      let message = 'Reset failed. Please try again.';

      const extractMessageFromData = (data: unknown): string | undefined => {
        if (!data || typeof data !== 'object') return undefined;
        const d = data as Record<string, unknown>;
        if (typeof d.detail === 'string') return d.detail;
        if (typeof d.message === 'string') return d.message;
        return undefined;
      };

      if (axios.isAxiosError(err)) {
        const fromData = extractMessageFromData(err.response?.data);
        message = fromData || err.message || message;
      } else if (err instanceof Error) {
        message = err.message;
      } else {
        message = String(err);
      }

      setError(message || 'Reset failed. Please try again.');
    }
  };

  return (
    <div className="shadow-2xl mx-auto w-full max-w-md rounded-2xl bg-black/40 backdrop-blur-lg border border-white/20 p-4 md:p-8">
      <h2 className="text-xl font-bold text-white">Reset Password</h2>
      <p className="mt-2 max-w-sm text-sm text-neutral-300">Enter your email and choose a new password.</p>

      <form className="my-8" onSubmit={handleSubmit}>
        {error && (
          <div className="mb-4 rounded-md bg-red-500/20 border border-red-500/30 p-3 text-sm text-red-300">
            {error}
          </div>
        )}

        <LabelInputContainer className="mb-4">
          <Label htmlFor="email" className="text-white">Email Address</Label>
          <Input
            id="email"
            placeholder="john@example.com"
            type="email"
            value={formData.email}
            onChange={handleInputChange}
            required
          />
        </LabelInputContainer>

        <LabelInputContainer className="mb-4">
          <Label htmlFor="password" className="text-white">New Password</Label>
          <div className="relative">
            <Input
              id="password"
              placeholder=""
              type={showPassword ? "text" : "password"}
              value={formData.password}
              onChange={handleInputChange}
              required
            />
            <button
              type="button"
              className="absolute inset-y-0 right-0 flex items-center pr-3"
              onClick={() => setShowPassword(!showPassword)}
            >
              {showPassword ? (
                <IconEyeOff className="h-4 w-4 text-neutral-400 hover:text-white" />
              ) : (
                <IconEye className="h-4 w-4 text-neutral-400 hover:text-white" />
              )}
            </button>
          </div>
          <p className="text-xs text-neutral-400 mt-1">Password must be at least 6 characters</p>
        </LabelInputContainer>

        <LabelInputContainer className="mb-6">
          <Label htmlFor="confirmPassword" className="text-white">Confirm New Password</Label>
          <div className="relative">
            <Input
              id="confirmPassword"
              placeholder=""
              type={showConfirmPassword ? "text" : "password"}
              value={formData.confirmPassword}
              onChange={handleInputChange}
              required
            />
            <button
              type="button"
              className="absolute inset-y-0 right-0 flex items-center pr-3"
              onClick={() => setShowConfirmPassword(!showConfirmPassword)}
            >
              {showConfirmPassword ? (
                <IconEyeOff className="h-4 w-4 text-neutral-400 hover:text-white" />
              ) : (
                <IconEye className="h-4 w-4 text-neutral-400 hover:text-white" />
              )}
            </button>
          </div>
        </LabelInputContainer>

        <button
          className="group/btn relative block h-10 w-full rounded-md font-medium text-white shadow-lg hover:shadow-gray-500/20 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
          style={{ backgroundColor: '#202020' }}
          type="submit"
          disabled={loading}
        >
          {loading ? "Please wait..." : "Reset Password →"}
          <BottomGradient />
        </button>
      </form>

      <div className="mt-6 text-center">
        <p className="text-sm text-neutral-400">
          Remembered your password?{' '}
          <button
            onClick={() => navigate('/login')}
            className="font-semibold text-blue-400 hover:text-blue-300 transition-colors duration-200"
          >
            Sign in
          </button>
        </p>
      </div>
    </div>
  );
}

const BottomGradient = () => {
  return (
    <>
      <span className="absolute inset-x-0 -bottom-px block h-px w-full bg-gradient-to-r from-transparent via-cyan-500 to-transparent opacity-0 transition duration-500 group-hover/btn:opacity-100" />
      <span className="absolute inset-x-10 -bottom-px mx-auto block h-px w-1/2 bg-gradient-to-r from-transparent via-indigo-500 to-transparent opacity-0 blur-sm transition duration-500 group-hover/btn:opacity-100" />
    </>
  );
};

const LabelInputContainer = ({
  children,
  className,
}: {
  children: React.ReactNode;
  className?: string;
}) => {
  return (
    <div className={cn("flex w-full flex-col space-y-2", className)}>
      {children}
    </div>
  );
};
