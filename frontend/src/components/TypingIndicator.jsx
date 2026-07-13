export default function TypingIndicator() {
  return (
    <div
      style={{
        display: "flex",
        gap: 5,
        width: "fit-content",
        background: "#fff",
        border: "1px solid #e5e7eb",
        padding: "12px 15px",
        borderRadius: 18,
      }}
    >
      {[1, 2, 3].map((i) => (
        <span
          key={i}
          style={{
            width: 7,
            height: 7,
            background: "#999",
            borderRadius: "50%",
            animation: "typing 1.2s infinite",
            animationDelay: `${i * 0.15}s`,
          }}
        />
      ))}

      <style>
        {`
          @keyframes typing {
            0%,60%,100%{
              transform:translateY(0);
            }

            30%{
              transform:translateY(-5px);
            }
          }
        `}
      </style>
    </div>
  );
}
