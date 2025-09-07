"use client"

import type React from "react"

import { Search } from "lucide-react"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

interface SearchBarProps {
  value: string
  onChange: (value: string) => void
  onSearch: () => void
}

export function SearchBar({ value, onChange, onSearch }: SearchBarProps) {
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      onSearch()
    }
  }

  return (
    <div className="relative w-full max-w-2xl mx-auto">
      <div className="relative flex items-center">
        <Search className="absolute left-3 h-4 w-4 text-muted-foreground" />
        <Input
          type="text"
          placeholder="Explore problem statements..."
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onKeyPress={handleKeyPress}
          className="pl-10 pr-20 h-12 text-base bg-input border-border focus:ring-2 focus:ring-primary/20 focus:border-primary"
        />
        <Button
          onClick={onSearch}
          className="absolute right-1 h-10 px-4 bg-primary hover:bg-primary/90 text-primary-foreground"
        >
          Search
        </Button>
      </div>
    </div>
  )
}
