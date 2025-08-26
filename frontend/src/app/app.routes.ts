import { Routes } from '@angular/router';
import { MainLayoutComponent } from './layout/main-layout/main-layout.component';
import { AuthComponent } from './pages/auth/auth.component';
import { LandingLayoutComponent } from './layout/landing-layout/landing-layout.component';
import { LandingComponent } from './pages/landing/landing.component';
import { ChatbotComponent } from './pages/chatbot/chatbot.component';
import { UploadResumeComponent } from './pages/upload-resume/upload-resume.component';
import { ResumeGalleryComponent } from './pages/resume-gallery/resume-gallery.component';

export const routes: Routes = [
{ path: 'auth', component: AuthComponent },

{
path: '',
component: LandingLayoutComponent,
children: [
{ path: '', component: LandingComponent }
]
},

{
path: 'Home',
component: MainLayoutComponent,
children: [
{ path: 'chatbot', component: ChatbotComponent },
{ path: 'upload-resume', component: UploadResumeComponent },
{ path: 'resume-gallery', component: ResumeGalleryComponent },
]
},

{ path: '**', redirectTo: '' }
];

