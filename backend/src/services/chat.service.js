import axios from "axios";
import config from "../configs/config.js";

export const processUserQueryStream = async (message, res) => {
    try {
        const response = await axios.post(
            `${config.ragApiUrl}/chat`,
            { question: message },
            { responseType: 'stream', timeout: 45_000 },
        );
        
        // Pipe the stream directly to the Express response
        response.data.pipe(res);
        
        // Handle stream errors
        response.data.on("error", (err) => {
            console.error("Stream error from Python backend:", err.message);
            if (!res.headersSent) {
                res.status(500).json({ error: "Stream error occurred" });
            } else {
                res.end();
            }
        });

    } catch (error) {
        console.error("Error communicating with Python RAG service:", error.message);
        if (!res.headersSent) {
            if (error.code === 'ECONNREFUSED') {
                return res.status(503).json({ error: "AI engine is offline. Start the RAG server on port 8000." });
            }
            if (error.code === "ECONNABORTED") {
                return res.status(504).json({ error: "The AI engine took too long to respond. Please try again." });
            }
            if (error.response?.status === 503) {
                return res.status(503).json({ error: "AI engine is still starting. Please try again shortly." });
            }
            if (error.response?.status === 422) {
                return res.status(400).json({ error: "The chat request was not accepted by the AI engine." });
            }
            return res.status(502).json({ error: "Failed to process chat query." });
        } else {
            res.end();
        }
    }
};
