import { Routes } from '@angular/router';
import { MainLayoutComponent } from './main-layout/main-layout.component';
import { ContentAComponent } from './content-a/content-a.component';
import { ContentBComponent } from './content-b/content-b.component';
import { LoginComponent } from "./pages/login/login.component";
import { RegisterComponent } from "./pages/register/register.component";

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
      },
      {
        path: 'login',
        component: LoginComponent
      },
      {
        path: 'register',
        component: RegisterComponent,
      }
    ]
  }
];
