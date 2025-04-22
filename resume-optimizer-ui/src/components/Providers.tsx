"use client"; // This must be at the top to use client-side features

import { Provider } from "react-redux";
import { store } from "../store";

export default function Providers({ children }: { children: React.ReactNode }) {
  return <Provider store={store}>{children}</Provider>;
}
