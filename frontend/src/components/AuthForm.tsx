"use client";
import React, { useState } from "react";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";
import {
  IconBrandGithub,
  IconBrandGoogle,
  IconEye,
  IconEyeOff,
} from "@tabler/icons-react";
import { useAuth } from "@/contexts/AuthContext";

export default function AuthForm() {
  const { login, signup, loading } = useAuth();
  const [isLogin, setIsLogin] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [error, setError] = useState("");
  const [formData, setFormData] = useState({
    firstName: "",
    lastName: "",
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
    
    if (isLogin) {
      try {
        const success = await login(formData.email, formData.password);
        if (!success) {
          setError("Invalid email or password");
        }
      } catch (err) {
        setError("Login failed. Please try again.");
      }
    } else {
      if (formData.password !== formData.confirmPassword) {
        setError("Passwords don't match!");
        return;
      }
      try {
        const success = await signup({
          firstName: formData.firstName,
          lastName: formData.lastName,
          email: formData.email,
          password: formData.password,
        });
        if (!success) {
          setError("Signup failed. Please try again.");
        }
      } catch (err) {
        setError("Signup failed. Please try again.");
      }
    }
  };

  const toggleAuthMode = () => {
    setIsLogin(!isLogin);
    // Clear form when switching
    setFormData({
      firstName: "",
      lastName: "",
      email: "",
      password: "",
      confirmPassword: "",
    });
  };

  return (
    <div className="shadow-2xl mx-auto w-full max-w-md rounded-2xl bg-black/40 backdrop-blur-lg border border-white/20 p-4 md:p-8">
      <h2 className="text-xl font-bold text-white">
        {isLogin ? "Welcome Back" : "Create Your Account"}
      </h2>
      <p className="mt-2 max-w-sm text-sm text-neutral-300">
        {isLogin
          ? "Sign in to your account to continue"
          : "Join us today"}
      </p>

      <form className="my-8" onSubmit={handleSubmit}>
        {error && (
          <div className="mb-4 rounded-md bg-red-500/20 border border-red-500/30 p-3 text-sm text-red-300">
            {error}
          </div>
        )}
        {!isLogin && (
          <div className="mb-4 flex flex-col space-y-2 md:flex-row md:space-y-0 md:space-x-2">
            <LabelInputContainer>
              <Label htmlFor="firstName" className="text-white">First name</Label>
              <Input
                id="firstName"
                placeholder="John"
                type="text"
                value={formData.firstName}
                onChange={handleInputChange}
                required
              />
            </LabelInputContainer>
            <LabelInputContainer>
              <Label htmlFor="lastName" className="text-white">Last name</Label>
              <Input
                id="lastName"
                placeholder="Doe"
                type="text"
                value={formData.lastName}
                onChange={handleInputChange}
                required
              />
            </LabelInputContainer>
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
          <Label htmlFor="password" className="text-white">Password</Label>
          <div className="relative">
            <Input
              id="password"
              placeholder="••••••••"
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
        </LabelInputContainer>

        {!isLogin && (
          <LabelInputContainer className="mb-6">
            <Label htmlFor="confirmPassword" className="text-white">Confirm Password</Label>
            <div className="relative">
              <Input
                id="confirmPassword"
                placeholder="••••••••"
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
        )}

        {isLogin && (
          <div className="mb-6 flex items-center justify-between">
            <label className="flex items-center">
              <input
                type="checkbox"
                className="mr-2 h-4 w-4 rounded border-neutral-600 bg-neutral-800 text-blue-600 focus:ring-blue-500"
              />
              <span className="text-sm text-neutral-300">
                Remember me
              </span>
            </label>
            <a
              href="#"
              className="text-sm text-blue-400 hover:text-blue-300"
            >
              Forgot password?
            </a>
          </div>
        )}

        <button
          className="group/btn relative block h-10 w-full rounded-md font-medium text-white shadow-lg hover:shadow-gray-500/20 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
          style={{ backgroundColor: '#202020' }}
          type="submit"
          disabled={loading}
        >
          {loading ? "Please wait..." : `${isLogin ? "Sign In" : "Sign Up"} →`}
          <BottomGradient />
        </button>

        <div className="my-8 h-[1px] w-full bg-gradient-to-r from-transparent via-neutral-600 to-transparent" />

        <div className="flex flex-col space-y-4">
          <button
            className="group/btn shadow-lg relative flex h-10 w-full items-center justify-start space-x-2 rounded-md bg-neutral-800/50 backdrop-blur border border-neutral-700 px-4 font-medium text-white hover:bg-neutral-700/50 transition-all duration-200"
            type="button"
          >
            <IconBrandGithub className="h-4 w-4 text-neutral-300" />
            <span className="text-sm text-neutral-200">
              Continue with GitHub
            </span>
            <BottomGradient />
          </button>
          <button
            className="group/btn shadow-lg relative flex h-10 w-full items-center justify-start space-x-2 rounded-md bg-neutral-800/50 backdrop-blur border border-neutral-700 px-4 font-medium text-white hover:bg-neutral-700/50 transition-all duration-200"
            type="button"
          >
            <IconBrandGoogle className="h-4 w-4 text-neutral-300" />
            <span className="text-sm text-neutral-200">
              Continue with Google
            </span>
            <BottomGradient />
          </button>
        </div>
      </form>

      <div className="mt-6 text-center">
        <p className="text-sm text-neutral-400">
          {isLogin ? "Don't have an account?" : "Already have an account?"}{" "}
          <button
            onClick={toggleAuthMode}
            className="font-semibold text-blue-400 hover:text-blue-300 transition-colors duration-200"
          >
            {isLogin ? "Sign up" : "Sign in"}
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
