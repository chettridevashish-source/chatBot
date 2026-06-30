import express from "express";
import cors from "cors";
import chatRoutes from "./routes/chat.routes.js";

const app = express();

// Middleware
app.use(cors());
app.use(express.json()); // Parses incoming JSON requests

// Mount Routes
// Frontend will call: POST http://localhost:5000/api/chat
app.use("/api/chat", chatRoutes);

export default app;