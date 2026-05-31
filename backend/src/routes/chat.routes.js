import { Router } from "express";
import { handleChatQuery } from "../controllers/chat.controller.js"

const router = Router();

router.post("/",handleChatQuery);

export default router;