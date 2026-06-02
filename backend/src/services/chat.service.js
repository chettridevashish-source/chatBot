import fs from "fs";
import path from "path";
import { GoogleGenAI } from "@google/genai";
import config from "../configs/config.js";
import { systemPrompt } from "../prompts/systemPrompt.js";

const ai = new GoogleGenAI({ apikey: config.GEMINI_API_KEY });

// Resolve path to your sso_data.json file
const dataPath = path.resolve("src/data/sso_data.json");
const ssoData = JSON.parse(fs.readFileSync(dataPath, "utf-8"));

export const processUserQuery = async (userMessage) => {
  try {
    const response = await ai.models.generateContent({
      model: "gemini-2.5-flash",
      contents: userMessage,
      config: {
        //INSTRUCTION TO THE GEMINI LLM
        systemInstruction: `
          ${systemPrompt}
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