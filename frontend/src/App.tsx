import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

import { Button } from "@/components/ui/button"
import { BackgroundBeams } from "@/components/ui/background-beams";

function App() {
  const [count, setCount] = useState(0)

  return (
    <div style={{ position: "relative", minHeight: "100vh", overflow: "hidden", backgroundColor: "black" }}>
      {/* Background Beams */}
      <BackgroundBeams className="z-0" />
      {/* Main Content */}

    </div>
  )
}

export default App
