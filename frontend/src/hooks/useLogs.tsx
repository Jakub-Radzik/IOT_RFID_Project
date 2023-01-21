import { Log } from "../types";

export const useLogs = () => {
  const logs: Log[] = [
    {
      _id: "1",
      cardId: "1",
      date: "2023-01-20T16:49:01.618Z",
    },
    {
      _id: "2",
      cardId: "134",
      date: "2023-01-21T12:49:01.618Z",
    },
    {
      _id: "3",
      cardId: "123",
      date: new Date().toISOString(),
    },
    {
      _id: "4",
      cardId: "133",
      date: "2023-01-21T16:49:01.618Z",
    },
  ];

  return {
    logs,
  };
};
