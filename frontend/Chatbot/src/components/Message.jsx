import styled from "styled-components";

const Message = ({ text, sender }) => {
  return <Bubble className={sender}>{text}</Bubble>;
};

export default Message;

const Bubble = styled.div`
  max-width: 78%;
  padding: 10px 14px;
  border-radius: 14px;
  color: rgba(255, 255, 255, 0.95);
  font-size: 14px;
  line-height: 1.4;
  word-wrap: break-word;
  white-space: pre-wrap;

  background-color: rgba(255, 255, 255, 0.12);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.15);

  &.user {
    align-self: flex-end;
    background-color: rgba(255, 255, 255, 0.18);
    color: white;
  }

  &.bot {
    align-self: flex-start;
  }
`;
