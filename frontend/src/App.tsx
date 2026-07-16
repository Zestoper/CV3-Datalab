import { useEffect, useState } from "react";
import BroadcastTable from "./BroadcastTable";
import type { Broadcast, BroadcastType } from "./types";

function App() {
  const [type, setType] = useState<BroadcastType>("lb");
  const [broadcasts, setBroadcasts] = useState<Broadcast[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    fetch(`/api/broadcasts?type=${type}`)
      .then((res) => res.json())
      .then((data: Broadcast[]) => setBroadcasts(data))
      .finally(() => setLoading(false));
  }, [type]);

  return (
    <div className="container">
      <h1>라방 · 홈쇼핑 랭킹</h1>
      <div className="tabs">
        <button
          className={type === "lb" ? "active" : ""}
          onClick={() => setType("lb")}
        >
          라방
        </button>
        <button
          className={type === "hs" ? "active" : ""}
          onClick={() => setType("hs")}
        >
          홈쇼핑
        </button>
      </div>
      {loading ? <p>불러오는 중...</p> : <BroadcastTable broadcasts={broadcasts} />}
    </div>
  );
}

export default App;
