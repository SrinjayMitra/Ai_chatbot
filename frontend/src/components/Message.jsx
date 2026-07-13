import ProductCard from "./ProductCard.jsx";

export default function Message({ role, text, match }) {
  const isUser = role === "user";

  if (!isUser && match) {
    return (
      <div
        style={{
          marginBottom: 18,
        }}
      >
        <ProductCard
          name={match.productName}
          url={match.productUrl}
          category={match.category}
          reason={match.reason}
        />
      </div>
    );
  }

  return (
    <div
      style={{
        display: "flex",
        justifyContent: isUser ? "flex-end" : "flex-start",
        marginBottom: 14,
      }}
    >
      <div
        style={{
          maxWidth: "75%",
          padding: "12px 16px",
          borderRadius: 18,
          background: isUser ? "#111" : "#ffffff",

          color: isUser ? "#fff" : "#333",

          border: isUser ? "none" : "1px solid #e5e7eb",

          fontSize: 15,
          lineHeight: 1.5,
        }}
      >
        {text}
      </div>
    </div>
  );
}
