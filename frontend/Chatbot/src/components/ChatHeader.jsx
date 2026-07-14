import styled from "styled-components";
import { MdClose } from "react-icons/md";

const ChatHeader = ({ toggle }) => {
  return (
    <ChatHead>
      <h1>AI-Bot</h1>
      <CloseButton onClick={toggle}>
        <MdClose />
      </CloseButton>
    </ChatHead>
  );
};

export default ChatHeader;

const ChatHead = styled.div`
  height: 60px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.15);
  background-color: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(10px);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 14px;

  h1 {
    font-size: 17px;
    color: white;
    font-weight: 600;
    margin: 0;
  }
`;

const CloseButton = styled.button`
  width: 30px;
  height: 30px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  color: white;
  font-size: 16px;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  transition:
    background-color 0.2s ease,
    transform 0.15s ease;

  &:hover {
    background-color: rgb(182, 15, 15);
    transform: scale(1.08);
  }

  &:active {
    transform: scale(0.95);
  }
`;
