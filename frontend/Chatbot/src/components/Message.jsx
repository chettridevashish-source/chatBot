import styled, { keyframes } from "styled-components";

const Message = ({ text, sender }) => {
  return <Bubble className={sender}>{text}</Bubble>;
};

export default Message;

const fadeInUp = keyframes`
  from {
    opacity: 0;
    transform: translateY(8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
`;

const Bubble = styled.div`
  max-width: 78%;
  padding: 10px 14px;
  border-radius: 14px;
  color: white;
  font-size: 16px;
  line-height: 1.4;
  word-wrap: break-word;
  white-space: pre-wrap;

  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);

  animation: ${fadeInUp} 0.25s ease-out;

  &.user {
    align-self: flex-end;
    background-color: rgba(240, 195, 120, 0.28);
    border: 1px solid rgba(240, 195, 120, 0.4);
  }

  &.bot {
    align-self: flex-start;
    background-color: rgba(100, 150, 190, 0.22);
    border: 1px solid rgba(100, 150, 190, 0.35);
  }
`;
