import React, { useRef, useMemo } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Line, Sphere, Text } from '@react-three/drei';
import * as THREE from 'three';

interface Node {
  id: string;
  label: string;
  position: [number, number, number];
  type: 'server' | 'client' | 'threat';
}

interface Edge {
  source: string;
  target: string;
  strength: number;
}

interface NetworkGraph3DProps {
  nodes: Node[];
  edges: Edge[];
}

const NetworkNode: React.FC<{ node: Node; isHovered: boolean; onHover: (id: string | null) => void }> = ({ node, isHovered, onHover }) => {
  const meshRef = useRef<THREE.Mesh>(null);

  useFrame(() => {
    if (meshRef.current && isHovered) {
      meshRef.current.rotation.y += 0.05;
    }
  });

  const getNodeColor = () => {
    switch (node.type) {
      case 'server': return '#00ff88';
      case 'client': return '#0088ff';
      case 'threat': return '#ff0044';
      default: return '#ffffff';
    }
  };

  const nodeSize = isHovered ? 0.3 : 0.2;

  return (
    <group position={node.position}>
      <Sphere
        ref={meshRef}
        args={[nodeSize, 32, 32]}
        onPointerOver={() => onHover(node.id)}
        onPointerOut={() => onHover(null)}
      >
        <meshStandardMaterial
          color={getNodeColor()}
          emissive={getNodeColor()}
          emissiveIntensity={isHovered ? 0.8 : 0.3}
          metalness={0.5}
          roughness={0.3}
        />
      </Sphere>
      {isHovered && (
        <Text
          position={[0, 0.5, 0]}
          fontSize={0.2}
          color="white"
          anchorX="center"
          anchorY="middle"
        >
          {node.label}
        </Text>
      )}
    </group>
  );
};

const NetworkEdge: React.FC<{ start: [number, number, number]; end: [number, number, number]; strength: number }> = ({ start, end, strength }) => {
  const points = useMemo(() => [
    new THREE.Vector3(...start),
    new THREE.Vector3(...end)
  ], [start, end]);

  return (
    <Line
      points={points}
      color={strength > 0.7 ? '#ff4444' : '#4488ff'}
      lineWidth={strength * 3}
      opacity={0.6}
      transparent
    />
  );
};

const NetworkGraph3D: React.FC<NetworkGraph3DProps> = ({ nodes, edges }) => {
  const [hoveredNode, setHoveredNode] = React.useState<string | null>(null);

  const nodeMap = useMemo(() => {
    const map = new Map<string, [number, number, number]>();
    nodes.forEach(node => map.set(node.id, node.position));
    return map;
  }, [nodes]);

  return (
    <div className="w-full h-[600px] bg-gray-900 rounded-lg overflow-hidden">
      <Canvas camera={{ position: [0, 0, 10], fov: 60 }}>
        <ambientLight intensity={0.4} />
        <pointLight position={[10, 10, 10]} intensity={1} />
        <pointLight position={[-10, -10, -10]} intensity={0.5} />
        <spotLight position={[0, 10, 0]} angle={0.3} penumbra={1} intensity={0.8} />

        {edges.map((edge, index) => {
          const start = nodeMap.get(edge.source);
          const end = nodeMap.get(edge.target);
          if (start && end) {
            return <NetworkEdge key={index} start={start} end={end} strength={edge.strength} />;
          }
          return null;
        })}

        {nodes.map((node) => (
          <NetworkNode
            key={node.id}
            node={node}
            isHovered={hoveredNode === node.id}
            onHover={setHoveredNode}
          />
        ))}

        <OrbitControls enableZoom={true} enablePan={true} autoRotate autoRotateSpeed={0.5} />
      </Canvas>
    </div>
  );
};

export default NetworkGraph3D;
