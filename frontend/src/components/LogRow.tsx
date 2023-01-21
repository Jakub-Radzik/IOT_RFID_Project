import { FC } from "react";
import { Cell, Row } from "../style/style";
import { Log } from "../types";
import { formatDate, formatTime } from "../utils/date";

type Props = {
  log: Log;
};

export const LogRow: FC<Props> = ({ log }) => {
  const { _id, cardId, date } = log;

  return (
    <div style={Row}>
      <div style={Cell}>{_id}</div>
      <div style={Cell}>{cardId}</div>
      <div style={Cell}>{formatDate(date)}</div>
      <div style={Cell}>{formatTime(date)}</div>
    </div>
  );
};
