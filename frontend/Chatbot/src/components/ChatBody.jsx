import styled, { keyframes } from "styled-components";
import Message from "./Message";

const ChatBody = ({ messages, loading }) => {
  return (
    <BodyContainer>
      {messages.map((msg) => (
        <Message key={msg.id} sender={msg.sender} text={msg.text} />
      ))}

      {loading && (
        <TypingBubble>
          <Dot delay="0s" />
          <Dot delay="0.2s" />
          <Dot delay="0.4s" />
        </TypingBubble>
      )}
    </BodyContainer>
  );
};

export default ChatBody;

const BodyContainer = styled.div`
  background-color: transparent;
  height: calc(100% - 132px);
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 15px;
  overflow-y: auto;
  flex: 8;
`;

const bounce = keyframes`
  0%, 60%, 100% {
    transform: translateY(0);
    opacity: 0.4;
  }
  30% {
    transform: translateY(-6px);
    opacity: 1;
  }
`;

const TypingBubble = styled.div`
  align-self: flex-start;
  background-color: rgba(255, 255, 255, 0.12);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  padding: 10px 14px;
  border-radius: 14px;
  display: flex;
  gap: 5px;
`;

const Dot = styled.div`
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: white;
  animation: ${bounce} 1.2s infinite ease-in-out;
  animation-delay: ${(props) => props.delay};
`;
