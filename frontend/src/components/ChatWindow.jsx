import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useLazyQuery } from "@apollo/client";
import { ASK_BOT } from "../apollo/client.js";
import {
  messageSent,
  matchReceived,
  responseFailed,
  sessionCleared,
} from "../redux/chatSlice.js";
import Message from "./Message.jsx";

export default function ChatWindow() {
  const dispatch = useDispatch();
  const { messages, isLoading } = useSelector((state) => state.chat);
  const [input, setInput] = useState("");

  const [askBot] = useLazyQuery(ASK_BOT, {
    onCompleted: (data) => dispatch(matchReceived(data.askBot)),
    onError: () => dispatch(responseFailed()),
  });

  function handleSend() {
    if (!input.trim()) return;
    dispatch(messageSent(input));
    askBot({ variables: { question: input } });
    setInput("");
  }

  return (
    <div
      style={{
        maxWidth: 520,
        margin: "60px auto",
        fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
        color: "#000",
        padding: "0 20px",
      }}
    >
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "baseline",
          marginBottom: 24,
        }}
      >
        <h1 style={{ fontSize: 20, fontWeight: 500, margin: 0 }}>
          Find a product
        </h1>
        <button
          onClick={() => dispatch(sessionCleared())}
          style={{
            fontSize: 12,
            background: "none",
            border: "none",
            color: "#999",
            cursor: "pointer",
            padding: 0,
          }}
        >
          Clear
        </button>
      </div>

      <div style={{ minHeight: 300, marginBottom: 20 }}>
        {messages.length === 0 && !isLoading && (
          <div style={{ fontSize: 14, color: "#999" }}>
            Describe what you need — e.g. "something to stop sewer backflow"
          </div>
        )}
        {messages.map((m) => (
          <Message key={m.id} role={m.role} text={m.text} match={m.match} />
        ))}
        {isLoading && (
          <div style={{ fontSize: 14, color: "#999", padding: "10px 0" }}>
            Finding a match…
          </div>
        )}
      </div>

      <div
        style={{
          display: "flex",
          borderBottom: "1px solid #000",
          paddingBottom: 8,
        }}
      >
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          placeholder="Describe what you need"
          style={{
            flex: 1,
            border: "none",
            outline: "none",
            fontSize: 15,
            fontFamily: "inherit",
            background: "transparent",
          }}
        />
        <button
          onClick={handleSend}
          disabled={isLoading}
          style={{
            border: "none",
            background: "none",
            fontSize: 14,
            cursor: isLoading ? "default" : "pointer",
            color: isLoading ? "#ccc" : "#000",
          }}
        >
          Send
        </button>
      </div>
    </div>
  );
}
