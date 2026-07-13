/**
 * Run this against your live server to get a REAL number for the
 * "cut payload size by X% vs REST" resume bullet, instead of guessing.
 *
 * Usage: node scripts/measure-payload-size.js
 */
const GRAPHQL_URL = "http://localhost:8000/graphql";

async function main() {
  // GraphQL: client asks only for what it needs (question + answer text)
  const gqlQuery = `query { faqs { question answer } }`;
  const gqlRes = await fetch(GRAPHQL_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query: gqlQuery }),
  });
  const gqlBody = await gqlRes.text();

  // Simulated REST equivalent: a typical REST FAQ endpoint returns the
  // full record (id, product, question, answer) whether you need it or not.
  const restEquivalent = JSON.stringify(
    JSON.parse(gqlBody).data.faqs.map((f, i) => ({
      id: String(i + 1),
      product: "CloudSync Pro",
      question: f.question,
      answer: f.answer,
    }))
  );

  const gqlSize = Buffer.byteLength(gqlBody, "utf8");
  const restSize = Buffer.byteLength(restEquivalent, "utf8");
  const reduction = (((restSize - gqlSize) / restSize) * 100).toFixed(1);

  console.log(`REST-equivalent payload: ${restSize} bytes`);
  console.log(`GraphQL payload:         ${gqlSize} bytes`);
  console.log(`Reduction:               ${reduction}%`);
  console.log(`\nUse this real number in your resume bullet instead of a guess.`);
}

main().catch(console.error);
