import { NextResponse } from "next/server";
import { reviewFinding } from "@/lib/demo-store";
import { gateMutation } from "@/lib/demo-gate";

export const dynamic = "force-dynamic";
export const runtime = "nodejs";

export async function POST(req: Request, { params }: { params: { id: string } }) {
  const blocked = gateMutation(req);
  if (blocked) return blocked;

  const body = (await req.json().catch(() => ({}))) as {
    action?: "accept" | "edit" | "reject";
    override_text?: string;
    note?: string;
  };
  if (body.action !== "accept" && body.action !== "edit" && body.action !== "reject") {
    return NextResponse.json({ detail: "Invalid action" }, { status: 400 });
  }
  const finding = reviewFinding(params.id, {
    action: body.action,
    override_text: body.override_text,
    note: body.note,
  });
  if (!finding) {
    return NextResponse.json({ detail: "Finding not found" }, { status: 404 });
  }
  return NextResponse.json(finding);
}
