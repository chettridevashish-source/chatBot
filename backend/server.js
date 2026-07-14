import { spawn } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

import app from "./src/app.js";
import config from "./src/configs/config.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ragDirectory = path.resolve(__dirname, "../rag");
let ragProcess;

if (config.autoStartRag) {
    console.log("Starting the local RAG service...");
    ragProcess = spawn("uv", ["run", "python", "main.py"], {
        cwd: ragDirectory,
        stdio: "inherit",
    });

    ragProcess.on("error", (error) => {
        console.error(`Could not start the RAG service: ${error.message}`);
        console.error("Start it manually with: cd rag && uv run python main.py");
    });
}

const server = app.listen(config.port, () => {
    console.log(`Backend listening on http://localhost:${config.port}`);
    console.log("Frontend endpoint: POST /api/chat");
});

function shutdown() {
    server.close();
    ragProcess?.kill("SIGTERM");
}

process.once("SIGINT", shutdown);
process.once("SIGTERM", shutdown);
