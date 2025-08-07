import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RagService } from '../../services/rag/rag.service';

@Component({
selector: 'app-chatbot',
standalone: true,
imports: [CommonModule, FormsModule],
templateUrl: './chatbot.component.html',
styleUrls: ['./chatbot.component.css']
})
export class ChatbotComponent {
userMessage = '';
messages: { sender: 'user' | 'bot', text: string }[] = [];
isLoading = false;

constructor(private ragService: RagService) {}

  sendMessage() {
    const query = this.userMessage.trim();
    if (!query) return;

    this.messages.push({ sender: 'user', text: query });
    this.userMessage = '';
    this.isLoading = true;

    this.ragService.askQuestion(query).subscribe({
      next: res => {
        this.messages.push({ sender: 'bot', text: res.answer });
        this.isLoading = false;
      },
      error: () => {
        this.messages.push({ sender: 'bot', text: 'Erreur lors de la récupération de la réponse.' });
        this.isLoading = false;
      }
    });
  }
}
