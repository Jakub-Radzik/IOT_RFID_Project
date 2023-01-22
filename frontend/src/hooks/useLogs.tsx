import { Log } from "../types";
import axios, { AxiosResponse } from 'axios';
import { useEffect, useState } from "react";

export const useLogs = () => {

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
