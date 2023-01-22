import { Log } from "../types";
import axios from 'axios';

const API_URL = 'http://127.0.0.1:5000';

export const useLogs = () => {

  axios.get(`${API_URL}/logs/get`, {
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
    }
  }).then((res) => {
    console.log("asdas")
    console.log(res)
  }).catch((err) => {
    console.log(err)
  })

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
