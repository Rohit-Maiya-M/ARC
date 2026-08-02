"use client";

import React, { useState, useRef, useEffect } from "react";
import { 
  SandpackProvider, 
  SandpackLayout, 
  SandpackCodeEditor 
} from "@codesandbox/sandpack-react";
import { Send, Database, Cpu, Layers, FileCode, Terminal, UploadCloud, Loader2, Folder, FolderOpen, ChevronDown, ChevronRight, Play, TerminalSquare, Trash2, Maximize2, Minimize2 } from "lucide-react";

interface TreeFile {
  type: "file";
  path: string;
  name: string;
}

interface TreeFolder {
  type: "folder";
  name: string;
  children: Record<string, TreeFile | TreeFolder>;
}

type TreeNode = TreeFile | TreeFolder;

export default function ArcStudioDashboard() {
  const [currentStep, setCurrentStep] = useState<"UPLOAD" | "INDEXING" | "WORKSPACE">("UPLOAD");
  
  // Dynamic Left Sidebar Resizing Configurations
  const [sidebarWidth, setSidebarWidth] = useState(240); 
  const isResizingRef = useRef(false);

  // Fast Testing State Mount Variables
  const [testRepoInput, setTestRepoInput] = useState("");

  // Terminal Logging Window Panels States
  const [terminalLogs, setTerminalLogs] = useState<string[]>([
    "⚙️ ARC Studio Core Execution Subsystem Initialized.",
    "🌐 Ready for Spring Boot Framework Handshake connections on Port 8080..."
  ]);
  const [isTerminalExpanded, setIsTerminalExpanded] = useState(true);
  
  // Workspace Dynamic Tree File Structural Maps
  const [virtualFiles, setVirtualFiles] = useState<Record<string, { code: string }>>({});
  const [fileTree, setFileTree] = useState<Record<string, TreeNode>>({});
  const [activeFile, setActiveFile] = useState("");
  const [expandedFolders, setExpandedFolders] = useState<Record<string, boolean>>({});
  
  // Context Metadata
  const [targetRepoId, setTargetRepoId] = useState<number | null>(null);
  const [projectName, setProjectName] = useState("Selected Repository");

  const [query, setQuery] = useState("");
  const [chatHistory, setChatHistory] = useState([
    { 
      role: "assistant", 
      text: "Welcome to ARC Studio. Ask me any conceptual architecture, schema logic, or integration pipeline questions about your repository." 
    }
  ]);

  // Terminal logging helper utility
  const logToTerminal = (message: string) => {
    const timestamp = new Date().toLocaleTimeString();
    setTerminalLogs((prev) => [...prev, `[${timestamp}] ${message}`]);
  };

  // Drag Handle Listeners Logic for Resizing
  const startResizing = (e: React.MouseEvent) => {
    e.preventDefault();
    isResizingRef.current = true;
    document.body.style.cursor = "col-resize";
    document.body.style.userSelect = "none"; 
  };

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (!isResizingRef.current) return;
      const newWidth = Math.max(160, Math.min(500, e.clientX - 16)); 
      setSidebarWidth(newWidth);
    };

    const handleMouseUp = () => {
      if (isResizingRef.current) {
        isResizingRef.current = false;
        document.body.style.cursor = "default";
        document.body.style.userSelect = "auto";
      }
    };

    window.addEventListener("mousemove", handleMouseMove);
    window.addEventListener("mouseup", handleMouseUp);
    return () => {
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("mouseup", handleMouseUp);
    };
  }, []);

  // PRIVACY-FILTERED TREE PARSER (Strips local paths completely)
  const buildTreeFromPaths = (paths: string[]): Record<string, TreeNode> => {
    const root: Record<string, TreeNode> = {};

    paths.forEach((rawPath) => {
      // Standardize windows backslashes to clean uniform web forward slashes
      let cleanPath = rawPath.replace(/\\/g, "/");

      // Locate the entry point of the project root ("ARC" or "IMS")
      // Splitting by 'extracted/' allows us to grab everything *after* the backend's absolute disk path prefix
      if (cleanPath.includes("/extracted/")) {
        const structuralSegments = cleanPath.split("/extracted/");
        if (structuralSegments.length > 1) {
          // Removes the UUID hash segment to start straight from your source root name
          const subSegments = structuralSegments[1].split("/");
          subSegments.shift(); // Drop the dynamic file path reference id
          cleanPath = subSegments.join("/");
        }
      } else if (cleanPath.includes("C:/")) {
        // Fallback catch boundary to remove nested disk fragments explicitly if structural segments shift
        const alternativeSlices = cleanPath.split("/");
        const anchorIndex = alternativeSlices.findIndex(s => s === "ARC" || s === "IMS");
        if (anchorIndex !== -1) {
          cleanPath = alternativeSlices.slice(anchorIndex).join("/");
        }
      }

      // Strip away any trailing or leading edge loose slashes
      if (cleanPath.startsWith("/")) cleanPath = cleanPath.slice(1);

      const parts = cleanPath.split("/");
      let currentLevel = root;

      parts.forEach((part, index) => {
        if (!part.trim()) return;
        const isLast = index === parts.length - 1;

        if (isLast) {
          currentLevel[part] = {
            type: "file",
            path: rawPath, // Keeps the original absolute path bound for backend requests
            name: part,
          };
        } else {
          if (!currentLevel[part] || currentLevel[part].type === "file") {
            currentLevel[part] = {
              type: "folder",
              name: part,
              children: {},
            };
          }
          currentLevel = (currentLevel[part] as TreeFolder).children;
        }
      });
    });

    return root;
  };

  const toggleFolder = (folderId: string) => {
    setExpandedFolders((prev) => ({ ...prev, [folderId]: !prev[folderId] }));
  };

  const findFirstFilePath = (nodes: Record<string, TreeNode>): string => {
    for (const key in nodes) {
      if (nodes[key].type === "file") return (nodes[key] as TreeFile).path;
      const childPath = findFirstFilePath((nodes[key] as TreeFolder).children);
      if (childPath) return childPath;
    }
    return "";
  };

  // DYNAMIC BYPASS MOUNT CONTROLLER
  const mountRepositoryById = async (idToMount: string) => {
    if (!idToMount.trim()) return;
    
    setCurrentStep("INDEXING");
    const repoId = parseInt(idToMount, 10);
    setTargetRepoId(repoId);
    setProjectName(`Repository DB ID: ${repoId}`);
    logToTerminal(`Initiating instant lifecycle mount for Repository ID: ${repoId}...`);

    try {
      const filesResponse = await fetch(`http://localhost:8080/repositories/${repoId}/files`);
      if (!filesResponse.ok) throw new Error("Failed to load specified project structure map");
      
      const incomingFilesMap = await filesResponse.json();
      const paths = Object.keys(incomingFilesMap);

      if (paths.length === 0) {
        throw new Error("Target repository mapping rows are empty.");
      }

      const sandpackFilesBlock: Record<string, { code: string }> = {};
      Object.entries(incomingFilesMap).forEach(([path, content]) => {
        sandpackFilesBlock[path] = { code: content as string };
      });

      const structuredTree = buildTreeFromPaths(paths);
      
      setVirtualFiles(sandpackFilesBlock);
      setFileTree(structuredTree);
      setActiveFile(findFirstFilePath(structuredTree));

      setCurrentStep("WORKSPACE");
      logToTerminal(`✅ Success. Mounted repository source entities securely into runtime workspace.`);
    } catch (err) {
      console.error(err);
      logToTerminal(`❌ Mount Exception: Failed to pull dataset records from target database.`);
      alert(`Mount Exception: Could not pull records for ID ${repoId}.`);
      setCurrentStep("UPLOAD");
    }
  };

  // STANDARD ZIP UPLOAD CONTROLLER
  const handleZipUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setCurrentStep("INDEXING");
    setProjectName(file.name.replace(".zip", ""));
    logToTerminal(`Uploading compressed file archive payload: ${file.name}...`);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const uploadResponse = await fetch("http://localhost:8080/repositories/upload", {
        method: "POST",
        body: formData,
      });

      if (!uploadResponse.ok) throw new Error("Upload processing aborted by Spring gateway");
      
      const repoData = await uploadResponse.json();
      const repoId = repoData.id; 
      setTargetRepoId(repoId);
      logToTerminal(`Spring framework pipeline processed upload. Assigned Repository Database ID: ${repoId}`);

      const filesResponse = await fetch(`http://localhost:8080/repositories/${repoId}/files`);
      if (!filesResponse.ok) throw new Error("Failed to fetch repository files structure map");
      
      const incomingFilesMap = await filesResponse.json();
      const paths = Object.keys(incomingFilesMap);

      const sandpackFilesBlock: Record<string, { code: string }> = {};
      Object.entries(incomingFilesMap).forEach(([path, content]) => {
        sandpackFilesBlock[path] = { code: content as string };
      });

      const structuredTree = buildTreeFromPaths(paths);
      
      setVirtualFiles(sandpackFilesBlock);
      setFileTree(structuredTree);
      setActiveFile(findFirstFilePath(structuredTree));

      setCurrentStep("WORKSPACE");
      logToTerminal(`✅ Ingestion Complete. Privacy-isolated project folders compiled into Sandpack workspace.`);
    } catch (error) {
      console.error(error);
      logToTerminal(`❌ System processing anomaly detected during stream chunking upload routines.`);
      alert("Error building dynamic tree structure. Please verify Spring Boot configuration.");
      setCurrentStep("UPLOAD");
    }
  };

  // GEMINI GENERATIVE ASSISTANT ROUTING
  const handleAskARC = async () => {
    if (!query.trim()) return;
    
    setChatHistory((prev) => [...prev, { role: "user", text: query }]);
    const currentQuery = query;
    setQuery("");
    logToTerminal(`Dispatching query to Gemini core context model mapping array...`);

    try {
      const response = await fetch(`http://localhost:8080/repositories/${targetRepoId}/gemini/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: currentQuery }),
      });

      if (!response.ok) throw new Error("Generative RAG parsing processing failed");
      const data = await response.json();
      
      setChatHistory((prev) => [
        ...prev, 
        { role: "assistant", text: data.answer || "No response generated from backend." }
      ]);
      logToTerminal(`Response generated successfully from Gemini generative framework models.`);
    } catch (error) {
      setChatHistory((prev) => [
        ...prev, 
        { role: "assistant", text: "❌ Connection error with Spring Boot service. Ensure your Java app server is running on port 8080." }
      ]);
      logToTerminal(`❌ Connection failure: Could not link up data frames on designated port.`);
    }
  };

  const renderTreeNodes = (nodes: Record<string, TreeNode>, currentPathId = "") => {
    return Object.entries(nodes)
      .sort(([keyA, nodeA], [keyB, nodeB]) => {
        if (nodeA.type !== nodeB.type) return nodeA.type === "folder" ? -1 : 1;
        return keyA.localeCompare(keyB);
      })
      .map(([key, node]) => {
        const nodePathId = currentPathId ? `${currentPathId}/${key}` : key;

        if (node.type === "folder") {
          const isExpanded = !!expandedFolders[nodePathId];
          return (
            <div key={nodePathId} className="w-full flex flex-col">
              <button
                onClick={() => toggleFolder(nodePathId)}
                className="w-full flex items-center gap-1.5 px-2 py-1 rounded hover:bg-zinc-800/40 text-zinc-400 hover:text-zinc-200 text-sm font-medium transition-colors duration-150"
              >
                <span className="text-zinc-500 flex-shrink-0">
                  {isExpanded ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
                </span>
                <span className="text-indigo-400 flex-shrink-0">
                  {isExpanded ? <FolderOpen size={14} /> : <Folder size={14} />}
                </span>
                <span className="truncate">{node.name}</span>
              </button>
              {isExpanded && (
                <div className="pl-3 border-l border-zinc-800/60 ml-3 mt-0.5 flex flex-col gap-0.5">
                  {renderTreeNodes(node.children, nodePathId)}
                </div>
              )}
            </div>
          );
        }

        const isFileActive = activeFile === node.path;
        return (
          <button
            key={node.path}
            onClick={() => {
              setActiveFile(node.path);
              logToTerminal(`Mounted context tab file viewer focus to: ${node.path}`);
            }}
            className={`w-full flex items-center gap-2 px-2 py-1 rounded text-sm font-medium transition-all duration-150 text-left ${
              isFileActive
                ? "bg-indigo-600/15 text-indigo-400 border border-indigo-500/30 shadow-sm"
                : "text-zinc-400 hover:bg-zinc-800/50 hover:text-zinc-200 border border-transparent"
            }`}
          >
            <FileCode size={14} className={isFileActive ? "text-indigo-400 flex-shrink-0" : "text-zinc-500 flex-shrink-0"} />
            <span className="truncate flex-1">{node.name}</span>
          </button>
        );
      });
  };

  return (
    <div className="h-screen w-screen bg-zinc-950 text-zinc-100 flex flex-col font-sans overflow-hidden">
      
      {/* HUD Bar Header */}
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
            <span>Subject: {projectName}</span>
          </div>
        </div>
      </header>

      {/* Main Container Content */}
      <div className="flex-1 flex overflow-hidden relative">

        {/* STEP A: INGESTION SCREEN */}
        {currentStep === "UPLOAD" && (
          <div className="absolute inset-0 flex flex-col items-center justify-center bg-zinc-950 z-20 px-4 gap-4">
            <div className="max-w-md w-full bg-zinc-900 border border-zinc-800 rounded-2xl p-8 shadow-2xl text-center space-y-6">
              <div className="w-16 h-16 bg-indigo-600/10 border border-indigo-500/20 text-indigo-400 rounded-full flex items-center justify-center mx-auto shadow-inner">
                <UploadCloud size={28} />
              </div>
              <div className="space-y-1">
                <h2 className="text-lg font-semibold text-zinc-100">Index Source Repository</h2>
                <p className="text-sm text-zinc-500">Provide a compressed ZIP file of your codebase to generate structured folder trees</p>
              </div>
              <label className="block w-full border border-dashed border-zinc-700 hover:border-indigo-500/80 bg-zinc-950/50 hover:bg-zinc-900/40 rounded-xl p-6 transition-all duration-150 cursor-pointer group">
                <input type="file" accept=".zip" onChange={handleZipUpload} className="hidden" />
                <span className="text-sm font-medium text-zinc-400 group-hover:text-indigo-400 block mb-1">Select code archive folder (.zip)</span>
                <span className="text-xs text-zinc-600 block">Streams live to Spring Boot Controller on Port 8080</span>
              </label>

              <div className="pt-4 border-t border-zinc-800/80 flex flex-col gap-2">
                <div className="text-xs font-medium text-zinc-500 text-left px-1">Testing bypass (Mount database record directly):</div>
                <div className="flex items-center gap-2 bg-zinc-950 rounded-xl p-1.5 border border-zinc-800 focus-within:border-indigo-500/60 transition-all duration-200">
                  <input
                    type="number"
                    placeholder="Enter Repo ID (e.g. 31)"
                    value={testRepoInput}
                    onChange={(e) => setTestRepoInput(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && mountRepositoryById(testRepoInput)}
                    className="bg-transparent flex-1 outline-none text-xs text-zinc-100 placeholder-zinc-700 px-2"
                  />
                  <button 
                    onClick={() => mountRepositoryById(testRepoInput)}
                    className="flex items-center gap-1 px-3 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold transition-colors"
                  >
                    <Play size={10} fill="currentColor" /> Mount
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* STEP B: LOADING SCREEN */}
        {currentStep === "INDEXING" && (
          <div className="absolute inset-0 flex flex-col items-center justify-center bg-zinc-950 z-20 px-4">
            <div className="space-y-4 text-center max-w-sm">
              <Loader2 size={36} className="text-indigo-500 animate-spin mx-auto" />
              <div className="space-y-1.5">
                <h3 className="text-base font-medium text-zinc-200 tracking-wide">Analyzing Test Subject...</h3>
                <p className="text-xs text-zinc-500 leading-relaxed">
                  Extracting source trees, compiling nested structural parameters layouts, and mapping dynamic code configurations...
                </p>
              </div>
            </div>
          </div>
        )}

        {/* STEP C: WORKSPACE CORE STUDIO */}
        {currentStep === "WORKSPACE" && (
          <>
            <div className="flex-1 h-full flex flex-col overflow-hidden">
              
              <div className="flex-1 flex overflow-hidden p-4 pb-2">
                <SandpackProvider             
                  customSetup={{ entry: activeFile }}
                  theme="dark"
                  files={virtualFiles}
                  options={{ 
                    visibleFiles: [activeFile],
                    activeFile: activeFile
                  }}
                  style={{ height: "100%", display: "flex", flexDirection: "row", width: "100%" }}
                >
                  <SandpackLayout 
                    className="flex-1 rounded-xl border border-zinc-800 overflow-hidden shadow-2xl flex"
                    style={{ height: "100%", minHeight: "100%" }}
                  >
                    {/* PRIVACY FILTERED PROJECT WORKSPACE TREE */}
                    <div 
                      className="border-r border-zinc-800 h-full p-3 flex flex-col gap-1 select-none flex-shrink-0 overflow-y-auto font-sans"
                      style={{ backgroundColor: "#151515", width: `${sidebarWidth}px` }}
                    >
                      <div className="flex items-center justify-between border-b border-zinc-800/80 pb-2 mb-2 px-1">
                        <div className="text-[11px] font-bold text-zinc-500 uppercase tracking-wider flex items-center gap-1.5 min-w-0">
                          <Terminal size={10} className="flex-shrink-0" /> <span className="truncate">Workspace</span>
                        </div>
                        <div className="flex items-center gap-1 bg-zinc-950 border border-zinc-800 px-1 py-0.5 rounded-md w-20 flex-shrink-0">
                          <input
                            type="text"
                            placeholder="ID..."
                            value={testRepoInput}
                            onChange={(e) => setTestRepoInput(e.target.value)}
                            onKeyDown={(e) => e.key === "Enter" && mountRepositoryById(testRepoInput)}
                            className="bg-transparent w-full outline-none text-[10px] text-zinc-300 font-medium placeholder-zinc-700 text-center"
                          />
                        </div>
                      </div>

                      <div className="flex flex-col gap-0.5 overflow-x-hidden">
                        {renderTreeNodes(fileTree)}
                      </div>
                    </div>

                    {/* DRAG WIDTH HANDLE DIVIDER */}
                    <div 
                      onMouseDown={startResizing}
                      className="w-1.5 h-full bg-zinc-950 hover:bg-indigo-500/80 cursor-col-resize flex-shrink-0 transition-colors duration-150 border-r border-zinc-800/40 z-20"
                      title="Drag to resize panel bounds"
                    />

                    {/* TEXT DISPLAY CODE CANVAS */}
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

              {/* DRAW LOGS TERMINAL PANEL */}
              <div className="px-4 pb-4 flex-shrink-0 flex flex-col z-10">
                <div className="bg-zinc-900 border border-zinc-800 rounded-xl overflow-hidden flex flex-col transition-all duration-300 shadow-xl">
                  <div className="h-9 bg-zinc-950 border-b border-zinc-800 px-4 flex items-center justify-between select-none">
                    <div className="flex items-center gap-2 text-xs font-semibold text-zinc-400 tracking-wide">
                      <TerminalSquare size={13} className="text-indigo-400" />
                      <span>Console Execution Outputs</span>
                    </div>
                    <div className="flex items-center gap-3">
                      <button 
                        onClick={() => setTerminalLogs([])} 
                        className="text-zinc-500 hover:text-zinc-300 transition-colors p-1"
                        title="Clear Console Shell Logs"
                      >
                        <Trash2 size={13} />
                      </button>
                      <button 
                        onClick={() => setIsTerminalExpanded(!isTerminalExpanded)} 
                        className="text-zinc-500 hover:text-zinc-300 transition-colors p-1"
                      >
                        {isTerminalExpanded ? <Minimize2 size={13} /> : <Maximize2 size={13} />}
                      </button>
                    </div>
                  </div>

                  {isTerminalExpanded && (
                    <div className="h-36 overflow-y-auto p-3 font-mono text-[11px] leading-relaxed text-zinc-400 space-y-1 bg-zinc-950/20 select-text selection:bg-indigo-500/30 scrollbar-thin scrollbar-thumb-zinc-800">
                      {terminalLogs.map((log, index) => (
                        <div key={index} className="whitespace-pre-wrap select-text truncate">
                          <span className="text-zinc-600 mr-2">&gt;&gt;</span>
                          {log}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>

            </div>

            {/* COGNITIVE RETRIEVAL ASSISTANT */}
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
                    className={`p-3.5 rounded-xl text-sm leading-relaxed max-w-[88%] shadow-sm overflow-hidden ${
                      msg.role === "user"
                        ? "bg-indigo-600 text-white ml-auto rounded-tr-none whitespace-pre-wrap break-words"
                        : "bg-zinc-800 text-zinc-200 border border-zinc-700/60 rounded-tl-none whitespace-pre-wrap break-words"
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
                  <button onClick={handleAskARC} className="p-2 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white transition-all duration-200 hover:scale-105">
                    <Send size={14} />
                  </button>
                </div>
              </div>
            </aside>
          </>
        )}

      </div>
    </div>
  );
}