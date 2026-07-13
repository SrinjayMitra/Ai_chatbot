import { createSlice, nanoid } from "@reduxjs/toolkit";

const STORAGE_KEY = "chatbot_session_v1";

function loadInitialState() {
  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) return JSON.parse(saved);
  } catch (e) {}
  return { sessionId: nanoid(), messages: [], isLoading: false };
}

const chatSlice = createSlice({
  name: "chat",
  initialState: loadInitialState(),
  reducers: {
    messageSent: (state, action) => {
      state.messages.push({ id: nanoid(), role: "user", text: action.payload });
      state.isLoading = true;
    },
    matchReceived: (state, action) => {
      state.messages.push({ id: nanoid(), role: "bot", match: action.payload });
      state.isLoading = false;
    },
    responseFailed: (state) => {
      state.isLoading = false;
    },
    sessionCleared: (state) => {
      state.messages = [];
      state.sessionId = nanoid();
    },
  },
});

export const { messageSent, matchReceived, responseFailed, sessionCleared } =
  chatSlice.actions;
export function persistChatState(state) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state.chat));
}
export default chatSlice.reducer;
