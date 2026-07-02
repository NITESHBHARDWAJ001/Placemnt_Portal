export function isRequired(value) {
  if (value === null || value === undefined) return "This field is required"
  if (typeof value === "string" && value.trim() === "") return "This field is required"
  return null
}

export function isEmail(value) {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!value || !re.test(value)) return "Enter a valid email address"
  return null
}

export function minLength(min) {
  return (value) => {
    if (!value || value.length < min) return `Must be at least ${min} characters`
    return null
  }
}

export function isNumberInRange(min, max) {
  return (value) => {
    if (value === null || value === undefined || value === "") return null
    const num = Number(value)
    if (Number.isNaN(num) || num < min || num > max) return `Must be between ${min} and ${max}`
    return null
  }
}

export function runValidators(value, validatorFns) {
  for (const fn of validatorFns) {
    const error = fn(value)
    if (error) return error
  }
  return null
}
