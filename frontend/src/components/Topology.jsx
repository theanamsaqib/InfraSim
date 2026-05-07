import { motion } from "framer-motion";


function Node({
  label,
  active,
  x,
  y
}) {

  return (

    <motion.div

      animate={{
        scale: active ? 1.1 : 1,
        opacity: active ? 1 : 0.7
      }}

      transition={{
        duration: 0.5
      }}

      className={`
        absolute
        px-4
        py-3
        rounded-xl
        text-white
        font-bold
        shadow-xl
        border
        ${
          active
            ? "bg-green-600 border-green-300"
            : "bg-slate-700 border-slate-500"
        }
      `}

      style={{
        left: x,
        top: y
      }}
    >

      {label}

    </motion.div>
  );
}


function Connection({
  x1,
  y1,
  x2,
  y2
}) {

  const length = Math.sqrt(
    Math.pow(x2 - x1, 2) +
    Math.pow(y2 - y1, 2)
  );

  const angle = Math.atan2(
    y2 - y1,
    x2 - x1
  ) * (180 / Math.PI);

  return (

    <div

      className="
        absolute
        bg-cyan-400
      "

      style={{
        left: x1,
        top: y1,
        width: length,
        height: 2,
        transform:
          `rotate(${angle}deg)`,

        transformOrigin:
          "0 0"
      }}
    />
  );
}


function Topology({
  servers
}) {

  return (

    <div className="
      relative
      h-[600px]
      bg-slate-800
      rounded-2xl
      overflow-hidden
      mt-10
    ">

      <h2 className="
        text-3xl
        font-bold
        p-6
      ">
        Infrastructure Topology
      </h2>

      <Connection
        x1={500}
        y1={120}
        x2={500}
        y2={220}
      />

      <Connection
        x1={500}
        y1={320}
        x2={250}
        y2={450}
      />

      <Connection
        x1={500}
        y1={320}
        x2={500}
        y2={450}
      />

      <Connection
        x1={500}
        y1={320}
        x2={750}
        y2={450}
      />

      <Node
        label="CLIENTS"
        active={true}
        x={430}
        y={50}
      />

      <Node
        label="DNS"
        active={true}
        x={460}
        y={150}
      />

      <Node
        label="LOAD BALANCER"
        active={true}
        x={410}
        y={250}
      />

      <Node
        label="INDIA REGION"
        active={
          servers.some(
            (s) =>
              s.region === "INDIA" &&
              s.healthy
          )
        }
        x={180}
        y={430}
      />

      <Node
        label="EUROPE REGION"
        active={
          servers.some(
            (s) =>
              s.region === "EUROPE" &&
              s.healthy
          )
        }
        x={430}
        y={430}
      />

      <Node
        label="US REGION"
        active={
          servers.some(
            (s) =>
              s.region === "US" &&
              s.healthy
          )
        }
        x={700}
        y={430}
      />

    </div>
  );
}

export default Topology;