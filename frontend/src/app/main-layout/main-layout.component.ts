import { ChangeDetectionStrategy, Component } from '@angular/core';

import { HeaderComponent } from '../components/header';
import { SidebarComponent } from '../components/sidebar';

@Component({
  selector: 'app-main-layout',
  standalone: true,
  imports: [HeaderComponent, SidebarComponent],
  templateUrl: './main-layout.component.html',
  styleUrl: './main-layout.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class MainLayoutComponent {}
