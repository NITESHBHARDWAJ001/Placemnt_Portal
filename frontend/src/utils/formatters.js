export function formatDate(value) {
  if (!value) return "-"
  const date = new Date(value)
  return date.toLocaleDateString("en-IN", { year: "numeric", month: "short", day: "numeric" })
}

export function formatDateTime(value) {
  if (!value) return "-"
  const date = new Date(value)
  return date.toLocaleString("en-IN", {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  })
}

export function formatCurrency(value) {
  if (value === null || value === undefined || value === "") return "-"
  return `₹${Number(value).toLocaleString("en-IN")} LPA`
}

export function formatStatusLabel(value) {
  if (!value) return ""
  return value
    .split("_")
    .map((w) => w.charAt(0) + w.slice(1).toLowerCase())
    .join(" ")
}

export function initials(name) {
  if (!name) return "?"
  return name
    .split(" ")
    .map((p) => p[0])
    .slice(0, 2)
    .join("")
    .toUpperCase()
}
