import { useState, useEffect, useRef } from "react";
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
import TypingIndicator from "./TypingIndicator.jsx";

export default function ChatWindow() {
  const dispatch = useDispatch();

  const { messages, isLoading } = useSelector((state) => state.chat);

  const [input, setInput] = useState("");

  const messagesEndRef = useRef(null);

  const [askBot] = useLazyQuery(ASK_BOT, {
    onCompleted: (data) => {
      dispatch(matchReceived(data.askBot));
    },
    onError: () => {
      dispatch(responseFailed());
    },
  });

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, isLoading]);

  function handleSend() {
    if (!input.trim()) return;

    dispatch(messageSent(input));

    askBot({
      variables: {
        question: input,
      },
    });

    setInput("");
  }

  return (
    <div
      style={{
        width: "100%",
        maxWidth: 650,
        height: "85vh",
        margin: "40px auto",
        display: "flex",
        flexDirection: "column",
        background: "#f9fafb",
        border: "1px solid #e5e7eb",
        borderRadius: 20,
        overflow: "hidden",
        boxShadow: "0 20px 40px rgba(0,0,0,0.08)",
        fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
      }}
    >
      {/* Header */}
      <div
        style={{
          padding: "18px 22px",
          background: "#ffffff",
          borderBottom: "1px solid #eeeeee",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 14,
          }}
        >
          <img
            src="https://www.galaxyplastics.com/wp-content/uploads/2024/10/Galaxy-Plastics-logo-horizontal.png"
            alt="Galaxy Plastics"
            style={{
              width: 110,
              height: "auto",
              objectFit: "contain",
            }}
          />

          <div>
            <div
              style={{
                fontSize: 18,
                fontWeight: 600,
                color: "#111",
              }}
            >
              GP AI Product Assistant
            </div>

            <div
              style={{
                fontSize: 13,
                color: "#888",
                marginTop: 3,
              }}
            >
              Find the right product quickly
            </div>
          </div>
        </div>

        <button
          onClick={() => dispatch(sessionCleared())}
          style={{
            border: "none",
            background: "#f3f4f6",
            color: "#555",
            padding: "7px 14px",
            borderRadius: 20,
            fontSize: 12,
            cursor: "pointer",
          }}
        >
          Clear
        </button>
      </div>

      {/* Chat Area */}
      <div
        style={{
          flex: 1,
          overflowY: "auto",
          padding: 24,
          background: "#f6f7fb",
        }}
      >
        {messages.length === 0 && !isLoading && (
          <div
            style={{
              textAlign: "center",
              marginTop: 120,
              color: "#8a8f98",
              fontSize: 14,
              lineHeight: 1.6,
            }}
          >
            Tell me what you need.
            <br />
            Example:
            <br />
            "something to stop sewer backflow"
          </div>
        )}

        {messages.map((m) => (
          <Message key={m.id} role={m.role} text={m.text} match={m.match} />
        ))}

        {isLoading && <TypingIndicator />}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div
        style={{
          padding: 16,
          background: "#ffffff",
          borderTop: "1px solid #eeeeee",
        }}
      >
        <div
          style={{
            display: "flex",
            alignItems: "center",
            background: "#f3f4f6",
            borderRadius: 16,
            padding: "8px 10px 8px 15px",
          }}
        >
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
            placeholder="Describe what you need..."
            style={{
              flex: 1,
              border: "none",
              outline: "none",
              background: "transparent",
              fontSize: 15,
            }}
          />

          <button
            onClick={handleSend}
            disabled={isLoading}
            style={{
              background: "#111",
              color: "#fff",
              border: "none",
              borderRadius: 12,
              padding: "9px 18px",
              fontSize: 14,
              cursor: isLoading ? "default" : "pointer",
            }}
          >
            Send
          </button>
        </div>
      </div>
      <div
        style={{
          textAlign: "center",
          padding: "8px 0 12px",
          fontSize: 12,
          color: "#999",
          background: "#ffffff",
        }}
      >
        © {new Date().getFullYear()} Srinjay Mitra. All rights reserved.
      </div>
    </div>
  );
}
