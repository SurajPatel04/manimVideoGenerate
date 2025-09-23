import { IconBrandGithub, IconBrandLinkedin } from "@tabler/icons-react";
import { useNavigate } from "react-router-dom";

export default function Header() {
  const navigate = useNavigate();

  return (
    <div className="mb-6 flex items-center justify-between">
      <button
        onClick={() => navigate('/')}
        className="text-white font-bold text-sm hover:opacity-90"
        aria-label="Go to homepage"
      >
        Manim
      </button>

      <div className="flex items-center space-x-3">
        <a href="https://www.linkedin.com/" target="_blank" rel="noreferrer" className="text-neutral-300 hover:text-blue-500">
          <IconBrandLinkedin className="w-5 h-5" />
        </a>
        <a href="https://github.com/" target="_blank" rel="noreferrer" className="text-neutral-300 hover:text-white">
          <IconBrandGithub className="w-5 h-5" />
        </a>
      </div>
    </div>
  );
}
