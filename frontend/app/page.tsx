import ChatInterface from "./components/ChatInterface";

export default function Home() {
  return (
    <main className="min-h-screen relative overflow-hidden bg-black">
      {/* Background Layer (Z-0 to Z-2 handled in CSS) */}
      <div className="stars"></div>

      {/* Background Glows */}
      <div className="absolute top-[-10%] left-[-10%] w-[50%] h-[50%] bg-cyan-900/10 rounded-full blur-[150px] pointer-events-none z-[1]" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[50%] h-[50%] bg-blue-900/10 rounded-full blur-[150px] pointer-events-none z-[1]" />

      {/* Foreground Content */}
      <ChatInterface />
    </main>
  );
}
