import express from "express";
import { handleChatQuery } from "../controllers/chat.controller.js";

const router = express.Router();

// Define the chat route
router.post("/", handleChatQuery);

export default router;