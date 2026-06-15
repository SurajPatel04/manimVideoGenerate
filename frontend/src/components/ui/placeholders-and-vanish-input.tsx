"use client";

import { AnimatePresence, motion } from "motion/react";
import { IconSettings } from "@tabler/icons-react";
import { useCallback, useEffect, useRef, useState } from "react";
import { cn } from "@/lib/utils";

export function PlaceholdersAndVanishInput({
  placeholders,
  onChange,
  onSubmit,
  onCancel,
  isGenerating = false,
}: {
  placeholders: string[];
  onChange: (e: React.ChangeEvent<HTMLTextAreaElement>) => void;
  onSubmit: (e: React.FormEvent<HTMLFormElement>, options: { format: string; quality: string; resolution?: string }) => void;
  onCancel?: () => void;
  isGenerating?: boolean;
}) {
  const [currentPlaceholder, setCurrentPlaceholder] = useState(0);
  const [format, setFormat] = useState("mp4");
  const [quality, setQuality] = useState("ql");
  const [resolution, setResolution] = useState("1920x1080");
  const [customWidth, setCustomWidth] = useState(1920);
  const [customHeight, setCustomHeight] = useState(1080);
  const [showOptions, setShowOptions] = useState(false);
  const optionsRef = useRef<HTMLDivElement>(null);

  const intervalRef = useRef<NodeJS.Timeout | null>(null);
  const startAnimation = () => {
    intervalRef.current = setInterval(() => {
      setCurrentPlaceholder((prev) => (prev + 1) % placeholders.length);
    }, 3000);
  };
  const handleVisibilityChange = () => {
    if (document.visibilityState !== "visible" && intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    } else if (document.visibilityState === "visible") {
      startAnimation();
    }
  };

  useEffect(() => {
    startAnimation();
    document.addEventListener("visibilitychange", handleVisibilityChange);

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
      document.removeEventListener("visibilitychange", handleVisibilityChange);
    };
  }, [placeholders]);

  const [value, setValue] = useState("");
  const [isMultiline, setIsMultiline] = useState(false);
  const formRef = useRef<HTMLFormElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  // Flying bubble animation state
  const [flyingBubble, setFlyingBubble] = useState<{
    id: string;
    text: string;
    startRect: DOMRect;
    targetId: string;
  } | null>(null);
  const [animStep, setAnimStep] = useState<"start" | "flying" | "done">("start");
  const [targetRect, setTargetRect] = useState<DOMRect | null>(null);

  useEffect(() => {
    if (flyingBubble && animStep === "start") {
      const timer = setTimeout(() => {
        const userBubbles = document.querySelectorAll('.user-message-bubble');
        const targetEl = userBubbles.length > 0 ? userBubbles[userBubbles.length - 1] : document.getElementById("chat-bottom");
        if (targetEl) {
          setTargetRect(targetEl.getBoundingClientRect());
          setAnimStep("flying");
        } else {
          setAnimStep("done");
        }
      }, 30);
      return () => clearTimeout(timer);
    }
  }, [flyingBubble, animStep]);

  const lineHeightRef = useRef<number | null>(null);

  const resizeTextarea = useCallback(() => {
    const textarea = inputRef.current;
    if (!textarea) return;

    if (textarea.value === "") {
      textarea.style.height = "auto";
      textarea.style.overflowY = "hidden";
      setIsMultiline(false);
      return;
    }

    if (lineHeightRef.current === null) {
      const computedLineHeight = getComputedStyle(textarea).lineHeight;
      lineHeightRef.current = computedLineHeight === "normal" ? 24 : Number.parseFloat(computedLineHeight);
    }
    
    const lineHeight = lineHeightRef.current;
    const maxHeight = lineHeight * 6;

    textarea.style.height = "auto";
    const scrollHeight = textarea.scrollHeight;
    
    textarea.style.height = `${Math.min(scrollHeight, maxHeight)}px`;
    textarea.style.overflowY = scrollHeight > maxHeight ? "auto" : "hidden";
    setIsMultiline(scrollHeight > lineHeight * 1.5 + 16);
  }, []);

  useEffect(() => {
    resizeTextarea();
  }, [value, resizeTextarea]);

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      const target = event.target as Node;
      const plusButton = (event.target as Element).closest('[data-plus-button]');
      if (plusButton) return;

      if (optionsRef.current && !optionsRef.current.contains(target)) {
        setShowOptions(false);
      }
    }

    if (showOptions) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [showOptions]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey && !isGenerating) {
      e.preventDefault();
      e.currentTarget.form?.requestSubmit();
    }
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!value && !isGenerating) return;

    if (isGenerating && onCancel) {
      onCancel();
    } else {
      if (formRef.current) {
        const rect = formRef.current.getBoundingClientRect();
        setFlyingBubble({
          id: Date.now().toString(),
          text: value,
          startRect: rect,
          targetId: "latest-message",
        });
        setAnimStep("start");
      }

      setValue("");
      if (inputRef.current) {
        inputRef.current.value = "";
      }
      resizeTextarea();

      const res = resolution === 'custom' ? `${customWidth}x${customHeight}` : resolution;
      onSubmit && onSubmit(e, { format, quality, resolution: res });
    }
  };

  const leftSlot = (
    <button
      type="button"
      data-plus-button="true"
      onClick={(e) => {
        e.preventDefault();
        e.stopPropagation();
        setShowOptions(!showOptions);
      }}
      className={cn(
        "h-8 w-8 rounded-lg transition-all duration-200 flex items-center justify-center",
        "text-neutral-500 hover:text-neutral-300 hover:bg-neutral-700/50 cursor-pointer",
        showOptions && "text-neutral-300 bg-neutral-700/50"
      )}
    >
      <motion.div
        animate={{ rotate: showOptions ? 45 : 0 }}
        transition={{ duration: 0.2 }}
      >
        <IconSettings className="h-[18px] w-[18px]" />
      </motion.div>
    </button>
  );



  return (
    <div className="w-full relative max-w-xl mx-auto">
      <form
        ref={formRef}
        className={cn(
          "relative mx-auto flex w-full max-w-xl flex-col overflow-hidden rounded-2xl bg-zinc-800 shadow-[0px_2px_3px_-1px_rgba(0,0,0,0.1),_0px_1px_0px_0px_rgba(25,28,33,0.02),_0px_0px_0px_1px_rgba(25,28,33,0.08)] transition duration-200",
          value && "bg-zinc-800/90"
        )}
        onSubmit={handleSubmit}
      >
        <AnimatePresence initial={false}>
          {showOptions && (
            <motion.div
              ref={optionsRef}
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: "auto", opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              transition={{ duration: 0.2, ease: "easeInOut" }}
              className="w-full px-4 overflow-hidden origin-top"
            >
              <div className="mb-2 mt-3 p-3 rounded-2xl bg-neutral-900/50 backdrop-blur-sm border border-neutral-700/50 shadow-sm">
                <div className="flex gap-4 items-center flex-wrap">
                  <div className="flex flex-col gap-1.5 min-w-[80px]">
                    <label className="text-[11px] text-neutral-400 font-medium uppercase tracking-wider">Format</label>
                    <select
                      value={format}
                      onChange={(e) => setFormat(e.target.value)}
                      className="bg-neutral-800/80 text-neutral-200 text-sm rounded-lg px-3 py-1.5 border border-neutral-700/50 focus:outline-none focus:border-neutral-600 focus:ring-1 focus:ring-neutral-600 transition-colors cursor-pointer"
                    >
                      <option value="mp4">MP4</option>
                      <option value="gif">GIF</option>
                    </select>
                  </div>
                  <div className="flex flex-col gap-1.5 min-w-[100px]">
                    <label className="text-[11px] text-neutral-400 font-medium uppercase tracking-wider">Quality</label>
                    <select
                      value={quality}
                      onChange={(e) => setQuality(e.target.value)}
                      className="bg-neutral-800/80 text-neutral-200 text-sm rounded-lg px-3 py-1.5 border border-neutral-700/50 focus:outline-none focus:border-neutral-600 focus:ring-1 focus:ring-neutral-600 transition-colors cursor-pointer"
                    >
                      <option value="ql">Low</option>
                      <option value="qm">Medium</option>
                      <option value="qh">High</option>
                    </select>
                  </div>
                  <div className="flex flex-col gap-1.5 min-w-[140px]">
                    <label className="text-[11px] text-neutral-400 font-medium uppercase tracking-wider">Resolution</label>
                    <select
                      value={resolution}
                      onChange={(e) => {
                        const val = e.target.value;
                        setResolution(val);
                        if (val === '1080x1920') {
                          setCustomWidth(1080);
                          setCustomHeight(1920);
                        } else if (val === '1920x1080') {
                          setCustomWidth(1920);
                          setCustomHeight(1080);
                        }
                      }}
                      className="bg-neutral-800/80 text-neutral-200 text-sm rounded-lg px-3 py-1.5 border border-neutral-700/50 focus:outline-none focus:border-neutral-600 focus:ring-1 focus:ring-neutral-600 transition-colors cursor-pointer"
                    >
                      <option value="1080x1920">Mobile (1080×1920)</option>
                      <option value="1920x1080">Desktop (1920×1080)</option>
                      <option value="custom">Custom</option>
                    </select>
                  </div>
                  {resolution === 'custom' && (
                    <div className="flex gap-2 items-end min-w-[180px]">
                      <div className="flex flex-col gap-1.5">
                        <label className="text-[11px] text-neutral-400 uppercase tracking-wider">Width</label>
                        <input
                          type="number"
                          min={1}
                          value={customWidth}
                          onChange={(e) => setCustomWidth(Number(e.target.value))}
                          className="bg-neutral-800/80 text-white text-sm rounded-lg px-3 py-1.5 border border-neutral-700/50 focus:outline-none focus:border-neutral-600 w-20"
                        />
                      </div>
                      <div className="flex flex-col gap-1.5">
                        <label className="text-[11px] text-neutral-400 uppercase tracking-wider">Height</label>
                        <input
                          type="number"
                          min={1}
                          value={customHeight}
                          onChange={(e) => setCustomHeight(Number(e.target.value))}
                          className="bg-neutral-800/80 text-white text-sm rounded-lg px-3 py-1.5 border border-neutral-700/50 focus:outline-none focus:border-neutral-600 w-20"
                        />
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
        <div className="relative flex min-h-12 w-full items-end">
          {leftSlot ? (
            <div
              className={cn(
                "relative z-50 flex h-12 shrink-0 pl-2 transition-all",
                isMultiline ? "items-end pb-1" : "items-center",
              )}
            >
              {leftSlot}
            </div>
          ) : null}
          <textarea
            onChange={(e) => {
              setValue(e.target.value);
              onChange && onChange(e);
            }}
            onKeyDown={handleKeyDown}
            ref={inputRef}
            value={value}
            rows={1}
            disabled={isGenerating}
            className={cn(
              "relative z-50 my-1 max-h-[10rem] min-h-10 flex-1 resize-none border-none bg-transparent px-3 py-2 pr-16 text-sm leading-6 text-white focus:outline-none focus:ring-0 sm:text-base input-scrollbar",
              isGenerating && "cursor-not-allowed opacity-50"
            )}
          />

          <div className="pointer-events-none absolute inset-0 flex h-12 items-center">
            <AnimatePresence mode="wait">
              {!value && (
                <motion.p
                  initial={{
                    y: 5,
                    opacity: 0,
                  }}
                  key={`current-placeholder-${currentPlaceholder}`}
                  animate={{
                    y: 0,
                    opacity: 1,
                  }}
                  exit={{
                    y: -15,
                    opacity: 0,
                  }}
                  transition={{
                    duration: 0.3,
                    ease: "linear",
                  }}
                  className={cn(
                    "w-[calc(100%-5rem)] truncate text-left text-sm font-normal text-zinc-500 sm:text-base",
                    leftSlot ? "pl-14" : "pl-4 sm:pl-12",
                  )}
                >
                  {isGenerating ? "Click the stop button to cancel..." : placeholders[currentPlaceholder]}
                </motion.p>
              )}
            </AnimatePresence>
          </div>

          <div className="pointer-events-none absolute bottom-0 right-0 top-0 z-40 w-14 bg-inherit" />
          <button
            disabled={(!value && !isGenerating) || (isGenerating && !onCancel)}
            type={isGenerating ? "button" : "submit"}
            onClick={isGenerating ? onCancel : undefined}
            className={cn(
              "absolute right-3 z-50 flex h-8 w-8 items-center justify-center rounded-full bg-zinc-900 transition duration-200 disabled:bg-zinc-800",
              isMultiline ? "bottom-2" : "top-1/2 -translate-y-1/2",
              (isGenerating) && "bg-zinc-800 cursor-pointer",
              (!value && !isGenerating) ? "opacity-30 cursor-not-allowed" : "cursor-pointer"
            )}
          >
            {isGenerating ? (
              <div className="h-2.5 w-2.5 bg-white rounded-[1px]" />
            ) : (
              <motion.svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                className="text-gray-300 h-4 w-4"
              >
                <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                <motion.path
                  d="M5 12l14 0"
                  initial={{
                    strokeDasharray: "50%",
                    strokeDashoffset: "50%",
                  }}
                  animate={{
                    strokeDashoffset: value ? 0 : "50%",
                  }}
                  transition={{
                    duration: 0.3,
                    ease: "linear",
                  }}
                />
                <path d="M13 18l6 -6" />
                <path d="M13 6l6 6" />
              </motion.svg>
            )}
          </button>
        </div>
      </form>

      {/* Flying Bubble Animation */}
      <AnimatePresence>
        {flyingBubble && (
          <motion.div
            initial={{
              position: "fixed",
              left: flyingBubble.startRect.left,
              top: flyingBubble.startRect.top,
              width: flyingBubble.startRect.width,
              height: flyingBubble.startRect.height,
              backgroundColor: "#000000",
              borderColor: "#262626",
              borderWidth: "1px",
              borderStyle: "solid",
              borderRadius: "16px",
              opacity: 1,
              color: "#ffffff",
              paddingLeft: leftSlot ? "48px" : "12px",
              paddingTop: "8px",
              paddingRight: "48px",
              paddingBottom: "8px",
              fontSize: "14px",
              display: "flex",
              alignItems: "center",
              zIndex: 99999,
              pointerEvents: "none",
              boxShadow: "0 10px 25px -5px rgba(0, 0, 0, 0.5)",
            }}
            animate={
              animStep === "flying" && targetRect
                ? {
                    left: targetRect.left,
                    top: targetRect.top,
                    width: targetRect.width,
                    height: targetRect.height,
                    backgroundColor: "#262626",
                    borderColor: "#262626",
                    borderRadius: "16px 2px 16px 16px",
                    opacity: [1, 1, 0],
                    paddingLeft: "16px",
                    paddingTop: "10px",
                    paddingRight: "16px",
                    paddingBottom: "10px",
                  }
                : animStep === "done"
                ? { opacity: 0 }
                : {}
            }
            transition={{
              duration: 0.35,
              ease: [0.25, 1, 0.5, 1],
            }}
            onAnimationComplete={() => {
              if (animStep === "flying" || animStep === "done") {
                setFlyingBubble(null);
                setAnimStep("start");
              }
            }}
          >
            <span className="truncate w-full text-left text-sm leading-6 sm:text-base">{flyingBubble.text}</span>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
