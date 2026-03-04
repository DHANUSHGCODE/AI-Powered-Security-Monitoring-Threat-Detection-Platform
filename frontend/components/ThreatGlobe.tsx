import React, { Suspense } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Stars, Sphere, useTexture } from '@react-three/drei';

// Simple Earth globe with texture (public domain image)
const Earth = () => {
    const [colorMap] = useTexture([
        'https://raw.githubusercontent.com/creativetimofficial/public-assets/master/soft-ui-dashboard-pro/assets/img/earth.jpg',
    ]);
    return (
        <Sphere args={[1, 64, 64]}>
            <meshStandardMaterial map={colorMap} metalness={0.1} roughness={0.9} />
        </Sphere>
    );
};

const ThreatGlobe: React.FC = () => {
    return (
        <div className="w-full h-64">
            <Canvas camera={{ position: [0, 0, 3] }}>
                <ambientLight intensity={0.5} />
                <directionalLight position={[5, 5, 5]} intensity={1} />
                <Suspense fallback={null}>
                    <Earth />
                </Suspense>
                <OrbitControls enableZoom={true} />
                <Stars radius={100} depth={50} count={5000} factor={4} saturation={0} fade />
            </Canvas>
        </div>
    );
};

export default ThreatGlobe;
