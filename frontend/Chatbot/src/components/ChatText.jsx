// import styled from "styled-components";
// import { IoSendSharp } from "react-icons/io5";
// import { useState, useRef, useEffect } from "react";

// const ChatText = ({ onSend, loading }) => {
//   const [value, setValue] = useState("");
//   const inputRef = useRef(null);

//   const handleSend = () => {
//     if (!value.trim() || loading) return;
//     onSend(value);
//     setValue("");
//   };

//   const handleKeyDown = (e) => {
//     if (e.key === "Enter") handleSend();
//   };

//   // Focus the input whenever the component mounts (chat container opens)
//   useEffect(() => {
//     inputRef.current?.focus();
//   }, []);

//   // Refocus the input once loading finishes (bot has replied)
//   useEffect(() => {
//     if (!loading) {
//       inputRef.current?.focus();
//     }
//   }, [loading]);

//   return (
//     <Text>
//       <Input
//         ref={inputRef}
//         value={value}
//         onChange={(e) => setValue(e.target.value)}
//         onKeyDown={handleKeyDown}
//         type="text"
//         placeholder="Enter your message here...."
//         disabled={loading}
//       />
//       {/* <IoSendSharp className="send" onClick={handleSend} /> */}
//       <SendButton onClick={handleSend}>
//         <IoSendSharp />
//       </SendButton>
//     </Text>
//   );
// };

// export default ChatText;

// const Text = styled.div`
//   display: flex;
//   align-items: center;
//   gap: 10px;
//   height: 70px;
//   padding: 0 14px;
//   backdrop-filter: blur(8px);
//   border-top: 1px solid rgba(255, 255, 255, 0.2);
// `;

// //   .send {
// //     border: 1px solid #dfd4d44f;
// //     box-shadow: 1px 1px 5px #dfd4d44f;
// //     background-color: #0056b3;
// //     padding: 10px;
// //     height: 35px;
// //     width: 60px;
// //     border-radius: 10px;
// //     color: white;
// //     cursor: pointer;
// //     &:hover {
// //       border: 0.5px solid white;
// //       box-shadow: 3px 3px 10px white;
// //     }
// //   }
// // `;
// const SendButton = styled.button`
//   width: 50px;
//   height: 50px;
//   border: 1px solid rgba(255, 255, 255, 0.3);
//   border-radius: 50%;
//   background-color: rgba(255, 255, 255, 0.2);
//   backdrop-filter: blur(8px);
//   color: white;
//   font-size: 20px;
//   display: flex;
//   justify-content: center;
//   align-items: center;
//   cursor: pointer;
//   transition:
//     background-color 0.2s ease,
//     transform 0.15s ease;

//   &:hover:not(:disabled) {
//     background-color: rgba(255, 255, 255, 0.35);
//     transform: scale(1.08);
//   }

//   &:active:not(:disabled) {
//     transform: scale(0.95);
//   }

//   &:disabled {
//     background-color: rgba(255, 255, 255, 0.08);
//     cursor: not-allowed;
//   }
// `;

// const Input = styled.input`
//   flex: 1;
//   height: 40px;
//   padding: 0 14px;
//   font-size: 14px;
//   border: 1px solid rgba(255, 255, 255, 0.3);
//   border-radius: 20px;
//   background-color: rgba(255, 255, 255, 0.15);
//   backdrop-filter: blur(8px);
//   -webkit-backdrop-filter: blur(8px);
//   color: white;

//   &::placeholder {
//     color: rgba(255, 255, 255, 0.65);
//   }

//   &:focus {
//     outline: none;
//     background-color: rgba(255, 255, 255, 0.22);
//     box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.35);
//   }

//   &:disabled {
//     opacity: 0.6;
//   }
// `;

import styled from "styled-components";
import { IoSendSharp } from "react-icons/io5";
import { useState, useRef, useEffect } from "react";

const ChatText = ({ onSend, loading }) => {
  const [value, setValue] = useState("");
  const inputRef = useRef(null);

  const handleSend = () => {
    if (!value.trim() || loading) return;
    onSend(value);
    setValue("");
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") handleSend();
  };

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  useEffect(() => {
    if (!loading) inputRef.current?.focus();
  }, [loading]);

  return (
    <Text>
      <Input
        ref={inputRef}
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={handleKeyDown}
        type="text"
        placeholder="Enter your message"
        disabled={loading}
      />
      <SendButton onClick={handleSend} disabled={!value.trim() || loading}>
        <IoSendSharp />
      </SendButton>
    </Text>
  );
};

export default ChatText;

const Text = styled.div`
  display: flex;
  align-items: center;
  gap: 10px;
  height: 72px;
  padding: 0 14px;
  background-color: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(10px);
  border-top: 1px solid rgba(255, 255, 255, 0.12);
`;

const Input = styled.input`
  flex: 1;
  height: 36px;
  padding: 0 14px;
  font-size: 14px;
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 20px;
  background-color: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  color: white;

  &::placeholder {
    color: rgba(255, 255, 255, 0.6);
  }

  &:focus {
    outline: none;
    background-color: rgba(255, 255, 255, 0.15);
    box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.2);
  }

  &:disabled {
    opacity: 0.6;
  }
`;

const SendButton = styled.button`
  width: 34px;
  height: 34px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  color: white;
  font-size: 15px;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  transition:
    background-color 0.2s ease,
    transform 0.15s ease;

  &:hover:not(:disabled) {
    background-color: rgb(24, 50, 163);
    transform: scale(1.08);
  }

  &:active:not(:disabled) {
    transform: scale(0.95);
  }

  &:disabled {
    background-color: rgba(255, 255, 255, 0.06);
    cursor: not-allowed;
  }
`;
