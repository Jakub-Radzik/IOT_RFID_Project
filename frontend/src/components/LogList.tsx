import { FC, useCallback, useEffect, useState } from "react";
import { Cell, Row } from "../style/style";
import { Log } from "../types";
import { LogRow } from "./LogRow";

type Props = {
  logs: Log[];
};

const ASCsortCallback = (a: Log, b: Log) => {
    const dateA = new Date(a.date);
    const dateB = new Date(b.date);
    return dateA.getTime() - dateB.getTime();
}

const DESCsortCallback = (a: Log, b: Log) => {
    const dateA = new Date(a.date);
    const dateB = new Date(b.date);
    return dateB.getTime() - dateA.getTime();
}

export const LogList: FC<Props> = ({ logs }) => {

  const [sortedLogs, setSortedLogs] = useState<Log[]>(logs);

  const [sortDirection, setSortDirection] = useState<"ASC" | "DESC">("DESC");
  const [filter, setFilter] = useState<string>("");

  const filterHandler = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFilter(e.target.value);
    };

    const sortHandler = useCallback(() => {
        if (sortDirection === "ASC") {
            setSortDirection("DESC");
        } else {
            setSortDirection("ASC");
        }
    },[sortDirection])

    useEffect(() => {
        if (filter) {
            if(sortDirection === "ASC"){
                setSortedLogs(logs.filter(log => log.cardId.startsWith(filter)).sort(ASCsortCallback));
            }else{
                setSortedLogs(logs.filter(log => log.cardId.startsWith(filter)).sort(DESCsortCallback));
            }
        }else{
            if(sortDirection === "ASC"){
                setSortedLogs(logs.sort(ASCsortCallback));
            }else{
                setSortedLogs(logs.sort(DESCsortCallback));
            }
        }
    }, [filter, sortDirection])

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
      }}
    >
        <div style={Row}>
            <button onClick={sortHandler}>Sort by date - {sortDirection}</button>
            <input type="text" placeholder="card id" value={filter} onChange={filterHandler}/>
        </div>
      <div style={Row}>
        <div style={Cell}>ID</div>
        <div style={Cell}>Card ID</div>
        <div style={Cell}>Date</div>
        <div style={Cell}>Time</div>
      </div>
      {sortedLogs.map(log => (
        <LogRow log={log} key={log._id} />
      ))}
    </div>
  );
};
