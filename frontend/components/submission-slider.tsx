"use client"
import { Slider } from "@/components/ui/slider"
import { Label } from "@/components/ui/label"
import { TrendingUp } from "lucide-react"

interface SubmissionSliderProps {
  minSubmissions: number
  maxSubmissions: number
  value: [number, number]
  onChange: (value: [number, number]) => void
}

export function SubmissionSlider({ minSubmissions, maxSubmissions, value, onChange }: SubmissionSliderProps) {
  return (
    <div className="space-y-3 p-4 border border-border rounded-lg bg-card/50">
      <div className="flex items-center gap-2">
        <TrendingUp className="h-4 w-4 text-muted-foreground" />
        <Label className="text-sm font-medium">Submission Count Range</Label>
      </div>

      <div className="px-2">
        <Slider
          value={value}
          onValueChange={onChange}
          min={minSubmissions}
          max={maxSubmissions}
          step={1}
          className="w-full"
        />
      </div>

      <div className="flex items-center justify-between text-xs text-muted-foreground px-2">
        <span>{value[0]} submissions</span>
        <span>{value[1]} submissions</span>
      </div>

      <div className="flex items-center justify-between text-xs text-muted-foreground px-2">
        <span>Min: {minSubmissions}</span>
        <span>Max: {maxSubmissions}</span>
      </div>
    </div>
  )
}
