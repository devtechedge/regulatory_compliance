import { NextResponse } from "next/server";
import { health } from "@/lib/demo-store";

export const dynamic = "force-dynamic";
export const runtime = "nodejs";

export function GET() {
  return NextResponse.json(health());
}
