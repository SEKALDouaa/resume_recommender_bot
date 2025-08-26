import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, map } from 'rxjs';
import { StorageService } from '../storage/storage.service'; // 👈 import your storage service

export interface RagRequest {
query: string;
}

export interface RankedResume {
rank: number;
resume_id: string;
image_url?: string;
}

export interface RagResponse {
answer: string;
ranked_resumes: RankedResume[];
error?: string;
}

@Injectable({
providedIn: 'root',
})
export class RagService {
private apiUrl = 'http://localhost:5000/qa/ask';

constructor(private http: HttpClient, private storage: StorageService) {}

  private getAuthHeaders(): HttpHeaders {
    const token = this.storage.getToken(); // 👈 fetch token from storage
    return new HttpHeaders({
      Authorization: `Bearer ${token}`,
    });
  }

  askQuestion(query: string): Observable<RagResponse> {
    const payload: RagRequest = { query };
    return this.http.post<any>(this.apiUrl, payload, {
      headers: this.getAuthHeaders(),
    }).pipe(
      map(res => res.response as RagResponse) // 👈 unwrap here
    );
  }
}
