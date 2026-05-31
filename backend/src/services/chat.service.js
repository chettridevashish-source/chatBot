import fs from "fs";
import path from "path";
import { GoogleGenAI } from "@google/genai";
import config from "../configs/config.js";

const ai = new GoogleGenAI({ apikey: config.GEMINI_API_KEY });

// Resolve path to your sso_data.json file
const dataPath = path.resolve("src/data/sso_data.json");
const ssoData = JSON.parse(fs.readFileSync(dataPath, "utf-8"));

export const processUserQuery = async (userMessage) => {
  try {
   //the response is injected in this ai model
    const response = await ai.models.generateContent({
      model: "gemini-2.5-flash",
      contents: userMessage,
      config: {
        systemInstruction: `
          You are the official AI Chatbot Assistant for the Sikkim Single Sign-On (SSO) portal.
          Your task is to answer citizen queries politely and accurately using ONLY the provided JSON context below.
          
          Guidelines:
          - If the user asks about document requirements, look into the relevant service and list them as clean bullet points.
          - If they ask about steps/how to apply, break it down using numbered steps.
          - If they ask about fees, reference the exact amounts.
          - If a query cannot be answered using this JSON data, politely tell the user that you are only trained to help with the available SSO services.
          
          Sikkim SSO Data Context:
          ${JSON.stringify(ssoData, null, 2)}
        `,
      },
    });

    return response.text;
  } catch (error) {
    console.error("Error in Chat Service:", error);
    throw new Error("Failed to process your request with the AI engine.");
  }
};