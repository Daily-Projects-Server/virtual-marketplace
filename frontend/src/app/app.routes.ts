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
