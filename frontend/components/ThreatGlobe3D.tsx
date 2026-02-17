import React, { useRef, useState, useEffect } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Sphere, MeshDistortMaterial } from '@react-three/drei';
import * as THREE from 'three';

interface ThreatPoint {
  id: number;
  position: [number, number, number];
  severity: 'low' | 'medium' | 'high' | 'critical';
  type: string;
}

interface ThreatGlobe3DProps {
  threats: ThreatPoint[];
}

const AnimatedSphere: React.FC<{ position: [number, number, number]; severity: string }> = ({ position, severity }) => {
  const meshRef = useRef<THREE.Mesh>(null);
  const [hovered, setHovered] = useState(false);

  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.rotation.x += 0.01;
      meshRef.current.rotation.y += 0.01;
      const scale = hovered ? 1.5 : 1 + Math.sin(state.clock.elapsedTime * 2) * 0.1;
      meshRef.current.scale.set(scale, scale, scale);
    }
  });

  const getColor = () => {
    switch (severity) {
      case 'critical': return '#ff0000';
      case 'high': return '#ff6b00';
      case 'medium': return '#ffaa00';
      case 'low': return '#00ff00';
      default: return '#ffffff';
    }
  };

  return (
    <mesh
      ref={meshRef}
      position={position}
      onPointerOver={() => setHovered(true)}
      onPointerOut={() => setHovered(false)}
    >
      <sphereGeometry args={[0.1, 16, 16]} />
      <meshStandardMaterial color={getColor()} emissive={getColor()} emissiveIntensity={0.5} />
    </mesh>
  );
};

const CentralGlobe: React.FC = () => {
  const meshRef = useRef<THREE.Mesh>(null);

  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.rotation.y += 0.002;
    }
  });

  return (
    <mesh ref={meshRef}>
      <Sphere args={[2, 64, 64]}>
        <MeshDistortMaterial
          color="#1a1a2e"
          attach="material"
          distort={0.3}
          speed={2}
          roughness={0.4}
        />
      </Sphere>
    </mesh>
  );
};

const ThreatGlobe3D: React.FC<ThreatGlobe3DProps> = ({ threats }) => {
  return (
    <div className="w-full h-[600px] bg-gray-900 rounded-lg overflow-hidden">
      <Canvas camera={{ position: [0, 0, 8], fov: 50 }}>
        <ambientLight intensity={0.5} />
        <pointLight position={[10, 10, 10]} intensity={1} />
        <pointLight position={[-10, -10, -10]} intensity={0.5} />
        
        <CentralGlobe />
        
        {threats.map((threat) => (
          <AnimatedSphere
            key={threat.id}
            position={threat.position}
            severity={threat.severity}
          />
        ))}
        
        <OrbitControls enableZoom={true} enablePan={true} />
      </Canvas>
    </div>
  );
};

export default ThreatGlobe3D;
