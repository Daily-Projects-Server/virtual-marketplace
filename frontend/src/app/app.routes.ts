import { Routes } from '@angular/router';
import { MainLayoutComponent } from './main-layout/main-layout.component';
import { ContentAComponent } from './content-a/content-a.component';
import { ContentBComponent } from './content-b/content-b.component';

export const routes: Routes = [
  {
    path: '',
    component: MainLayoutComponent,
    children: [
      {
        path: 'component-a',
        component: ContentAComponent
      },
      {
        path: 'component-b',
        component: ContentBComponent
      }
    ]
  }
];

import { Routes } from '@angular/router';
import { LoginFormComponent } from './components/login-form/login-form.component';
import { MainComponent } from './components/main/main.component';
import { RegisterFormComponent } from './components/register-form/register-form.component';
import { ModalComponent } from './components/modal/modal.component';

export const routes: Routes = [
  { path: '', redirectTo: 'main', pathMatch: 'full' },
  {
    path: 'main',
    component: MainComponent,
  },
  {
    path: 'modal',
    component: ModalComponent,
    outlet: 'modal',
    children: [
      {
        path: 'login',
        component: LoginFormComponent,
      },
      { path: 'register', component: RegisterFormComponent },
    ],
  },
];
