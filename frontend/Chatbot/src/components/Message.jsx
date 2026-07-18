import styled, { keyframes } from "styled-components";
import ReactMarkdown from "react-markdown";

const Message = ({ text, sender }) => {
  return (
    <Bubble className={sender}>
      {sender === "bot" ? (
        <ReactMarkdown
          components={{
            a: ({ node, ...props }) => <a target="_blank" rel="noopener noreferrer" style={{ color: "#82b1ff", textDecoration: "underline" }} {...props} />,
            p: ({ node, ...props }) => <p style={{ margin: "0 0 10px 0" }} {...props} />,
            ul: ({ node, ...props }) => <ul style={{ paddingLeft: "20px", margin: "0 0 10px 0" }} {...props} />,
            ol: ({ node, ...props }) => <ol style={{ paddingLeft: "20px", margin: "0 0 10px 0" }} {...props} />,
            li: ({ node, ...props }) => <li style={{ marginBottom: "5px" }} {...props} />,
            strong: ({ node, ...props }) => <strong style={{ color: "#ffffff", fontWeight: "bold" }} {...props} />
          }}
        >
          {text}
        </ReactMarkdown>
      ) : (
        text
      )}
    </Bubble>
  );
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

  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);

  animation: ${fadeInUp} 0.25s ease-out;

  &.user {
    align-self: flex-end;
    background-color: rgba(240, 195, 120, 0.28);
    border: 1px solid rgba(240, 195, 120, 0.4);
    white-space: pre-wrap;
  }

  &.bot {
    align-self: flex-start;
    background-color: rgba(100, 150, 190, 0.22);
    border: 1px solid rgba(100, 150, 190, 0.35);
  }
`;
