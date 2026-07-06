"use client";

import React, { useState } from "react";
import { 
  SandpackProvider, 
  SandpackLayout, 
  SandpackCodeEditor 
} from "@codesandbox/sandpack-react";
import { Send, Database, Cpu, Layers, FileCode, Terminal } from "lucide-react";

export default function ArcStudioDashboard() {
  const [query, setQuery] = useState("");
  const [activeFile, setActiveFile] = useState("/01_schema.sql");
  const [chatHistory, setChatHistory] = useState([
    { 
      role: "assistant", 
      text: "Welcome to ARC Studio. Ask me any conceptual architecture, schema logic, or integration pipeline questions about your repository." 
    }
  ]);

  const fileList = [
    { path: "/01_schema.sql", name: "01_schema.sql" },
    { path: "/auth.py", name: "auth.py" }
  ];

  const handleAskARC = async () => {
    if (!query.trim()) return;
    
    setChatHistory((prev) => [...prev, { role: "user", text: query }]);
    const currentQuery = query;
    setQuery("");

    try {
      const response = await fetch("http://localhost:8000/generate/api", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          question: currentQuery,
          repository_id: 30
        }),
      });

      if (!response.ok) throw new Error("Retrieval connection failed");
      const data = await response.json();
      
      setChatHistory((prev) => [
        ...prev, 
        { role: "assistant", text: data.answer || "No response generated." }
      ]);
    } catch (error) {
      setChatHistory((prev) => [
        ...prev, 
        { role: "assistant", text: "❌ Error connecting to ARC backend service. Ensure FastAPI is running." }
      ]);
    }
  };

  return (
    <div className="h-screen w-screen bg-zinc-950 text-zinc-100 flex flex-col font-sans overflow-hidden">
      
      {/* 1. Global Navigation Bar */}
      <header className="h-14 border-b border-zinc-800 px-6 flex items-center justify-between bg-zinc-900 z-10 flex-shrink-0">
        <div className="flex items-center gap-3">
          <div className="bg-indigo-600 p-1.5 rounded-lg text-white">
            <Cpu size={18} />
          </div>
          <h1 className="font-bold text-base tracking-wider text-white">
            ARC <span className="text-indigo-400 font-medium">STUDIO</span>
          </h1>
        </div>
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2 text-xs text-zinc-400 bg-zinc-950 px-3 py-1.5 rounded-md border border-zinc-800">
            <Database size={12} className="text-emerald-400" />
            <span>Milvus DB: Active (IP Metric)</span>
          </div>
          <div className="flex items-center gap-2 text-xs text-zinc-400 bg-zinc-950 px-3 py-1.5 rounded-md border border-zinc-800">
            <Layers size={12} className="text-indigo-400" />
            <span>Subject: Smart IMS</span>
          </div>
        </div>
      </header>

      {/* 2. Main Studio Grid Workspace */}
      <div className="flex-1 flex overflow-hidden bg-zinc-950">
        
        {/* LEFT CANVAS PANEL: Stretched fully down with no bottom padding cutoff */}
        <div className="flex-1 h-full p-4 pb-4 flex flex-col overflow-hidden">
          <SandpackProvider             
            customSetup={{ entry: "/01_schema.sql" }}
            theme="dark"
            files={{
              "/01_schema.sql": {
                code: `-- Smart Inventory Management System Schema\nCREATE TABLE Supplier (\n    SupplierID INT UNSIGNED NOT NULL AUTO_INCREMENT,\n    SupplierName VARCHAR(120) NOT NULL,\n    PRIMARY KEY (SupplierID)\n);`
              },
              "/auth.py": {
                code: `# Authentication interface module\ndef verify_login(email, password):\n    pass`
              }
            }}
            activeFile={activeFile}
            options={{
              visibleFiles: [activeFile]
            }}
            // Overrides the internal root element height constraints cleanly
            style={{ height: "100%", display: "flex", flexDirection: "column" }}
          >
            <SandpackLayout 
              className="flex-1 rounded-xl border border-zinc-800 overflow-hidden shadow-2xl flex"
              style={{ height: "100%", minHeight: "100%" }}
            >
              
              {/* FILE EXPLORER PANEL: Full height sidebar container */}
              <div 
                className="w-60 border-r border-zinc-800 h-full p-3 flex flex-col gap-1 select-none flex-shrink-0"
                style={{ backgroundColor: "#151515" }}
              >
                <div className="text-[11px] font-bold text-zinc-500 uppercase tracking-wider px-2 mb-2 flex items-center gap-1.5">
                  <Terminal size={10} /> Workspace Files
                </div>
                {fileList.map((file) => (
                  <button
                    key={file.path}
                    onClick={() => setActiveFile(file.path)}
                    className={`w-full flex items-center gap-2 px-2 py-1.5 rounded-md text-sm font-medium transition-all duration-150 ${
                      activeFile === file.path
                        ? "bg-indigo-600/15 text-indigo-400 border border-indigo-500/30 shadow-sm"
                        : "text-zinc-400 hover:bg-zinc-800/50 hover:text-zinc-200 border border-transparent"
                    }`}
                  >
                    <FileCode size={14} className={activeFile === file.path ? "text-indigo-400" : "text-zinc-500"} />
                    <span className="truncate">{file.name}</span>
                  </button>
                ))}
              </div>

              {/* EDITOR PANEL: Stretched explicitly to 100% inner space */}
              <SandpackCodeEditor 
                showTabs={false} 
                showLineNumbers
                showInlineErrors
                wrapContent
                className="flex-1 h-full text-zinc-300 font-mono" 
                style={{ height: "100%" }}
              />
            </SandpackLayout>
          </SandpackProvider>
        </div>

        {/* RIGHT PANEL: Codex-style AI Retrieval Assistant */}
        <aside className="w-[420px] border-l border-zinc-800 bg-zinc-900/40 flex flex-col h-full shadow-2xl flex-shrink-0">
          <div className="p-4 border-b border-zinc-800 bg-zinc-900/80 backdrop-blur flex justify-between items-center">
            <div>
              <h2 className="font-semibold text-sm text-zinc-200">Repository Intelligence</h2>
              <p className="text-xs text-zinc-500">Cross-file semantic search active</p>
            </div>
            <div className="flex gap-1.5">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
            </div>
          </div>

          <div className="flex-1 p-4 overflow-y-auto space-y-4 scrollbar-thin scrollbar-thumb-zinc-800">
            {chatHistory.map((msg, idx) => (
              <div 
                key={idx} 
                className={`p-3.5 rounded-xl text-sm leading-relaxed max-w-[88%] shadow-sm ${
                  msg.role === "user" 
                    ? "bg-indigo-600 text-white ml-auto rounded-tr-none" 
                    : "bg-zinc-800 text-zinc-200 border border-zinc-700/60 rounded-tl-none whitespace-pre-wrap"
                }`}
              >
                {msg.text}
              </div>
            ))}
          </div>

          <div className="p-4 border-t border-zinc-800 bg-zinc-900/80 backdrop-blur">
            <div className="flex items-center gap-2 bg-zinc-950 rounded-xl p-2.5 border border-zinc-800 focus-within:border-indigo-500/80 transition-all duration-200 shadow-inner">
              <input
                type="text"
                placeholder="Ask ARC regarding schemas, flows, or endpoints..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleAskARC()}
                className="bg-transparent flex-1 outline-none text-sm text-zinc-100 placeholder-zinc-600 px-1"
              />
              <button 
                onClick={handleAskARC}
                className="p-2 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white transition-all duration-200 hover:scale-105"
              >
                <Send size={14} />
              </button>
            </div>
          </div>
        </aside>

      </div>
    </div>
  );
}