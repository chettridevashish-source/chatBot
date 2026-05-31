import express from "express";
import chatRouter from "./routes/chat.routes.js"
import cors from "cors"

const app = express();

app.use(cors());
app.use(express.json());

app.use("/chat",chatRouter);

export default app;