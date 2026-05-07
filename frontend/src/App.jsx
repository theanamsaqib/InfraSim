import {
  useEffect,
  useState
} from "react";

import Topology from "./components/Topology";

import {
  Activity,
  Server,
  Wifi,
  Database
} from "lucide-react";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer
} from "recharts";


function getLatencyColor(latency) {

  if (latency < 1.5) {

    return "text-green-400";
  }

  if (latency < 3) {

    return "text-yellow-400";
  }

  return "text-red-400";
}


function MetricCard({
  title,
  value,
  icon
}) {

  return (

    <div className="
      bg-slate-800
      rounded-2xl
      p-5
      shadow-lg
    ">

      <div className="
        flex
        justify-between
        items-center
      ">

        <div>

          <p className="text-slate-400">
            {title}
          </p>

          <h2 className="
            text-3xl
            font-bold
            mt-2
          ">
            {value}
          </h2>

        </div>

        {icon}

      </div>

    </div>
  );
}


function LatencyCard({
  title,
  value
}) {

  return (

    <div className="
      bg-slate-800
      rounded-2xl
      p-5
      shadow-lg
    ">

      <p className="text-slate-400">
        {title}
      </p>

      <h2 className={`
        text-4xl
        font-bold
        mt-3
        ${
          getLatencyColor(value)
        }
      `}>

        {value || 0}s

      </h2>

    </div>
  );
}


function ServerCard({
  server
}) {

  return (

    <div className={`
      rounded-2xl
      p-4
      shadow-lg
      border
      transition-all
      duration-300
      ${
        server.healthy
          ? "bg-green-900 border-green-500"
          : "bg-red-900 border-red-500"
      }
    `}>

      <h3 className="
        text-xl
        font-bold
      ">
        {server.server_id}
      </h3>

      <p className="mt-2">
        Region: {server.region}
      </p>

      <p className="mt-1">
        Status:
        {
          server.healthy
            ? " HEALTHY"
            : " DOWN"
        }
      </p>

    </div>
  );
}


function TraceItem({
  trace
}) {

  return (

    <div className="
      bg-slate-800
      rounded-xl
      p-3
      mb-3
    ">

      <p className="font-bold">
        Trace {trace.trace_id}
      </p>

      <p>
        {trace.service}
        {" → "}
        {trace.operation}
      </p>

      <p className="text-slate-400">
        {trace.duration_ms} ms
      </p>

    </div>
  );
}


function App() {

  const [metrics, setMetrics] = useState({

    total_requests: 0,

    successful_requests: 0,

    failed_requests: 0,

    server_failures: 0,

    packet_loss_events: 0,

    cache_hits: 0,

    cache_misses: 0,

    average_latency: 0,

    latest_latency: 0,

    p50_latency: 0,

    p95_latency: 0,

    p99_latency: 0,

    uptime_seconds: 0
  });

  const [history, setHistory] =
    useState([]);

  const [servers, setServers] =
    useState([]);

  const [traces, setTraces] =
    useState([]);


  useEffect(() => {

    const socket = new WebSocket(
      "wss://your-backend.onrender.com/ws"
    );

    socket.onopen = () => {

      console.log(
        "Connected to InfraSim backend"
      );
    };

    socket.onmessage = (event) => {

      const message = JSON.parse(
        event.data
      );

      if (
        message.type === "metrics"
      ) {

        setMetrics(message.data);

        setHistory((prev) => [

          ...prev.slice(-20),

          {
            time: new Date()
              .toLocaleTimeString(),

            latency: Number(
              message.data
                .latest_latency || 0
            )
          }
        ]);
      }

      if (
        message.type === "servers"
      ) {

        setServers(message.data);
      }

      if (
        message.type === "trace"
      ) {

        setTraces((prev) => [

          message.data,

          ...prev.slice(0, 9)
        ]);
      }
    };

    return () => socket.close();

  }, []);


  return (

    <div className="
      min-h-screen
      bg-slate-900
      text-white
      p-6
    ">

      <h1 className="
        text-5xl
        font-bold
        mb-8
      ">
        InfraSim Dashboard
      </h1>

      {/* PRIMARY METRICS */}

      <div className="
        grid
        grid-cols-1
        md:grid-cols-2
        lg:grid-cols-4
        gap-6
      ">

        <MetricCard
          title="Requests"
          value={
            metrics.total_requests || 0
          }
          icon={<Activity />}
        />

        <MetricCard
          title="Failures"
          value={
            metrics.server_failures || 0
          }
          icon={<Server />}
        />

        <MetricCard
          title="Packet Loss"
          value={
            metrics.packet_loss_events || 0
          }
          icon={<Wifi />}
        />

        <MetricCard
          title="Cache Hits"
          value={
            metrics.cache_hits || 0
          }
          icon={<Database />}
        />

      </div>


      {/* LATENCY METRICS */}

      <div className="
        grid
        grid-cols-1
        md:grid-cols-3
        gap-6
        mt-6
      ">

        <LatencyCard
          title="P50 Latency"
          value={metrics.p50_latency}
        />

        <LatencyCard
          title="P95 Latency"
          value={metrics.p95_latency}
        />

        <LatencyCard
          title="P99 Latency"
          value={metrics.p99_latency}
        />

      </div>


      {/* LATENCY GRAPH */}

      <div className="
        mt-10
        bg-slate-800
        p-6
        rounded-2xl
      ">

        <h2 className="
          text-2xl
          font-bold
          mb-4
        ">
          Live Latency
        </h2>

        <ResponsiveContainer
          width="100%"
          height={300}
        >

          <LineChart data={history}>

            <XAxis dataKey="time" />

            <YAxis />

            <Tooltip />

            <Line
              type="monotone"
              dataKey="latency"
              stroke="#38bdf8"
              strokeWidth={3}
            />

          </LineChart>

        </ResponsiveContainer>

      </div>


      {/* TOPOLOGY */}

      <Topology servers={servers} />


      {/* SERVER GRID */}

      <div className="mt-10">

        <h2 className="
          text-3xl
          font-bold
          mb-5
        ">
          Regional Infrastructure
        </h2>

        <div className="
          grid
          grid-cols-1
          md:grid-cols-2
          lg:grid-cols-3
          gap-4
        ">

          {
            servers.map((server) => (

              <ServerCard
                key={server.server_id}
                server={server}
              />

            ))
          }

        </div>

      </div>


      {/* DISTRIBUTED TRACES */}

      <div className="mt-10">

        <h2 className="
          text-3xl
          font-bold
          mb-5
        ">
          Live Distributed Traces
        </h2>

        {
          traces.map((trace, index) => (

            <TraceItem
              key={index}
              trace={trace}
            />

          ))
        }

      </div>

    </div>
  );
}

export default App;