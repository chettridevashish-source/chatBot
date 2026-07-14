import express from "express";
import cors from "cors";
import chatRoutes from "./routes/chat.routes.js";
import config from "./configs/config.js";

const app = express();

// Accept both URL forms used by VS Code Live Server: localhost and 127.0.0.1.
app.use(cors({
    origin: config.clientOrigins,
    methods: ["GET", "POST", "OPTIONS"],
    allowedHeaders: ["Content-Type"],
}));
app.use(express.json({ limit: "16kb" }));
app.get("/health", (_req, res) => {
    res.status(200).json({ status: "ok" });
});

// Frontend calls POST http://<current-host>:3000/api/chat
app.use("/api/chat", chatRoutes);

// Keep invalid JSON from becoming Express's default HTML error page. The
// frontend (and other API consumers) can consistently handle JSON errors.
app.use((error, _req, res, next) => {
    if (error instanceof SyntaxError && "body" in error) {
        return res.status(400).json({ error: "Request body must be valid JSON" });
    }
    return next(error);
});

export default app;
