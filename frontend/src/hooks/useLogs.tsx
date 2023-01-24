import { Log } from "../types";
import axios from 'axios';
import { useEffect, useState } from "react";
import useWebSocket from 'react-use-websocket';
import _ from 'lodash';

const socketUrl = 'ws://localhost:7001';

export const useLogs = () => {
  const [logs, setLogs] = useState<Log[]>([]);

  const wsMessageHandler = (message: MessageEvent<string>) => {
      const data = JSON.parse(message.data);
      setLogs([...logs, data]);
  }

  useWebSocket(socketUrl, {
    onOpen: () => console.log('opened'),
    onMessage: wsMessageHandler,
    onClose: () => console.log('closed'),
    onError: (error) => console.log(error),
  });

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
