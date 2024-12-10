"use client"

import { ScalingRangeModal } from "@/components/scaling-range-modal"

export default function Home() {
  return (
    <main className="min-h-screen flex items-center justify-center p-4">
      <ScalingRangeModal
        isOpen={true}
        onClose={() => console.log("closed")}
        onSubmit={(data) => console.log("submitted", data)}
      />
    </main>
  )
}
