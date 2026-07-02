import { ref } from "vue"
import driveService from "@/services/drive.service"

export function useEligibility() {
  const checking = ref(false)
  const result = ref(null)

  async function check(driveId) {
    checking.value = true
    try {
      const { data } = await driveService.checkEligibility(driveId)
      result.value = data.data
      return data.data
    } finally {
      checking.value = false
    }
  }

  return { checking, result, check }
}
