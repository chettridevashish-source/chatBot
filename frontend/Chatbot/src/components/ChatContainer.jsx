import styled from "styled-components";
import ChatHeader from "./ChatHeader";
import ChatBody from "./ChatBody";
import ChatText from "./ChatText";
import { useState } from "react";

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

    try {
      const response = await fetch("http://localhost:3000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage }),
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const data = await response.json();
      addMessage(data.reply, "bot");
    } catch (error) {
      console.error("Failed to get bot reply:", error);

      if (error instanceof TypeError) {
        addMessage(
          "⚠️ Server is not connected yet. Please try again later.",
          "bot",
        );
      } else {
        addMessage("Sorry, something went wrong. Please try again.", "bot");
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
