import { ApolloClient, InMemoryCache, gql } from "@apollo/client";
import.meta.env.VITE_GRAPHQL_URL;

export const client = new ApolloClient({
  uri: import.meta.env.VITE_GRAPHQL_URL || "http://localhost:8000/graphql",
  cache: new InMemoryCache(),
});

export const ASK_BOT = gql`
  query AskBot($question: String!) {
    askBot(question: $question) {
      reason
      productName
      productUrl
      category
    }
  }
`;
