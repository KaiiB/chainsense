import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import { Wallet } from '../types';

interface ScatterProps {
  data: Wallet[];
  xField: 'pc1' | 'ld1';
  yField: 'pc2' | 'ld2';
  title: string;
  colorField: 'cluster_id';
}

export const ScatterChart: React.FC<ScatterProps> = ({
  data,
  xField,
  yField,
  title,
  colorField
}) => {
  const svgRef = useRef<SVGSVGElement>(null);

  useEffect(() => {
    if (!svgRef.current || data.length === 0) return;

    const margin = { top: 30, right: 30, bottom: 50, left: 50 };
    const width = 600 - margin.left - margin.right;
    const height = 500 - margin.top - margin.bottom;

    // Clear previous content
    d3.select(svgRef.current).selectAll("*").remove();

    const svg = d3.select(svgRef.current)
      .attr('width', width + margin.left + margin.right)
      .attr('height', height + margin.top + margin.bottom)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    // Scales
    const xScale = d3.scaleLinear()
      .domain(d3.extent(data, d => d[xField]) as [number, number])
      .range([0, width])
      .nice();

    const yScale = d3.scaleLinear()
      .domain(d3.extent(data, d => d[yField]) as [number, number])
      .range([height, 0])
      .nice();

    const colorScale = d3.scaleOrdinal(d3.schemeCategory10);

    // Grid lines
    svg.append('g')
      .attr('class', 'grid-line')
      .attr('transform', `translate(0,${height})`)
      .call(d3.axisBottom(xScale)
        .tickSize(-height)
        .tickFormat(() => ''));

    svg.append('g')
      .attr('class', 'grid-line')
      .call(d3.axisLeft(yScale)
        .tickSize(-width)
        .tickFormat(() => ''));

    // Points
    svg.selectAll('.dot')
      .data(data)
      .enter()
      .append('circle')
      .attr('class', 'dot')
      .attr('cx', d => xScale(d[xField]))
      .attr('cy', d => yScale(d[yField]))
      .attr('r', 3)
      .attr('fill', d => colorScale(String(d[colorField])))
      .attr('opacity', 0.65)
      .append('title')
      .text(d => `${d.wallet.slice(0, 10)}... | Cluster ${d.cluster_id}`);

    // Axes
    svg.append('g')
      .attr('transform', `translate(0,${height})`)
      .call(d3.axisBottom(xScale));

    svg.append('g')
      .call(d3.axisLeft(yScale));

    // Labels
    svg.append('text')
      .attr('class', 'axis-label')
      .attr('x', width / 2)
      .attr('y', height + 40)
      .text(xField.toUpperCase());

    svg.append('text')
      .attr('class', 'axis-label')
      .attr('transform', 'rotate(-90)')
      .attr('y', 0 - margin.left)
      .attr('x', 0 - (height / 2))
      .attr('dy', '1em')
      .text(yField.toUpperCase());

    // Title
    svg.append('text')
      .attr('x', width / 2)
      .attr('y', -10)
      .attr('text-anchor', 'middle')
      .style('font-size', '14px')
      .style('font-weight', 'bold')
      .text(title);

  }, [data, xField, yField, title]);

  return <svg ref={svgRef}></svg>;
};
