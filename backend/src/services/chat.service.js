import axios from "axios";
import config from "../configs/config.js";

export const processUserQuery = async (message) => {
    try {
        const response = await axios.post(
            `${config.ragApiUrl}/chat`,
            { question: message },
            { timeout: 45_000 },
        );
        if (typeof response.data?.answer !== "string" || !response.data.answer.trim()) {
            throw new Error("The AI engine returned an invalid response.");
        }
        return response.data.answer.trim();
    } catch (error) {
        console.error("Error communicating with Python RAG service:", error.message);
        if (error.code === 'ECONNREFUSED') {
            const serviceError = new Error("AI engine is offline. Start the RAG server on port 8000.");
            serviceError.statusCode = 503;
            throw serviceError;
        }
        if (error.code === "ECONNABORTED") {
            const serviceError = new Error("The AI engine took too long to respond. Please try again.");
            serviceError.statusCode = 504;
            throw serviceError;
        }
        if (error.response?.status === 503) {
            const serviceError = new Error("AI engine is still starting. Please try again shortly.");
            serviceError.statusCode = 503;
            throw serviceError;
        }
        if (error.response?.status === 422) {
            const serviceError = new Error("The chat request was not accepted by the AI engine.");
            serviceError.statusCode = 400;
            throw serviceError;
        }
        const serviceError = new Error("Failed to process chat query.");
        serviceError.statusCode = 502;
        throw serviceError;
    }
};
