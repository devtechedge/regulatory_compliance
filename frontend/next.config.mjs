/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Vercel traces the app itself; standalone is for Docker / self-host.
  ...(process.env.VERCEL ? {} : { output: "standalone" }),
  allowedDevOrigins: ["localhost"],
};

export default nextConfig;
