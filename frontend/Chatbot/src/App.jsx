import ChatContainer from "./components/ChatContainer";
import styled, { createGlobalStyle } from "styled-components";
import Widget from "./components/Widget";
import { useState } from "react";

function App() {
  const [seeCotainer, setSeeContainer] = useState(false);

  const ClickWidget = () => {
    setSeeContainer((prev) => !prev);
  };

  const AddMessage = () => {};

  return (
    <>
      <GlobalStyle />
      <Container>
        {seeCotainer && <ChatContainer toggle={ClickWidget} />}
        {!seeCotainer && <Widget toggle={ClickWidget} />}
      </Container>
    </>
  );
}

export default App;

const GlobalStyle = createGlobalStyle`
  html, body {
    margin: 0;
    padding: 0;
    height: 100%;
  }

  body {
    background-image: url("/images/sso_bg2.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed; 
  }
`;

const Container = styled.div`
  position: fixed;
  bottom: 100px;
  right: 24px;
  z-index: 9999;

  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 12px;
`;

// import ChatContainer from "./components/ChatContainer";
// import styled from "styled-components";

// const App = () => {
//   return (
//     <Container>
//       <div>
//         <ChatContainer />
//       </div>
//     </Container>
//   );
// };

// const Container = styled.div`
//   height: 100vh;
//   width: 100vw;
//   background-image: url("/images/sso_bg.jpg");
//   background-position: center;
//   background-size: cover;

//   display: flex;
//   justify-content: end;
//   align-items: end;
// `;

// export default App;
