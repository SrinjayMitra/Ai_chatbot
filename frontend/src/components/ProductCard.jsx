// export default function ProductCard({ name, url, category, reason }) {
//   if (!name) {
//     return (
//       <div
//         style={{
//           padding: 12,
//           borderRadius: 10,
//           background: "#fef3c7",
//           margin: "6px 0",
//           fontSize: 14,
//         }}
//       >
//         {reason}
//       </div>
//     );
//   }
//   return (
//     <a
//       href={url}
//       target="_blank"
//       rel="noopener noreferrer"
//       style={{
//         display: "block",
//         padding: 12,
//         borderRadius: 10,
//         border: "1px solid #d1d5db",
//         margin: "6px 0",
//         textDecoration: "none",
//         color: "inherit",
//         background: "white",
//       }}
//     >
//       <div
//         style={{ fontSize: 12, color: "#6b7280", textTransform: "uppercase" }}
//       >
//         {category}
//       </div>
//       <div style={{ fontWeight: 600, margin: "4px 0" }}>{name}</div>
//       <div style={{ fontSize: 14, color: "#374151" }}>{reason}</div>
//       <div style={{ fontSize: 13, color: "#4f46e5", marginTop: 6 }}>
//         View product →
//       </div>
//     </a>
//   );
// }

export default function ProductCard({ name, url, category, reason }) {
  if (!name) {
    return (
      <div
        style={{
          padding: "12px 0",
          fontSize: 14,
          color: "#666",
          lineHeight: 1.5,
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
        padding: "14px 0",
        borderTop: "1px solid #eee",
        textDecoration: "none",
        color: "inherit",
      }}
    >
      <div
        style={{
          fontSize: 11,
          color: "#999",
          letterSpacing: "0.05em",
          textTransform: "uppercase",
        }}
      >
        {category}
      </div>
      <div style={{ fontSize: 16, fontWeight: 500, margin: "4px 0" }}>
        {name}
      </div>
      <div style={{ fontSize: 14, color: "#555", lineHeight: 1.5 }}>
        {reason}
      </div>
      <div
        style={{
          fontSize: 13,
          color: "#000",
          marginTop: 8,
          textDecoration: "underline",
        }}
      >
        View product
      </div>
    </a>
  );
}
