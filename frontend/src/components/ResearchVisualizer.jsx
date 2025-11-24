import React, { useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Sphere, MeshDistortMaterial, Stars } from '@react-three/drei';
function AnimatedCore({ status }) {
    const sphereRef = useRef();
    const isActive = status !== 'IDLE' && status !== 'COMPLETED';
    useFrame(({ clock }) => {
        const t = clock.getElapsedTime();
        sphereRef.current.rotation.x = t * 0.4;
        sphereRef.current.rotation.y = t * 0.5;
        if (isActive) {
            sphereRef.current.scale.setScalar(2 + Math.sin(t * 3) * 0.2);
        } else {
            sphereRef.current.scale.setScalar(2);
        }
    });
    return (
        <Sphere ref={sphereRef} args={[1, 64, 64]} scale={2}>
            <MeshDistortMaterial
                color={isActive ? "#6366f1" : "#334155"}
                emissive={isActive ? "#4f46e5" : "#000000"}
                emissiveIntensity={isActive ? 0.5 : 0}
                attach="material"
                distort={isActive ? 0.6 : 0.3}
                speed={isActive ? 4 : 1.5}
                roughness={0.2}
                metalness={0.9}
            />
        </Sphere>
    );
}
export default function ResearchVisualizer({ status }) {
    return (
        <div className="h-full w-full relative bg-gradient-to-b from-slate-900 to-black">
            <div className="absolute top-0 left-0 w-full p-4 z-10 flex justify-between items-start pointer-events-none">
                <div>
                    <h3 className="text-xs font-bold text-slate-500 uppercase tracking-[0.2em]">System Status</h3>
                    <p className="text-lg font-mono mt-1 text-white drop-shadow-lg">
                        {status === 'IDLE' ? <span className="text-slate-500">STANDBY</span> :
                            status === 'COMPLETED' ? <span className="text-emerald-400">COMPLETE</span> :
                                <span className="text-indigo-400 animate-pulse">{status}</span>}
                    </p>
                </div>
                <div className="flex gap-1">
                    {[1, 2, 3].map(i => (
                        <div key={i} className={`w-1 h-1 rounded-full ${status !== 'IDLE' ? 'bg-indigo-500 animate-ping' : 'bg-slate-800'}`} style={{ animationDelay: `${i * 200}ms` }} />
                    ))}
                </div>
            </div>
            <Canvas camera={{ position: [0, 0, 6] }}>
                <color attach="background" args={['#050505']} />
                <ambientLight intensity={0.5} />
                <pointLight position={[10, 10, 10]} intensity={1} color="#4f46e5" />
                <pointLight position={[-10, -10, -10]} intensity={0.5} color="#10b981" />
                <Stars radius={100} depth={50} count={5000} factor={4} saturation={0} fade speed={1} />
                <AnimatedCore status={status} />
                <OrbitControls enableZoom={false} autoRotate autoRotateSpeed={0.5} />
            </Canvas>
        </div>
    );
}