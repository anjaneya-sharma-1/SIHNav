export interface BookmarkedProblem {
  ps_id: string
  title: string
  summary: string
  difficulty: string | string[]
  organization: string
  bookmarkedAt: number
}

export class BookmarkManager {
  private static STORAGE_KEY = "sih-bookmarks"

  static getBookmarks(): BookmarkedProblem[] {
    if (typeof window === "undefined") return []

    try {
      const stored = localStorage.getItem(this.STORAGE_KEY)
      return stored ? JSON.parse(stored) : []
    } catch {
      return []
    }
  }

  static addBookmark(problem: any): void {
    if (typeof window === "undefined") return

    const bookmarks = this.getBookmarks()
    const bookmark: BookmarkedProblem = {
      ps_id: problem.ps_id,
      title: problem.title,
      summary: problem.summary,
      difficulty: problem.difficulty,
      organization: problem.organization,
      bookmarkedAt: Date.now(),
    }

    // Remove if already exists, then add to beginning
    const filtered = bookmarks.filter((b) => b.ps_id !== problem.ps_id)
    const updated = [bookmark, ...filtered]

    localStorage.setItem(this.STORAGE_KEY, JSON.stringify(updated))
  }

  static removeBookmark(ps_id: string): void {
    if (typeof window === "undefined") return

    const bookmarks = this.getBookmarks()
    const updated = bookmarks.filter((b) => b.ps_id !== ps_id)
    localStorage.setItem(this.STORAGE_KEY, JSON.stringify(updated))
  }

  static isBookmarked(ps_id: string): boolean {
    const bookmarks = this.getBookmarks()
    return bookmarks.some((b) => b.ps_id === ps_id)
  }

  static toggleBookmark(problem: any): boolean {
    if (this.isBookmarked(problem.ps_id)) {
      this.removeBookmark(problem.ps_id)
      return false
    } else {
      this.addBookmark(problem)
      return true
    }
  }
}
