export default function ProductCard({ name, url, category, reason }) {
  if (!name) {
    return (
      <div
        style={{
          background: "#fff",
          border: "1px solid #e5e7eb",
          borderRadius: 16,
          padding: 16,
          color: "#666",
          fontSize: 14,
        }}
      >
        {reason}
      </div>
    );
  }

  return (
    <a
      href={url}
      target="_blank"
      rel="noopener noreferrer"
      style={{
        display: "block",
        background: "#fff",
        border: "1px solid #e5e7eb",
        borderRadius: 18,
        padding: 18,
        textDecoration: "none",
        color: "#111",
        boxShadow: "0 5px 15px rgba(0,0,0,0.03)",
      }}
    >
      <div
        style={{
          fontSize: 11,
          letterSpacing: 1,
          color: "#888",
          textTransform: "uppercase",
        }}
      >
        {category}
      </div>

      <div
        style={{
          fontSize: 17,
          fontWeight: 600,
          marginTop: 6,
        }}
      >
        {name}
      </div>

      <div
        style={{
          marginTop: 8,
          fontSize: 14,
          color: "#555",
          lineHeight: 1.5,
        }}
      >
        {reason}
      </div>

      <div
        style={{
          marginTop: 12,
          fontSize: 13,
          fontWeight: 500,
        }}
      >
        View product →
      </div>
    </a>
  );
}
