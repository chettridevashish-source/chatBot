import axios from "axios";

export const processUserQuery = async (message, session) => {
    try {
        // Your Python FastAPI server must be running on port 8000
        const pythonServiceUrl = 'http://127.0.0.1:8000/chat';

        // Python expects { "question": "..." } based on our FastAPI schemas
        const payload = {
            question: message
        };

        const response = await axios.post(pythonServiceUrl, payload);

        // Python returns { "answer": "..." }, we extract 'answer' and return it as 'aiReply'
        return response.data.answer;
        
    } catch (error) {
        console.error("❌ Error communicating with Python RAG service:", error.message);
        
        // Check if Python server is down
        if (error.code === 'ECONNREFUSED') {
            throw new Error("AI engine is currently offline. Please ensure Python backend is running.");
        }

        throw new Error("Failed to process chat query.");
    }
};