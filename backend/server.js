import express from "express";
import cors from "cors";
import axios from "axios";
import { spawn } from "child_process";
import path from "path";
import { fileURLToPath } from "url";

const app = express();
const PORT = 3000;

// Setup paths to find the 'rag' directory from 'backend'
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ragDirectory = path.resolve(__dirname, '../rag');

app.use(cors({ origin: "*" }));
app.use(express.json());

// --- AUTOMATIC PYTHON STARTUP ---
console.log("Initializing Python RAG Engine...");

const pythonProcess = spawn("uv", ["run", "main.py"], {
    cwd: ragDirectory,
    shell: true
});

pythonProcess.stdout.on("data", (data) => console.log(`[PYTHON]: ${data}`));
pythonProcess.stderr.on("data", (data) => console.error(`[PYTHON ERROR]: ${data}`));

// Ensure Python dies when Node dies
process.on("SIGINT", () => {
    console.log("\nShutting down...");
    pythonProcess.kill();
    process.exit();
});

// --- API ROUTE ---
app.post("/api/chat", async (req, res) => {
    try {
        const { message } = req.body;
        const response = await axios.post("http://127.0.0.1:8000/chat", { question: message });
        res.json({ reply: response.data.answer });
    } catch (error) {
        res.status(500).json({ error: "AI Engine not ready." });
    }
});

app.listen(PORT, () => {
    console.log(`✅ Backend and AI Engine started on http://localhost:${PORT}`);
});