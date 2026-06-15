"use client";
import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "motion/react";
import { cn } from "@/lib/utils";

export const LayoutTextFlip = ({
  text = "Build Amazing",
  words = ["Landing Pages", "Component Blocks", "Page Sections", "3D Shaders"],
  duration = 3000,
}: {
  text: string;
  words: string[];
  duration?: number;
}) => {
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentIndex((prevIndex) => (prevIndex + 1) % words.length);
    }, duration);

    return () => clearInterval(interval);
  }, []);

  return (
    <>
      <motion.span
        layoutId="subtext"
        // Make the main static text noticeably larger than the flipping words
        className="text-4xl font-bold tracking-tight drop-shadow-lg md:text-7xl block md:inline-block mb-2 md:mb-0 md:mr-4"
      >
        {text}
      </motion.span>

      <motion.span
        layout
        // Keep the flipping words a bit smaller so the main title stands out
        className="relative w-fit overflow-hidden rounded-md bg-[#171717] px-3 py-1.5 md:px-4 md:py-2 font-sans text-xl sm:text-2xl font-bold tracking-tight text-white shadow-sm drop-shadow-lg md:text-5xl inline-block"
      >
        <AnimatePresence mode="popLayout">
          <motion.span
            key={currentIndex}
            initial={{ y: -40, filter: "blur(10px)" }}
            animate={{
              y: 0,
              filter: "blur(0px)",
            }}
            exit={{ y: 50, filter: "blur(10px)", opacity: 0 }}
            transition={{
              duration: 0.5,
            }}
            className={cn("inline-block whitespace-nowrap")}
          >
            {words[currentIndex]}
          </motion.span>
        </AnimatePresence>
      </motion.span>
    </>
  );
};
