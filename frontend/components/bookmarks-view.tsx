"use client"

import { useState, useEffect } from "react"
import { BookmarkManager, type BookmarkedProblem } from "@/lib/bookmarks"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { BookmarkCheck, Building2, Calendar, ArrowLeft } from "lucide-react"

interface BookmarksViewProps {
  onBack: () => void
}

function getDifficultyInfo(difficulty: string | string[]) {
  const difficultyValue = Array.isArray(difficulty) ? difficulty[0] : difficulty

  switch (difficultyValue) {
    case "Easy":
      return { color: "border-l-green-500", badge: "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200" }
    case "Med":
      return {
        color: "border-l-yellow-500",
        badge: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200",
      }
    case "Hard":
      return { color: "border-l-red-500", badge: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200" }
    default:
      return { color: "border-l-gray-500", badge: "bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200" }
  }
}

function formatDifficultyLabel(difficulty: string | string[]) {
  const difficultyValue = Array.isArray(difficulty) ? difficulty[0] : difficulty
  return difficultyValue === "Med" ? "Medium" : difficultyValue
}

export function BookmarksView({ onBack }: BookmarksViewProps) {
  const [bookmarks, setBookmarks] = useState<BookmarkedProblem[]>([])

  useEffect(() => {
    setBookmarks(BookmarkManager.getBookmarks())
  }, [])

  const handleRemoveBookmark = (ps_id: string) => {
    BookmarkManager.removeBookmark(ps_id)
    setBookmarks(BookmarkManager.getBookmarks())
  }

  return (
    <div className="space-y-4 sm:space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center gap-3 sm:gap-4">
        <Button variant="ghost" onClick={onBack} className="flex items-center gap-2 self-start">
          <ArrowLeft className="h-4 w-4" />
          <span className="text-sm sm:text-base">Back to Search</span>
        </Button>
        <div className="flex-1">
          <h1 className="text-xl sm:text-2xl font-bold">Bookmarked Problems</h1>
          <p className="text-sm text-muted-foreground">{bookmarks.length} saved problems</p>
        </div>
      </div>

      {bookmarks.length === 0 ? (
        <Card className="p-6 sm:p-8 text-center">
          <div className="text-muted-foreground">
            <BookmarkCheck className="h-10 w-10 sm:h-12 sm:w-12 mx-auto mb-3 sm:mb-4 opacity-50" />
            <h3 className="text-base sm:text-lg font-medium mb-2">No bookmarks yet</h3>
            <p className="text-sm">Start bookmarking problems to save them for later!</p>
          </div>
        </Card>
      ) : (
        <div className="grid gap-3 sm:gap-4">
          {bookmarks.map((bookmark) => {
            const difficultyInfo = getDifficultyInfo(bookmark.difficulty)

            return (
              <Card
                key={bookmark.ps_id}
                className={`hover:shadow-md transition-shadow ${difficultyInfo.color} border-l-4`}
              >
                <CardHeader className="pb-3 px-4 sm:px-6">
                  <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-3">
                    <CardTitle className="text-base sm:text-lg font-semibold leading-tight pr-2">
                      {bookmark.title}
                    </CardTitle>
                    <div className="flex items-center gap-2 flex-shrink-0 self-start">
                      <Badge className={`text-xs px-2 py-1 font-medium ${difficultyInfo.badge}`}>
                        {formatDifficultyLabel(bookmark.difficulty)}
                      </Badge>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => handleRemoveBookmark(bookmark.ps_id)}
                        className="h-8 w-8 p-0 hover:bg-destructive/10 hover:text-destructive"
                      >
                        <BookmarkCheck className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                  <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 text-sm text-muted-foreground">
                    <span className="font-mono text-xs sm:text-sm">{bookmark.ps_id}</span>
                    <span className="flex items-center gap-1 text-xs sm:text-sm">
                      <Calendar className="h-3 w-3" />
                      {new Date(bookmark.bookmarkedAt).toLocaleDateString()}
                    </span>
                  </div>
                </CardHeader>

                <CardContent className="space-y-3 px-4 sm:px-6">
                  <p className="text-sm text-muted-foreground leading-relaxed line-clamp-3">{bookmark.summary}</p>

                  <div className="flex items-center gap-2 text-sm">
                    <Building2 className="w-4 h-4 text-muted-foreground flex-shrink-0" />
                    <span className="text-muted-foreground truncate">{bookmark.organization}</span>
                  </div>
                </CardContent>
              </Card>
            )
          })}
        </div>
      )}
    </div>
  )
}
