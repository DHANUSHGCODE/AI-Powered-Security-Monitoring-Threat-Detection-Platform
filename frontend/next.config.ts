import type { NextConfig } from "next";

// Fix #6: Removed ignoreBuildErrors: true
// TypeScript errors will now properly fail the build, catching real bugs early
const nextConfig: NextConfig = {
  // No typescript.ignoreBuildErrors - let real TS errors surface
};

export default nextConfig;
