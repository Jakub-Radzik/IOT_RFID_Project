import "./App.css";
import { LogList } from "./components/LogList";
import { useLogs } from "./hooks/useLogs";

function App() {
  const { logs } = useLogs();

  return (
    <div className='App'>
      <LogList logs={logs} />
    </div>
  );
}

export default App;
