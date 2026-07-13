import { ApolloProvider } from "@apollo/client";
import { Provider } from "react-redux";
import { Analytics } from "@vercel/analytics/react";
import { client } from "./apollo/client.js";
import { store } from "./redux/store.js";
import ChatWindow from "./components/ChatWindow.jsx";

export default function App() {
  return (
    <ApolloProvider client={client}>
      <Provider store={store}>
        <ChatWindow />
        <Analytics />
      </Provider>
    </ApolloProvider>
  );
}
