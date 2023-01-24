import { Log } from "../types";
import axios from 'axios';
import { useEffect, useState } from "react";
import useWebSocket from 'react-use-websocket';

const socketUrl = 'ws://localhost:7001';

export const useLogs = () => {
  const {sendMessage} = useWebSocket(socketUrl, {
    onOpen: () => console.log('opened'),
    onMessage: (message) => console.log(message),
    onClose: () => console.log('closed'),
    onError: (error) => console.log(error),
  });

  const [logs, setLogs] = useState<Log[]>([]);

  useEffect(() => {
    axios.get(`http://127.0.0.1:5000/logs/get`, {
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      }
    }).then(({data}) => {
      setLogs(data);
    }).catch((err) => {
      console.log(err)
    })
  
  }, [])


  return {
    logs,
  };
};
