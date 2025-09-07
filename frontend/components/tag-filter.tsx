"use client"

import { Badge } from "@/components/ui/badge"
import { X, ChevronDown, ChevronUp } from "lucide-react"
import { useState } from "react"

interface TagFilterProps {
  availableTags: Record<string, string[]>
  selectedTags: string[]
  onTagToggle: (tag: string) => void
}

export function TagFilter({ availableTags, selectedTags, onTagToggle }: TagFilterProps) {
  const [expandedCategories, setExpandedCategories] = useState<Record<string, boolean>>({
    Technology: true,
    Stakeholders: true,
  })

  const toggleCategory = (category: string) => {
    setExpandedCategories((prev) => ({
      ...prev,
      [category]: !prev[category],
    }))
  }

  return (
    <div className="w-full">
      <div className="space-y-4">
        {Object.entries(availableTags).map(([category, tags]) => {
          const isExpanded = expandedCategories[category]
          const categorySelectedCount = tags.filter((tag) => selectedTags.includes(tag)).length

          return (
            <div key={category} className="border border-border rounded-lg p-4 bg-card/50">
              <button
                onClick={() => toggleCategory(category)}
                className="flex items-center justify-between w-full text-left mb-3 hover:text-primary transition-colors"
              >
                <div className="flex items-center gap-2">
                  <h4 className="font-medium text-foreground">{category}</h4>
                  {categorySelectedCount > 0 && (
                    <Badge variant="outline" className="text-xs">
                      {categorySelectedCount} selected
                    </Badge>
                  )}
                </div>
                {isExpanded ? (
                  <ChevronUp className="h-4 w-4 text-muted-foreground" />
                ) : (
                  <ChevronDown className="h-4 w-4 text-muted-foreground" />
                )}
              </button>

              {isExpanded && (
                <div className="flex flex-wrap gap-2">
                  {tags.map((tag) => {
                    const isSelected = selectedTags.includes(tag)
                    return (
                      <Badge
                        key={tag}
                        variant={isSelected ? "default" : "secondary"}
                        className={`cursor-pointer transition-all duration-200 hover:scale-105 ${
                          isSelected
                            ? "bg-primary text-primary-foreground hover:bg-primary/90 border-primary"
                            : "bg-secondary text-secondary-foreground hover:bg-accent hover:text-accent-foreground border-border"
                        }`}
                        onClick={() => onTagToggle(tag)}
                      >
                        <span className="text-current">{tag}</span>
                        {isSelected && <X className="ml-1 h-3 w-3 text-current" />}
                      </Badge>
                    )
                  })}
                </div>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}
