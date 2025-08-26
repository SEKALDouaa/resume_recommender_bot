export interface ResumeResponse {
  message: string;       // success message from backend
  resume_id: string;     // ID returned by backend
  error?: string;        // error message (if any)
  traceback?: string;    // traceback (only on error)
}
