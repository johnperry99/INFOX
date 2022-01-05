import React from "react";
import { getForkClustering } from "./repository";

const ForkCluster = () => {
  return (
    <div>
      <button
        onClick={() => {
          getForkClustering("tensorflow/tensorflow");
        }}
      >
        click HERE
      </button>
    </div>
  );
};

export default ForkCluster;
