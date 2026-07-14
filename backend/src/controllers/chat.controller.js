import { processUserQuery } from "../services/chat.service.js";

export const handleChatQuery = async (req, res) => {
    const { message } = req.body; // Frontend sends { "message": "..." }

    if (typeof message !== "string" || !message.trim()) {
        return res.status(400).json({
            error: "Message field is required"
        });
    }
    if (message.trim().length > 1000) {
        return res.status(400).json({ error: "Message must be 1000 characters or fewer" });
    }

    try {
        const aiReply = await processUserQuery(
            message.trim(),
        );

        return res.status(200).json({
            reply: aiReply // Sends back { "reply": "..." }
        });
    } catch (error) {
        return res.status(error.statusCode || 500).json({
            error: error.message
        });
    }
};
