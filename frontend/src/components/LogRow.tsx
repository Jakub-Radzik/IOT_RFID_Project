import { FC } from "react";
import { Cell, Row } from "../style/style";
import { Log } from "../types";
import { formatDate, formatTime } from "../utils/date";

type Props = {
  log: Log;
};

export const LogRow: FC<Props> = ({ log }) => {
  const { card_uid, date, log_id } = log;

  return (
    <div style={Row}>
      <div style={Cell}>{log_id}</div>
      <div style={Cell}>{card_uid}</div>
      <div style={Cell}>{formatDate(date)}</div>
      <div style={Cell}>{formatTime(date)}</div>
    </div>
  );
};
