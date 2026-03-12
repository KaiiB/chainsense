import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

interface HeatmapProps {
  data: number[][];
  labels: string[];
  title: string;
}

export const Heatmap: React.FC<HeatmapProps> = ({ data, labels, title }) => {
  const svgRef = useRef<SVGSVGElement>(null);

  useEffect(() => {
    if (!svgRef.current || !data.length) return;

    const size = 40;
    const margin = { top: 30, right: 20, bottom: 100, left: 100 };
    const width = labels.length * size + margin.left + margin.right;
    const height = labels.length * size + margin.top + margin.bottom;

    d3.select(svgRef.current).selectAll("*").remove();

    const svg = d3.select(svgRef.current)
      .attr('width', width)
      .attr('height', height)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    const colorScale = d3.scaleLinear<string>()
      .domain([-1, 0, 1])
      .range(['#d62728', '#fff', '#2ca02c']);

    // Cells
    svg.selectAll('rect')
      .data(data.flat().map((v, i) => ({ value: v, row: Math.floor(i / data.length), col: i % data.length })))
      .enter()
      .append('rect')
      .attr('class', 'heatmap-cell')
      .attr('x', d => d.col * size)
      .attr('y', d => d.row * size)
      .attr('width', size)
      .attr('height', size)
      .attr('fill', d => colorScale(d.value))
      .append('title')
      .text(d => `${d.value.toFixed(2)}`);

    // X labels
    svg.selectAll('.x-label')
      .data(labels)
      .enter()
      .append('text')
      .attr('class', 'heatmap-label x-label')
      .attr('x', (d, i) => i * size + size / 2)
      .attr('y', -10)
      .text(d => d)
      .style('font-size', '9px');

    // Y labels
    svg.selectAll('.y-label')
      .data(labels)
      .enter()
      .append('text')
      .attr('class', 'heatmap-label y-label')
      .attr('x', -10)
      .attr('y', (d, i) => i * size + size / 2 + 4)
      .text(d => d)
      .style('text-anchor', 'end')
      .style('font-size', '9px');

    // Title
    svg.append('text')
      .attr('x', (labels.length * size) / 2)
      .attr('y', -30)
      .attr('text-anchor', 'middle')
      .style('font-size', '14px')
      .style('font-weight', 'bold')
      .text(title);

  }, [data, labels, title]);

  return <svg ref={svgRef}></svg>;
};
