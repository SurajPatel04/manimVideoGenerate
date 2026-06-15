"use client";
import { cn } from "@/lib/utils";
import React, { useState, createContext, useContext } from "react";
import { motion } from "motion/react";
import { IconMenu2 } from "@tabler/icons-react";
import { Link } from "react-router-dom";

interface Links {
  label: string;
  href: string;
  icon: React.JSX.Element | React.ReactNode;
}

interface SidebarContextProps {
  open: boolean;
  setOpen: React.Dispatch<React.SetStateAction<boolean>>;
  animate: boolean;
  autoOpen: boolean;
}

const SidebarContext = createContext<SidebarContextProps | undefined>(
  undefined
);

export const useSidebar = () => {
  const context = useContext(SidebarContext);
  if (!context) {
    throw new Error("useSidebar must be used within a SidebarProvider");
  }
  return context;
};

export const SidebarProvider = ({
  children,
  open: openProp,
  setOpen: setOpenProp,
  animate = true,
  autoOpen = true,
}: {
  children: React.ReactNode;
  open?: boolean;
  setOpen?: React.Dispatch<React.SetStateAction<boolean>>;
  animate?: boolean;
  autoOpen?: boolean;
}) => {
  const [openState, setOpenState] = useState(false);

  const open = openProp !== undefined ? openProp : openState;
  const setOpen = setOpenProp !== undefined ? setOpenProp : setOpenState;

  return (
    <SidebarContext.Provider value={{ open, setOpen, animate, autoOpen }}>
      {children}
    </SidebarContext.Provider>
  );
};

export const Sidebar = ({
  children,
  open,
  setOpen,
  animate,
  autoOpen,
}: {
  children: React.ReactNode;
  open?: boolean;
  setOpen?: React.Dispatch<React.SetStateAction<boolean>>;
  animate?: boolean;
  autoOpen?: boolean;
}) => {
  return (
    <SidebarProvider
      animate={animate}
      autoOpen={autoOpen}
      open={open}
      setOpen={setOpen}
    >
      {children}
    </SidebarProvider>
  );
};

export const SidebarBody = (props: React.ComponentProps<typeof motion.div> & { centerContent?: React.ReactNode; rightContent?: React.ReactNode }) => {
  return (
    <>
      <DesktopSidebar {...props} />
      <MobileSidebar {...(props as any)} />
    </>
  );
};

export const DesktopSidebar = ({
  className,
  children,
  centerContent,
  rightContent,
  ...props
}: React.ComponentProps<typeof motion.div> & { centerContent?: React.ReactNode; rightContent?: React.ReactNode }) => {
  const { open, setOpen, animate, autoOpen } = useSidebar();
  return (
    <>
      <motion.div
        className={cn(
          "h-full py-4 hidden md:flex md:flex-col bg-black border-r border-neutral-800 shrink-0",
          open ? "px-4" : "px-2",
          className
        )}
        animate={{
          width: animate ? (open ? "300px" : "68px") : "300px",
        }}
        onMouseEnter={() => {
          if (autoOpen) {
            setOpen(true);
          }
        }}
        onMouseLeave={() => {
          if (autoOpen) {
            setOpen(false);
          }
        }}
        {...props}
      >
        {children}
      </motion.div>
    </>
  );
};

export const MobileSidebar = ({
  className,
  children,
  centerContent,
  rightContent,
  ...props
}: React.ComponentProps<"div"> & { centerContent?: React.ReactNode; rightContent?: React.ReactNode }) => {
  const { open, setOpen } = useSidebar();
  return (
    <>
      <div
        className={cn(
          "h-14 px-4 flex flex-row md:hidden items-center justify-between bg-black border-b border-neutral-800 w-full relative"
        )}
        {...props}
      >
        <div className="flex items-center z-20">
          <IconMenu2
            className="text-neutral-200 h-6 w-6 cursor-pointer hover:text-white transition-colors"
            onClick={() => setOpen(!open)}
          />
        </div>
        <div className="absolute inset-0 flex items-center justify-center pointer-events-none z-10">
          <div className="pointer-events-auto">
            {centerContent}
          </div>
        </div>
        <div className="flex items-center z-20">
          {rightContent}
        </div>
        <motion.div
          initial={false}
          animate={{ x: open ? 0 : "-100%", opacity: open ? 1 : 0 }}
          transition={{
            duration: 0.3,
            ease: "easeInOut",
          }}
          className={cn(
            "fixed h-full w-full inset-0 bg-black p-6 z-[100] flex flex-col justify-between",
            open ? "pointer-events-auto" : "pointer-events-none",
            className
          )}
        >

          {children}
        </motion.div>
      </div>
    </>
  );
};

export const SidebarLink = ({
  link,
  className,
  ...props
}: {
  link: Links;
  className?: string;
  onClick?: () => void;
}) => {
  const { open, animate } = useSidebar();
  return (
    <Link
      to={link.href}
      className={cn(
        "flex items-center gap-2 group/sidebar py-2 rounded-lg transition-colors hover:bg-neutral-900 focus:bg-neutral-900 active:bg-neutral-800 outline-none focus:outline-none",
        open ? "justify-start px-0" : "justify-center px-2",
        className
      )}
      {...(props as any)}
    >
      {link.icon}

      {open || !animate ? (
        <span className="inline-block whitespace-pre !p-0 !m-0 text-sm text-neutral-700 transition duration-150 group-hover/sidebar:translate-x-1 dark:text-neutral-200">
          {link.label}
        </span>
      ) : null}
    </Link>
  );
};
