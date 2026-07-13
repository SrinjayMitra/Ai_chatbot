import { configureStore } from "@reduxjs/toolkit";
import chatReducer, { persistChatState } from "./chatSlice.js";

export const store = configureStore({ reducer: { chat: chatReducer } });
store.subscribe(() => persistChatState(store.getState()));
