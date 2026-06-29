import express from "express";
import cors from "cors";
import axios from "axios";
import { spawn } from "child_process";
import path from "path";
import { fileURLToPath } from "url";

const app = express();
const PORT = 3000; 

// Setup paths
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ragDirectory = path.resolve(__dirname, '../rag');

app.use(cors({ origin: "*" }));
app.use(express.json());

// --- AUTOMATIC PYTHON STARTUP ---
console.log("Initializing Python RAG Engine & Background Scheduler...");

// 1. Start the FastAPI RAG Engine (Online Chat)
const pythonProcess = spawn("uv", ["run", "main.py"], {
    cwd: ragDirectory,
    shell: true
});

pythonProcess.stdout.on("data", (data) => console.log(`[RAG API]: ${data.toString().trim()}`));
pythonProcess.stderr.on("data", (data) => console.error(`[RAG API ERROR]: ${data.toString().trim()}`));

// 2. Start the Background Scheduler (Offline PDF Sync)
const schedulerProcess = spawn("uv", ["run", "scheduler.py"], {
    cwd: ragDirectory,
    shell: true
});

schedulerProcess.stdout.on("data", (data) => console.log(`[SCHEDULER]: ${data.toString().trim()}`));
schedulerProcess.stderr.on("data", (data) => console.error(`[SCHEDULER ERROR]: ${data.toString().trim()}`));

// Cleanup on exit
process.on("SIGINT", () => {
    console.log("\nShutting down backend and all Python processes...");
    pythonProcess.kill();
    schedulerProcess.kill();
    process.exit();
});

// --- API ROUTE ---
app.post("/api/chat", async (req, res) => {
    const { message } = req.body;
    if (!message) return res.status(400).json({ error: "Message field is required." });

    try {
        // Forwarding request to FastAPI on port 8000
        const response = await axios.post("http://127.0.0.1:8000/chat", { 
            question: message 
        });
        res.json({ reply: response.data.answer });
    } catch (error) {
        console.error("[Backend Error]: Python AI Engine Error:", error.message);
        res.status(500).json({ error: "The AI engine is currently starting or offline." });
    }
});

app.listen(PORT, () => {
    console.log(`Backend and AI Engine started on http://localhost:${PORT}`);
    console.log(`Waiting for frontend requests...`);
});