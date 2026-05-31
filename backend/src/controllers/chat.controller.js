import { processUserQuery } from "../services/chat.service.js";

export const handleChatQuery = async(req,res)=>{
    const { message } = req.body;

    if(!message){
        return res.status(400).json({
            error: "Message field is required"
        })
    }
    try{
        const aiReply = await processUserQuery(message);
        return res.status(200).json({
            reply:aiReply
        })
    }
    catch( error)
    {
        return res.status(500).json({
            error:error.message
        });
    };
}