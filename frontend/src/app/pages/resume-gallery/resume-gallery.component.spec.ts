import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ResumeGalleryComponent } from './resume-gallery.component';

describe('ResumeGalleryComponent', () => {
  let component: ResumeGalleryComponent;
  let fixture: ComponentFixture<ResumeGalleryComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ResumeGalleryComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ResumeGalleryComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
