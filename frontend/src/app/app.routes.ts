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
