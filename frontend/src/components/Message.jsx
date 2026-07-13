import ProductCard from "./ProductCard.jsx";

export default function Message({ role, text, match }) {
  const isUser = role === "user";

  if (!isUser && match) {
    return (
      <ProductCard
        name={match.productName}
        url={match.productUrl}
        category={match.category}
        reason={match.reason}
      />
    );
  }

  return (
    <div style={{ padding: "10px 0", fontSize: 15, lineHeight: 1.5 }}>
      <span style={{ color: "#999", marginRight: 8 }}>
        {isUser ? "You" : "Bot"}
      </span>
      <span style={{ color: isUser ? "#000" : "#555" }}>{text}</span>
    </div>
  );
}
