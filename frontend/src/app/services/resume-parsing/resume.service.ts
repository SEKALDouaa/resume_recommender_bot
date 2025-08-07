import { Injectable } from '@angular/core';
import { HttpClient, HttpEvent, HttpEventType, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

interface ResumeResponse {
message: string;
resume_id: string;
error?: string;
}

@Injectable({
providedIn: 'root'
})
export class ResumeService {
private apiUrl = 'http://localhost:5000/process-resume'; // adjust base URL accordingly

constructor(private http: HttpClient) {}

  processResume(imageFile: File, imageUrl?: string): Observable<ResumeResponse> {
    const formData = new FormData();
    formData.append('image', imageFile);

    if (imageUrl) {
      formData.append('image_url', imageUrl);
    }

    return this.http.post<ResumeResponse>(this.apiUrl, formData);
  }
}
