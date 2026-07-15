import styled, { keyframes } from "styled-components";
import { useEffect, useRef } from "react";
import Message from "./Message";

const ChatBody = ({ messages, loading }) => {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  return (
    <BodyContainer>
      {messages.map((msg) => (
        <Message key={msg.id} sender={msg.sender} text={msg.text} />
      ))}

      {loading && (
        <TypingWrapper>
          <TypingBubble>
            <Dot delay="0s" />
            <Dot delay="0.2s" />
            <Dot delay="0.4s" />
          </TypingBubble>
          <TypingLabel>Typing...</TypingLabel>
        </TypingWrapper>
      )}

      <div ref={bottomRef} />
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

  /* Custom scrollbar — Chrome/Edge/Safari */
  &::-webkit-scrollbar {
    width: 6px;
  }

  &::-webkit-scrollbar-track {
    background: transparent;
  }

  &::-webkit-scrollbar-thumb {
    background-color: rgba(255, 255, 255, 0.25);
    border-radius: 10px;
  }

  &::-webkit-scrollbar-thumb:hover {
    background-color: rgba(255, 255, 255, 0.4);
  }

  /* Custom scrollbar — Firefox */
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 255, 255, 0.25) transparent;
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

const TypingWrapper = styled.div`
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 4px;
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

const TypingLabel = styled.span`
  font-size: 11px;
  color: rgba(255, 255, 255, 0.6);
  margin-left: 4px;
`;

const Dot = styled.div`
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: white;
  animation: ${bounce} 1.2s infinite ease-in-out;
  animation-delay: ${(props) => props.delay};
`;
