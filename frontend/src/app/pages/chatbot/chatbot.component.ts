import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { DomSanitizer, SafeHtml, SafeUrl } from '@angular/platform-browser';
import { RagService, RagResponse } from '../../services/rag/rag.service';
import { ResumeService } from '../../services/resume-parsing/resume.service';
import { marked } from 'marked';

@Component({
selector: 'app-chatbot',
standalone: true,
imports: [CommonModule, FormsModule],
templateUrl: './chatbot.component.html',
styleUrls: ['./chatbot.component.css']
})
export class ChatbotComponent {
userMessage = '';
messages: { sender: 'user' | 'bot'; text: SafeHtml; imageUrls?: SafeUrl[] }[] = [];
isLoading = false;

// For image modal
modalImageUrl: SafeUrl | null = null;
showModal = false;

constructor(
    private ragService: RagService,
    private resumeService: ResumeService,
    private sanitizer: DomSanitizer
  ) {}

  async sendMessage() {
    const query = this.userMessage.trim();
    if (!query) return;

    // Show user message
    this.messages.push({ sender: 'user', text: this.sanitizer.bypassSecurityTrustHtml(query) });
    this.userMessage = '';
    this.isLoading = true;

    try {
      const res: RagResponse | undefined = await this.ragService.askQuestion(query).toPromise();
      if (!res) throw new Error('No response from backend');

      // Parse markdown answer
      const parsedAnswer = await marked.parse(res.answer || 'Pas de réponse disponible');
      const answerHtml: SafeHtml = this.sanitizer.bypassSecurityTrustHtml(parsedAnswer);

      // Fetch resume images
      const imageUrls: SafeUrl[] = [];
      if (res.ranked_resumes?.length) {
        for (const ranked of res.ranked_resumes) {
          try {
            const blob = await this.resumeService.getResumeImage(ranked.resume_id).toPromise();
            if (blob) {
              imageUrls.push(this.sanitizer.bypassSecurityTrustUrl(URL.createObjectURL(blob)));
            }
          } catch (err) {
            console.warn(`Failed to fetch image for resume ${ranked.resume_id}`, err);
          }
        }
      }

      // Add bot message
      this.messages.push({ sender: 'bot', text: answerHtml, imageUrls });

    } catch (err) {
      console.error('Error retrieving response:', err);
      this.messages.push({
        sender: 'bot',
        text: this.sanitizer.bypassSecurityTrustHtml('Erreur lors de la récupération de la réponse.')
      });
    } finally {
      this.isLoading = false;
    }
  }

  // Click to open image modal
  openImageModal(url: SafeUrl) {
    this.modalImageUrl = url;
    this.showModal = true;
  }

  closeModal() {
    this.modalImageUrl = null;
    this.showModal = false;
  }
}
