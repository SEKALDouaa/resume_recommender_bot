import { Component, ElementRef, ViewChild, HostListener } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';

@Component({
selector: 'app-navbar',
standalone: true,
imports: [CommonModule, FormsModule, RouterModule],
templateUrl: './navbar.component.html',
styleUrl: './navbar.component.css'
})
export class NavbarComponent {
@ViewChild('searchInput') searchInput!: ElementRef<HTMLInputElement>;

searchExpanded = false;
currentLang = 'FR';
searchTerm = '';
isRootPage = false;
isLoading: boolean = false;

constructor(private router: Router) {
    this.router.events.subscribe(() => {
      this.isRootPage = this.router.url === '/' || this.router.url === '/Home' || this.router.url === '/Home/';
    });
  }

  toggleSearch(event: Event): void {
    event.stopPropagation();
    this.searchExpanded = !this.searchExpanded;

    if (this.searchExpanded) {
      setTimeout(() => {
        if (this.searchInput) {
          this.searchInput.nativeElement.focus();
        }
      }, 100);
    } else {
      this.clearSearch();
    }
  }

  toggleLang() {
    this.currentLang = this.currentLang === 'FR' ? 'EN' : 'FR';
  }

  @HostListener('document:click', ['$event'])
  handleClickOutside(event: Event): void {
    const target = event.target as HTMLElement;
    const searchContainer = target.closest('.search-container');

    if (this.searchExpanded && !searchContainer) {
      this.searchExpanded = false;
      this.clearSearch();
    }
  }

  goToDocumentation() {
    this.router.navigate(['/Home/documentation']);
  }

  onSearchInput(event: Event): void {
    const input = event.target as HTMLInputElement;
    this.searchTerm = input.value.trim();
  }

  private clearSearch(): void {
    this.searchTerm = '';
  }

  @HostListener('keydown', ['$event'])
  handleKeyDown(event: KeyboardEvent): void {
    if (this.searchExpanded) {
      switch (event.key) {
        case 'Escape':
          this.searchExpanded = false;
          this.clearSearch();
          break;
        case 'Enter':
          // Future action if you want Enter to trigger something
          break;
      }
    }
  }

  theme = {
    navbar: '#333333'
  };
}
