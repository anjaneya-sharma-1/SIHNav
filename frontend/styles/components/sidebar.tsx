"use client"
import { TagFilter } from "@/components/tag-filter"
import { SubmissionSlider } from "@/components/submission-slider"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { X, Filter, ArrowUpDown } from "lucide-react"

interface SidebarProps {
  isOpen: boolean
  onClose: () => void
  availableTags: Record<string, string[]>
  selectedTags: string[]
  onTagToggle: (tag: string) => void
  minSubmissions: number
  maxSubmissions: number
  submissionRange: [number, number]
  onSubmissionRangeChange: (range: [number, number]) => void
  sortBy: "relevance" | "submissions_high" | "submissions_low"
  onSortChange: (value: "relevance" | "submissions_high" | "submissions_low") => void
}

export function Sidebar({
  isOpen,
  onClose,
  availableTags,
  selectedTags,
  onTagToggle,
  minSubmissions,
  maxSubmissions,
  submissionRange,
  onSubmissionRangeChange,
  sortBy,
  onSortChange,
}: SidebarProps) {
  if (!isOpen) return null

  return (
    <>
      {/* Overlay for mobile */}
      <div className="fixed inset-0 bg-black/50 z-40 lg:hidden" onClick={onClose} />

      {/* Sidebar */}
      <div className="fixed left-0 top-0 h-full w-72 sm:w-80 bg-card border-r border-border z-50 overflow-y-auto">
        <div className="p-4 sm:p-6 space-y-4 sm:space-y-6">
          {/* Header */}
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Filter className="h-4 w-4 sm:h-5 sm:w-5 text-primary" />
              <h2 className="text-base sm:text-lg font-semibold text-foreground">Filters & Sort</h2>
            </div>
            <Button variant="ghost" size="sm" onClick={onClose}>
              <X className="h-4 w-4" />
            </Button>
          </div>

          {/* Active Filters Summary */}
          {selectedTags.length > 0 && (
            <div className="space-y-2">
              <h3 className="text-sm font-medium text-foreground">Active Filters</h3>
              <Badge variant="outline" className="text-xs">
                {selectedTags.length} tag{selectedTags.length !== 1 ? "s" : ""} selected
              </Badge>
            </div>
          )}

          {/* Sort Options */}
          <div className="space-y-2 sm:space-y-3">
            <div className="flex items-center gap-2">
              <ArrowUpDown className="w-4 h-4 text-muted-foreground" />
              <h3 className="text-sm font-medium text-foreground">Sort By</h3>
            </div>
            <Select value={sortBy} onValueChange={onSortChange}>
              <SelectTrigger className="w-full text-sm">
                <SelectValue placeholder="Sort by..." />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="relevance">Sort by Relevance</SelectItem>
                <SelectItem value="submissions_high">Most Submissions</SelectItem>
                <SelectItem value="submissions_low">Least Submissions</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {/* Submission Count Slider */}
          <div className="space-y-2 sm:space-y-3">
            <h3 className="text-sm font-medium text-foreground">Submission Count Range</h3>
            <SubmissionSlider
              minSubmissions={minSubmissions}
              maxSubmissions={maxSubmissions}
              value={submissionRange}
              onChange={onSubmissionRangeChange}
            />
          </div>

          {/* Tag Filters */}
          <div className="space-y-2 sm:space-y-3">
            <h3 className="text-sm font-medium text-foreground">Filter by Tags</h3>
            <TagFilter availableTags={availableTags} selectedTags={selectedTags} onTagToggle={onTagToggle} />
          </div>
        </div>
      </div>
    </>
  )
}
