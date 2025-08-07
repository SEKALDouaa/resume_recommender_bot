import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface RagRequest {
query: string;
}

export interface RagResponse {
answer: string;
error?: string;
}

@Injectable({
providedIn: 'root',
})
export class RagService {
private apiUrl = 'http://localhost:5000/ask';

constructor(private http: HttpClient) {}

  askQuestion(query: string): Observable<RagResponse> {
    const payload: RagRequest = { query };
    return this.http.post<RagResponse>(this.apiUrl, payload);
  }
}
