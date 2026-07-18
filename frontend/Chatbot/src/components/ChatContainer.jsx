import styled from "styled-components";
import ChatHeader from "./ChatHeader";
import ChatBody from "./ChatBody";
import ChatText from "./ChatText";
import { useState } from "react";

const chatApiUrl = import.meta.env.VITE_CHAT_API_URL || "/api/chat";

const ChatContainer = ({ toggle }) => {
  const [messages, setMessages] = useState([
    { id: 1, sender: "bot", text: "Hello, How may I help you." },
  ]);
  const [loading, setLoading] = useState(false);

  const addMessage = (text, sender) => {
    setMessages((prev) => [...prev, { id: Date.now(), sender, text }]);
  };

  const sendMessage = async (userMessage) => {
    addMessage(userMessage, "user");
    setLoading(true);
    
    // Add an empty bot message immediately
    const botMsgId = Date.now() + 1;
    setMessages((prev) => [...prev, { id: botMsgId, sender: "bot", text: "" }]);

    try {
      const response = await fetch(chatApiUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage }),
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      // Stop loading animation immediately as we start receiving data
      setLoading(false);

      const reader = response.body.getReader();
      const decoder = new TextDecoder("utf-8");
      
      let done = false;
      while (!done) {
        const { value, done: readerDone } = await reader.read();
        done = readerDone;
        if (value) {
          const chunk = decoder.decode(value, { stream: true });
          setMessages((prev) => 
            prev.map((msg) => 
              msg.id === botMsgId ? { ...msg, text: msg.text + chunk } : msg
            )
          );
        }
      }
    } catch (error) {
      console.error("Failed to get bot reply:", error);

      if (error instanceof TypeError) {
        setMessages((prev) => 
          prev.map((msg) => 
            msg.id === botMsgId ? { ...msg, text: "⚠️ Server is not connected yet. Please try again later." } : msg
          )
        );
      } else {
        setMessages((prev) => 
          prev.map((msg) => 
            msg.id === botMsgId ? { ...msg, text: "Sorry, something went wrong. Please try again." } : msg
          )
        );
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <ChatCont>
      <ChatHeader toggle={toggle} />
      <ChatBody messages={messages} loading={loading} />
      <ChatText onSend={sendMessage} loading={loading} />
    </ChatCont>
  );
};

export default ChatContainer;

// const ChatCont = styled.div`
//   height: 800px;
//   width: 1100px;
//   border: 1px solid #6b6a67;
//   border-radius: 16px;
//   background-color: #615b5b83;
//   overflow: hidden;
//   display: flex;
//   flex-direction: column;
// `;

const ChatCont = styled.div`
  height: 700px;
  width: 1100px;
  border-radius: 16px;
  overflow: hidden;
  display: flex;
  flex-direction: column;

  background: linear-gradient(135deg, #6b7b7a 0%, #7a7086 100%);
`;
