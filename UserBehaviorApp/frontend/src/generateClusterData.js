export const generateClusterData = (results) => {
  const clusterData = [];
  results.clusters.forEach((cluster, clusterIdx) => {
    for (let i = 0; i < cluster.size; i++) {
      clusterData.push({
        x: cluster.avg_spending + (Math.random() - 0.5) * 200,
        y: cluster.avg_purchases + (Math.random() - 0.5) * 2,
        cluster: clusterIdx
      });
    }
  });
  return clusterData;
};
