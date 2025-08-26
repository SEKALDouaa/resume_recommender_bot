import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ResumeService } from '../../services/resume-parsing/resume.service';

@Component({
selector: 'app-upload-resume',
standalone: true,
imports: [CommonModule],
templateUrl: './upload-resume.component.html',
styleUrls: ['./upload-resume.component.css']
})
export class UploadResumeComponent {
selectedFiles: File[] = [];
uploadMessage = '';
isUploading = false;

constructor(private resumeService: ResumeService) {}

  onFilesSelected(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files?.length) {
      this.selectedFiles = Array.from(input.files);
    }
  }

  uploadResumes() {
    if (!this.selectedFiles.length) return;

    this.uploadMessage = '';
    this.isUploading = true;

    this.resumeService.processResumes(this.selectedFiles).subscribe({
      next: (res) => {
        this.uploadMessage = `Succès: ${res.message}`;
        this.isUploading = false;
      },
      error: () => {
        this.uploadMessage = "Erreur lors de l'upload.";
        this.isUploading = false;
      }
    });
  }
}
