import { BackgroundBeams } from "@/components/ui/background-beams";

export default function VerifiedPage() {
  return (
    <div className="flex h-full items-center justify-center bg-black relative">
      <BackgroundBeams className="opacity-80" />

      <div className="relative z-10 w-full max-w-xl p-8 bg-gray-900/70 border border-gray-700 rounded-lg text-center">
        <h1 className="text-2xl md:text-3xl font-semibold text-white mb-4">Email Verification
</h1>
        <p className="text-sm text-gray-300">
          We've sent a verification email to your Gmail account. Please open your Gmail inbox and click the verification link to complete setup.
        </p>
      </div>
    </div>
  );
}
