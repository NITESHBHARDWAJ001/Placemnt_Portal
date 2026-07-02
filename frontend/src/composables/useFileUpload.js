import { ref } from "vue"

export function useFileUpload() {
  const uploading = ref(false)
  const error = ref(null)

  async function upload(uploadFn) {
    uploading.value = true
    error.value = null
    try {
      const result = await uploadFn()
      return result
    } catch (e) {
      error.value = e.response?.data?.message || "Upload failed"
      throw e
    } finally {
      uploading.value = false
    }
  }

  return { uploading, error, upload }
}
