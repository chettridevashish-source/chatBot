import dotenv from "dotenv"

dotenv.config();

const config={
    GEMINI_API_KEY:process.env.GEMINI_API_KEY,
    OPENROUTER_API_KEY:process.env.OPENROUTER_API_KEY,
    GROQ_API_KEY:process.env.GROQ_API_KEY
}

export default config;