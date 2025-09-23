"use client";
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { toast } from 'react-toastify';

export default function ForgotPassword() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [sent, setSent] = useState(false);
  const [error, setError] = useState("");

  const sendResetRequest = async (targetEmail: string) => {
    setError("");
    if (!targetEmail) {
      setError("Please enter your email address");
      return { ok: false };
    }

    setLoading(true);
    try {
      const res = await fetch(`/api/user/passwordResetRequest`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: targetEmail }),
      });

      let data: any = null;
      try {
        data = await res.json();
      } catch (e) {
        data = null;
      }

      if (!res.ok) {
        const msg = data?.detail || data?.message || data?.error || res.statusText || "Failed to send reset email";
        setError(typeof msg === 'string' ? msg : String(msg));
        toast.error(typeof msg === 'string' ? msg : String(msg));
        return { ok: false, data };
      }

      if (data?.status === true || data?.status === 'True') {
        setSent(true);
        toast.success(data?.message || 'Please check your email to reset your password.');
      } else if (data?.isVerified === false) {
        const msg = data?.message || data?.error || 'Account not verified';
        setError(typeof msg === 'string' ? msg : String(msg));
        toast.error(typeof msg === 'string' ? msg : String(msg));
        return { ok: false, data };
      } else {
        setSent(true);
        toast.success(data?.message || 'Please check your email to reset your password.');
      }

      return { ok: true, data };
    } catch (err: any) {
      setError(err?.message || 'Failed to send reset email');
      toast.error(err?.message || 'Failed to send reset email');
      return { ok: false, data: null };
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await sendResetRequest(email);
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-6">
      <div className="shadow-2xl mx-auto w-full max-w-md rounded-2xl bg-black/40 backdrop-blur-lg border border-white/20 p-4 md:p-8">
      <h2 className="text-xl font-bold text-white">Forgot Password</h2>
      <p className="mt-2 max-w-sm text-sm text-neutral-300">
        Enter the email associated with your account and we'll send a password
        reset link if the account exists.
      </p>

      <form className="my-8" onSubmit={handleSubmit}>
        {error && (
          <div className="mb-4 rounded-md bg-red-500/20 border border-red-500/30 p-3 text-sm text-red-300">
            {error}
          </div>
        )}

        {sent && (
          <div className="mb-4 rounded-md bg-green-500/10 border border-green-500/20 p-4 text-sm text-green-200">
            We've sent a password reset link. Check your email.
          </div>
        )}

        <div className="mb-4">
          <Label htmlFor="email" className="text-white">Email Address</Label>
          <Input
            id="email"
            placeholder="john@example.com"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>

        <button
          className="group/btn relative block h-10 w-full rounded-md font-medium text-white shadow-lg hover:shadow-gray-500/20 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
          style={{ backgroundColor: '#202020' }}
          type="submit"
          disabled={loading}
        >
          {loading ? 'Please wait...' : sent ? 'Resend link' : 'Send reset link'}
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
    </div>
  );
}

const BottomGradient = () => (
  <>
    <span className="absolute inset-x-0 -bottom-px block h-px w-full bg-gradient-to-r from-transparent via-cyan-500 to-transparent opacity-0 transition duration-500 group-hover/btn:opacity-100" />
    <span className="absolute inset-x-10 -bottom-px mx-auto block h-px w-1/2 bg-gradient-to-r from-transparent via-indigo-500 to-transparent opacity-0 blur-sm transition duration-500 group-hover/btn:opacity-100" />
  </>
);
