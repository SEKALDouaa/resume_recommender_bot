import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ResumeService } from '../../services/resume-parsing/resume.service';
import { HttpClientModule } from '@angular/common/http';

@Component({
selector: 'app-resume-gallery',
standalone: true,
imports: [CommonModule, HttpClientModule],
templateUrl: './resume-gallery.component.html',
styleUrls: ['./resume-gallery.component.css'],
})
export class ResumeGalleryComponent implements OnInit {
images: { src: string; index: number }[] = [];
isLoading = false;
error: string | null = null;

selectedImage: string | null = null;

constructor(private resumeService: ResumeService) {}

  ngOnInit(): void {
    this.loadAllResumeImages();
  }

  loadAllResumeImages() {
    this.isLoading = true;
    this.error = null;

    this.resumeService.getAllResumeImages().subscribe({
      next: (base64Images) => {
        this.images = base64Images.map((base64, i) => ({
          src: `data:image/jpeg;base64,${base64}`,
          index: i + 1,
        }));
        this.isLoading = false;
      },
      error: () => {
        this.error = 'Erreur lors du chargement des CVs.';
        this.isLoading = false;
      },
    });
  }

  openImage(src: string) {
    this.selectedImage = src;
  }

  closeModal() {
    this.selectedImage = null;
  }
}
