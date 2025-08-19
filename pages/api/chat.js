// pages/api/chat.js
import OpenAI from 'openai';
import { OpenAIStream, StreamingTextResponse } from 'ai';

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

export const runtime = 'edge';

export default async function POST(req) {
  const { messages } = await req.json();

  const response = await openai.chat.completions.create({
    model: 'gpt-4-turbo',
    stream: true,
    messages: [
        // This is a basic system prompt. We can enhance this based on the BRD's requirements.
        { role: 'system', content: 'You are a helpful and patient AI tutor for an IB school. You must guide students to the answer with Socratic questions rather than just giving the answer directly. Vary your level of scaffolding based on the student\'s apparent understanding.'}, 
        ...messages
    ],
  });

  const stream = OpenAIStream(response);
  return new StreamingTextResponse(stream);
}
