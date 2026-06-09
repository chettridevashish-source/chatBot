import express from "express";
import chatRouter from "./routes/chat.routes.js";
import cors from "cors";
import session from "express-session";

const app = express();

app.use(
  cors({
    origin: "http://127.0.0.1:5501",
    credentials: true
  })
);

app.use(express.json());

app.use(
  session({
    secret: "sso-chatbot-secret",
    resave: false,
    saveUninitialized: true,
    cookie: {
      maxAge: 24 * 60 * 60 * 1000
    }
  })
);

app.use("/chat", chatRouter);

export default app;