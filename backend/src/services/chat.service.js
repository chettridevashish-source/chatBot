import fs from "fs";
import path from "path";
import Groq from "groq-sdk";
import { GoogleGenAI } from "@google/genai";

import config from "../configs/config.js";
import { systemPrompt } from "../prompts/systemPrompt.js";

const groq = new Groq({
  apiKey: config.GROQ_API_KEY,
});

const gemini = new GoogleGenAI({
  apiKey: config.GEMINI_API_KEY,
});

const dataPath = path.resolve("src/data/sso_data.json");
const ssoData = JSON.parse(
  fs.readFileSync(dataPath, "utf-8")
);

export const processUserQuery = async (
  userMessage,
  session
) => {
  try {

    if (!session.chatHistory) {
      session.chatHistory = [];
    }

    session.chatHistory.push({
      role: "user",
      text: userMessage,
    });

    const recentHistory =
      session.chatHistory.slice(-10);

    const conversationContext =
      recentHistory
        .map(
          (msg) =>
            `${msg.role}: ${msg.text}`
        )
        .join("\n");

    const systemInstruction = `
${systemPrompt}

SSO DATA:
${JSON.stringify(ssoData, null, 2)}
`;

    let aiReply;

    try {

      console.log(
        "Using Groq..."
      );

      const groqResponse =
        await groq.chat.completions.create({
          model: "llama-3.1-8b-instant",
          messages: [
            {
              role: "system",
              content:
                systemInstruction,
            },
            {
              role: "user",
              content:
                conversationContext,
            },
          ],
        });

      aiReply =
        groqResponse.choices[0]
          .message.content;

    } catch (groqError) {

      console.log(
        "Groq failed. Switching to Gemini..."
      );

      const geminiResponse =
        await gemini.models.generateContent({
          model: "gemini-2.5-flash",
          contents:
            conversationContext,
          config: {
            systemInstruction,
          },
        });

      aiReply =
        geminiResponse.text;
    }

    session.chatHistory.push({
      role: "assistant",
      text: aiReply,
    });

    if (
      session.chatHistory.length >
      20
    ) {
      session.chatHistory =
        session.chatHistory.slice(
          -20
        );
    }

    return aiReply;

  } catch (error) {

    console.error(
      "Error in Chat Service:",
      error
    );

    throw new Error(
      "Failed to process your request with the AI engine."
    );
  }
};