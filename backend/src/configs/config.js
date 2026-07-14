import dotenv from "dotenv";

dotenv.config();

const defaultClientOrigins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://localhost:5501",
    "http://127.0.0.1:5501",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
];

const configuredOrigins = process.env.CLIENT_ORIGINS || process.env.CLIENT_ORIGIN || "";
const additionalOrigins = configuredOrigins
    .split(",")
    .map((origin) => origin.trim())
    .filter(Boolean);

const configuredPort = Number.parseInt(process.env.PORT || "3000", 10);

const config = {
    // Do not let an invalid environment value make Express listen on NaN.
    port: Number.isInteger(configuredPort) && configuredPort > 0 && configuredPort < 65_536
        ? configuredPort
        : 3000,
    ragApiUrl: process.env.RAG_API_URL || "http://127.0.0.1:8000",
    clientOrigins: [...new Set([...defaultClientOrigins, ...additionalOrigins])],
    // Python is normally run as its own service. Opt in to child-process
    // startup so a backend restart cannot unexpectedly duplicate it.
    autoStartRag: process.env.AUTO_START_RAG === "true",
};

export default config;
