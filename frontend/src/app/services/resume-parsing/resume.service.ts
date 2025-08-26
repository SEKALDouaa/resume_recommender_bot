import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ResumeResponse } from '../../models/resume-response.model';
import { StorageService } from '../storage/storage.service'; // 👈 import your storage service

@Injectable({
providedIn: 'root',
})
export class ResumeService {
private apiUrl = 'http://localhost:5000/resume/process-resume';
private resumeImageBaseUrl = 'http://localhost:5000/simple_resume/resume_image/';
private resumeMetadataBaseUrl = 'http://localhost:5000/resume';
private allResumeImagesUrl = 'http://localhost:5000/simple_resume/all_resume_images';

constructor(private http: HttpClient, private storage: StorageService) {}

  private getAuthHeaders(): HttpHeaders {
    const token = this.storage.getToken(); // 👈 fetch token
    return new HttpHeaders({
      Authorization: `Bearer ${token}`,
    });
  }

  processResumes(files: File[], imageUrl?: string): Observable<any> {
    const formData = new FormData();
    for (const file of files) {
      formData.append('images', file);
    }

    if (imageUrl) {
      formData.append('image_url', imageUrl);
    }

    return this.http.post<any>(this.apiUrl, formData, {
      headers: this.getAuthHeaders(),
    });
  }

  getResumeMetadata(resumeId: string): Observable<any> {
    return this.http.get(`${this.resumeMetadataBaseUrl}${resumeId}`, {
      headers: this.getAuthHeaders(),
    });
  }

  getResumeImage(resumeId: string): Observable<Blob> {
    return this.http.get(`${this.resumeImageBaseUrl}${resumeId}`, {
      responseType: 'blob',
      headers: this.getAuthHeaders(),
    });
  }

  getAllResumeImages(): Observable<string[]> {
    return this.http.get<string[]>(this.allResumeImagesUrl, {
      headers: this.getAuthHeaders(),
    });
  }
}
