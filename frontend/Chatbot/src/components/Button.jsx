import styled from "styled-components";

const Button = ({ text, color, icon }) => {
  return (
    <button>
      {icon}
      {text}
    </button>
  );
};

export default Button;
