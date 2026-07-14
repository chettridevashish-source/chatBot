import styled from "styled-components";
import { RiRobot2Fill } from "react-icons/ri";

const Widget = ({ toggle }) => {
  return (
    <WidgetContainer onClick={toggle}>
      <RiRobot2Fill />
    </WidgetContainer>
  );
};

export default Widget;

const WidgetContainer = styled.div`
  background: linear-gradient(135deg, #6b7b7a 0%, #7a7086 100%);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 26px;
  cursor: pointer;
  transition: transform 0.2s ease;

  &:hover {
    transform: scale(1.08);
  }
`;
