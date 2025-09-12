"use client";

import { AnimatePresence, motion } from "motion/react";
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
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onSubmit: (e: React.FormEvent<HTMLFormElement>, options: { format: string; quality: string }) => void;
  onCancel?: () => void;
  isGenerating?: boolean;
}) {
  const [currentPlaceholder, setCurrentPlaceholder] = useState(0);
  const [format, setFormat] = useState("mp4");
  const [quality, setQuality] = useState("ql");
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
      clearInterval(intervalRef.current); // Clear the interval when the tab is not visible
      intervalRef.current = null;
    } else if (document.visibilityState === "visible") {
      startAnimation(); // Restart the interval when the tab becomes visible
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

  const canvasRef = useRef<HTMLCanvasElement>(null);
  const newDataRef = useRef<any[]>([]);
  const inputRef = useRef<HTMLInputElement>(null);
  const [value, setValue] = useState("");
  const [animating, setAnimating] = useState(false);

  const draw = useCallback(() => {
    if (!inputRef.current) return;
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    canvas.width = 800;
    canvas.height = 800;
    ctx.clearRect(0, 0, 800, 800);
    const computedStyles = getComputedStyle(inputRef.current);

    const fontSize = parseFloat(computedStyles.getPropertyValue("font-size"));
    ctx.font = `${fontSize * 2}px ${computedStyles.fontFamily}`;
    ctx.fillStyle = "#FFF";
    ctx.fillText(value, 16, 40);

    const imageData = ctx.getImageData(0, 0, 800, 800);
    const pixelData = imageData.data;
    const newData: any[] = [];

    for (let t = 0; t < 800; t++) {
      let i = 4 * t * 800;
      for (let n = 0; n < 800; n++) {
        let e = i + 4 * n;
        if (
          pixelData[e] !== 0 &&
          pixelData[e + 1] !== 0 &&
          pixelData[e + 2] !== 0
        ) {
          newData.push({
            x: n,
            y: t,
            color: [
              pixelData[e],
              pixelData[e + 1],
              pixelData[e + 2],
              pixelData[e + 3],
            ],
          });
        }
      }
    }

    newDataRef.current = newData.map(({ x, y, color }) => ({
      x,
      y,
      r: 1,
      color: `rgba(${color[0]}, ${color[1]}, ${color[2]}, ${color[3]})`,
    }));
  }, [value]);

  useEffect(() => {
    draw();
  }, [value, draw]);

  // Handle clicking outside the options panel
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (optionsRef.current && !optionsRef.current.contains(event.target as Node)) {
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

  const animate = (start: number) => {
    const animateFrame = (pos: number = 0) => {
      requestAnimationFrame(() => {
        const newArr = [];
        for (let i = 0; i < newDataRef.current.length; i++) {
          const current = newDataRef.current[i];
          if (current.x < pos) {
            newArr.push(current);
          } else {
            if (current.r <= 0) {
              current.r = 0;
              continue;
            }
            current.x += Math.random() > 0.5 ? 1 : -1;
            current.y += Math.random() > 0.5 ? 1 : -1;
            current.r -= 0.05 * Math.random();
            newArr.push(current);
          }
        }
        newDataRef.current = newArr;
        const ctx = canvasRef.current?.getContext("2d");
        if (ctx) {
          ctx.clearRect(pos, 0, 800, 800);
          newDataRef.current.forEach((t) => {
            const { x: n, y: i, r: s, color: color } = t;
            if (n > pos) {
              ctx.beginPath();
              ctx.rect(n, i, s, s);
              ctx.fillStyle = color;
              ctx.strokeStyle = color;
              ctx.stroke();
            }
          });
        }
        if (newDataRef.current.length > 0) {
          animateFrame(pos - 8);
        } else {
          setValue("");
          setAnimating(false);
        }
      });
    };
    animateFrame(start);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && !animating) {
      vanishAndSubmit();
    }
  };

  const vanishAndSubmit = () => {
    setAnimating(true);
    draw();

    const value = inputRef.current?.value || "";
    if (value && inputRef.current) {
      const maxX = newDataRef.current.reduce(
        (prev, current) => (current.x > prev ? current.x : prev),
        0
      );
      animate(maxX);
    }
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (isGenerating && onCancel) {
      onCancel();
    } else {
      vanishAndSubmit();
      onSubmit && onSubmit(e, { format, quality });
    }
  };
  return (
    <div className="w-full relative max-w-xl mx-auto" ref={optionsRef}>
      {/* Options Panel */}
      <div className={cn(
        "mb-3 p-3 rounded-lg bg-[#202020] border border-gray-600 transition-all duration-200",
        showOptions ? "opacity-100 max-h-32" : "opacity-0 max-h-0 overflow-hidden p-0 mb-0 border-0"
      )}>
        <div className="flex gap-4 items-center flex-wrap">
          <div className="flex flex-col gap-1 min-w-[80px]">
            <label className="text-xs text-gray-400 font-medium">Format</label>
            <select
              value={format}
              onChange={(e) => setFormat(e.target.value)}
              className="bg-[#2a2a2a] text-white text-sm rounded px-3 py-1.5 border border-gray-600 focus:outline-none focus:border-gray-500 focus:ring-1 focus:ring-gray-500 transition-colors"
            >
              <option value="mp4">MP4</option>
              <option value="gif">GIF</option>
            </select>
          </div>
          <div className="flex flex-col gap-1 min-w-[100px]">
            <label className="text-xs text-gray-400 font-medium">Quality</label>
            <select
              value={quality}
              onChange={(e) => setQuality(e.target.value)}
              className="bg-[#2a2a2a] text-white text-sm rounded px-3 py-1.5 border border-gray-600 focus:outline-none focus:border-gray-500 focus:ring-1 focus:ring-gray-500 transition-colors"
            >
              <option value="ql">Low (ql)</option>
              <option value="qm">Medium (qm)</option>
              <option value="qh">High (qh)</option>
            </select>
          </div>
          <div className="flex items-end h-full">
            <div className="text-xs text-gray-500 mb-1">
              {format.toUpperCase()} • {quality === 'ql' ? 'Low' : quality === 'qm' ? 'Medium' : 'High'} Quality
            </div>
          </div>
        </div>
      </div>
      
      <form
        className={cn(
          "w-full relative h-12 rounded-full overflow-hidden transition duration-200",
          "bg-[#202020] border border-gray-600",
          value && "border-gray-500"
        )}
        onSubmit={handleSubmit}
      >
      <canvas
        className={cn(
          "absolute pointer-events-none  text-base transform scale-50 top-[20%] left-2 sm:left-8 origin-top-left filter invert dark:invert-0 pr-20",
          !animating ? "opacity-0" : "opacity-100"
        )}
        ref={canvasRef}
      />
      <input
        onChange={(e) => {
          if (!animating) {
            setValue(e.target.value);
            onChange && onChange(e);
          }
        }}
        onKeyDown={handleKeyDown}
        ref={inputRef}
        value={value}
        type="text"
        disabled={isGenerating}
        className={cn(
          "w-full relative text-sm sm:text-base z-50 border-none text-white bg-transparent h-full rounded-full focus:outline-none focus:ring-0 pl-4 sm:pl-10 pr-20",
          "placeholder:text-gray-400",
          animating && "text-transparent",
          isGenerating && "cursor-not-allowed opacity-50"
        )}
      />

      <button
        disabled={!value && !isGenerating}
        type="submit"
        className={cn(
          "absolute right-2 top-1/2 z-50 -translate-y-1/2 h-8 w-8 rounded-full transition duration-200 flex items-center justify-center",
          "bg-[#202020] border border-gray-600",
          (value || isGenerating) ? (isGenerating ? "bg-[#202020] text-red-400 hover:bg-gray-700" : "bg-white text-black hover:bg-gray-100") : "bg-[#202020] text-gray-400",
          (!value && !isGenerating) && "cursor-not-allowed"
        )}
      >
        {isGenerating ? (
          // Cancel icon (X)
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
            className="h-4 w-4 text-red-400"
          >
            <path stroke="none" d="M0 0h24v24H0z" fill="none" />
            <path d="M18 6l-12 12" />
            <path d="M6 6l12 12" />
          </motion.svg>
        ) : (
          // Submit icon (arrow)
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
            className={cn("h-4 w-4", value ? "text-black" : "text-gray-400")}
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

      <div className="absolute inset-0 flex items-center rounded-full pointer-events-none">
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
              className="text-gray-400 text-sm sm:text-base font-normal pl-4 sm:pl-12 text-left w-[calc(100%-2rem)] truncate"
            >
              {isGenerating ? "Click the cancel button to stop generation..." : placeholders[currentPlaceholder]}
            </motion.p>
          )}
        </AnimatePresence>
      </div>
    </form>
    
    {/* Options Toggle Button */}
    <button
      type="button"
      onClick={() => setShowOptions(!showOptions)}
      className="mt-2 mx-auto flex items-center gap-2 px-3 py-1.5 text-xs text-gray-400 hover:text-gray-300 transition-colors rounded hover:bg-gray-800/50"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="12"
        height="12"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        className="w-3 h-3"
      >
        <circle cx="12" cy="12" r="3" />
        <path d="M12 1v6M12 17v6M4.22 4.22l4.24 4.24M15.54 15.54l4.24 4.24M1 12h6M17 12h6M4.22 19.78l4.24-4.24M15.54 8.46l4.24-4.24" />
      </svg>
      <span>{showOptions ? "Hide" : "Show"} format and quality</span>
      <motion.svg
        xmlns="http://www.w3.org/2000/svg"
        width="12"
        height="12"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        animate={{ rotate: showOptions ? 180 : 0 }}
        transition={{ duration: 0.2 }}
        className="w-3 h-3"
      >
        <path d="M6 9l6 6 6-6" />
      </motion.svg>
    </button>
    </div>
  );
}
