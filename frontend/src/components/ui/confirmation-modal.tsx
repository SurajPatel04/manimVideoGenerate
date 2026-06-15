import React from "react";
import { motion, AnimatePresence } from "motion/react";
import { IconX, IconAlertTriangle, IconLogout, IconTrash } from "@tabler/icons-react";

interface ConfirmationModalProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: () => void;
  title: string;
  message: string;
  confirmText?: string;
  cancelText?: string;
  isDanger?: boolean;
}

export const ConfirmationModal: React.FC<ConfirmationModalProps> = ({
  isOpen,
  onClose,
  onConfirm,
  title,
  message,
  confirmText = "Confirm",
  cancelText = "Cancel",
  isDanger = false,
}) => {
  // Determine which icon to show based on title or isDanger
  const getIcon = () => {
    const t = title.toLowerCase();
    if (t.includes("logout")) return <IconLogout className="h-6 w-6" />;
    if (t.includes("delete")) return <IconTrash className="h-6 w-6" />;
    return <IconAlertTriangle className="h-6 w-6" />;
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center p-4">
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
            onClick={onClose}
            className="absolute inset-0 bg-black/70 md:backdrop-blur-[2px]"
          />

          {/* Modal content */}
          <motion.div
            initial={{ opacity: 0, scale: 0.98, y: 10 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.98, y: 10 }}
            transition={{ 
              duration: 0.15, 
              ease: "easeOut" 
            }}
            className="relative w-full max-w-[340px] border-2 border-white bg-black p-5 shadow-[8px_8px_0px_0px_rgba(255,255,255,0.1)]"
          >
            {/* Header: Icon + Title */}
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-3">
                <div className="flex h-10 w-10 shrink-0 items-center justify-center border-2 border-white bg-white/5 text-white">
                  {getIcon()}
                </div>
                <h3 className="text-lg font-black uppercase tracking-tighter text-white leading-none">{title}</h3>
              </div>
              <button
                onClick={onClose}
                className="p-1 text-neutral-500 transition hover:text-white"
              >
                <IconX className="h-5 w-5" />
              </button>
            </div>

            {/* Message */}
            <p className="mb-8 text-sm font-medium text-neutral-400 leading-snug">
              {message}
            </p>

            {/* Actions */}
            <div className="flex flex-col gap-2">
              <button
                type="button"
                onClick={() => {
                  onConfirm();
                  onClose();
                }}
                className={`w-full border-2 px-4 py-3 text-xs font-black uppercase tracking-[0.2em] transition-all active:translate-y-0.5 active:translate-x-0.5 active:shadow-none ${
                  isDanger
                    ? "border-red-600 bg-red-600 text-white shadow-[4px_4px_0px_0px_rgba(220,38,38,0.3)] hover:bg-red-500"
                    : "border-white bg-white text-black shadow-[4px_4px_0px_0px_rgba(255,255,255,0.3)] hover:bg-neutral-200"
                }`}
              >
                {confirmText}
              </button>
              <button
                type="button"
                onClick={onClose}
                className="w-full border-2 border-neutral-800 bg-transparent px-4 py-3 text-xs font-black uppercase tracking-[0.2em] text-neutral-500 transition-all hover:border-white hover:text-white active:bg-neutral-900"
              >
                {cancelText}
              </button>
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
};
